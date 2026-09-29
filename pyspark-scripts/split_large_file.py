import argparse
import csv
import json
import math
import os
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable

from pyspark.sql import SparkSession


SUPPORTED_EXTENSIONS = {
    ".csv": "CSV",
    ".json": "JSON",
    ".xml": "XML",
}

DEFAULT_TARGET_PART_SIZE_BYTES = 50 * 1024 * 1024


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Split large CSV, JSON, or XML files into "
            "record-safe parts based on a configurable "
            "target size."
        )
    )

    parser.add_argument(
        "--input_path",
        required=True,
        help="Path to the source file.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory where split files will be created.",
    )

    parser.add_argument(
        "--threshold_bytes",
        type=int,
        default=DEFAULT_TARGET_PART_SIZE_BYTES,
        help=(
            "Target maximum size in bytes for each output part."
        ),
    )

    return parser.parse_args()

def validate_arguments(
    arguments: argparse.Namespace,
) -> Path:
    if arguments.threshold_bytes <= 0:
        raise ValueError(
            "--threshold_bytes must be greater than zero."
        )

    input_path = Path(
        arguments.input_path
    ).resolve()

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"Input path is not a regular file: {input_path}"
        )

    extension = input_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file format: "
            f"{extension}. Supported formats are: "
            f"{', '.join(sorted(SUPPORTED_EXTENSIONS.keys()))}"
        )

    return input_path

def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("LumiLargeFileSplitter")
        .master("local[*]")
        .config(
            "spark.sql.adaptive.enabled",
            "false",
        )
        .getOrCreate()
    )


def calculate_part_count(
    file_size: int,
    threshold_bytes: int,
) -> int:
    if file_size <= threshold_bytes:
        return 1

    return max(
        2,
        math.ceil(
            file_size / threshold_bytes
        ),
    )


def utf8_size(value: str) -> int:
    return len(
        value.encode("utf-8")
    )


def create_output_directory(
    output_dir: Path,
) -> None:
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


def remove_if_exists(
    path: Path,
) -> None:
    if path.is_dir():
        shutil.rmtree(path)

    elif path.exists():
        path.unlink()


def split_csv(
    spark: SparkSession,
    input_path: Path,
    output_dir: Path,
    threshold_bytes: int,
) -> list[Path]:
    dataframe = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "false")
        .option("mode", "PERMISSIVE")
        .csv(str(input_path))
    )

    header = dataframe.columns

    if not header:
        raise ValueError(
            "CSV source does not contain a header."
        )

    rows = (
        dataframe.rdd
        .map(
            lambda row: row.asDict(
                recursive=True
            )
        )
    )

    row_chunks = (
        rows
        .mapPartitions(
            lambda iterator: csv_records_to_chunks(
                iterator,
                header,
                threshold_bytes,
            )
        )
        .collect()
    )

    if not row_chunks:
        raise ValueError(
            "CSV source does not contain any data records."
        )

    output_files = []

    for index, chunk in enumerate(
        row_chunks,
        start=1,
    ):
        destination = (
            output_dir
            / f"part-{index:03d}.csv"
        )

        write_csv_chunk(
            header,
            chunk,
            destination,
        )

        output_files.append(
            destination
        )

    return output_files


def csv_records_to_chunks(
    rows: Iterable[dict[str, Any]],
    header: list[str],
    threshold_bytes: int,
) -> Iterable[list[dict[str, Any]]]:
    current_records: list[dict[str, Any]] = []

    header_line = csv_row_to_string(
        header,
        header,
    )

    current_size = utf8_size(
        header_line
    )

    for row in rows:
        values = [
            normalize_csv_value(
                row.get(column)
            )
            for column in header
        ]

        row_line = csv_row_to_string(
            values,
            header,
        )

        row_size = utf8_size(
            row_line
        )

        if (
            current_records
            and current_size + row_size > threshold_bytes
        ):
            yield current_records

            current_records = []

            current_size = utf8_size(
                header_line
            )

        current_records.append(
            row
        )

        current_size += row_size

        if (
            len(current_records) == 1
            and current_size > threshold_bytes
        ):
            yield current_records

            current_records = []

            current_size = utf8_size(
                header_line
            )

    
    if current_records:
        yield current_records


def normalize_csv_value(
    value: Any,
) -> str:
    if value is None:
        return ""

    return str(value)


def csv_row_to_string(
    values: list[Any],
    header: list[str],
) -> str:
    from io import StringIO

    buffer = StringIO()

    writer = csv.writer(
        buffer,
        lineterminator="\n",
        quoting=csv.QUOTE_MINIMAL,
    )

    writer.writerow(values)

    return buffer.getvalue()


def write_csv_chunk(
    header: list[str],
    records: list[dict[str, Any]],
    destination: Path,
) -> None:
    with destination.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=header,
            extrasaction="ignore",
            lineterminator="\n",
        )

        writer.writeheader()

        for record in records:
            writer.writerow(
                {
                    column: normalize_csv_value(
                        record.get(column)
                    )
                    for column in header
                }
            )


def split_json(
    spark: SparkSession,
    input_path: Path,
    output_dir: Path,
    threshold_bytes: int,
) -> list[Path]:
    dataframe = (
        spark.read
        .option("multiLine", "true")
        .option("mode", "PERMISSIVE")
        .json(str(input_path))
    )

    rows = (
        dataframe.rdd
        .map(
            lambda row: row.asDict(
                recursive=True
            )
        )
    )

    record_chunks = (
        rows
        .mapPartitions(
            lambda iterator: json_records_to_chunks(
                iterator,
                threshold_bytes,
            )
        )
        .collect()
    )

    if not record_chunks:
        raise ValueError(
            "JSON source does not contain any records."
        )

    output_files = []

    for index, records in enumerate(
        record_chunks,
        start=1,
    ):
        destination = (
            output_dir
            / f"part-{index:03d}.json"
        )

        write_json_chunk(
            records,
            destination,
        )

        output_files.append(
            destination
        )

    return output_files


def json_records_to_chunks(
    rows: Iterable[dict[str, Any]],
    threshold_bytes: int,
) -> Iterable[list[dict[str, Any]]]:
    current_records: list[dict[str, Any]] = []

    for row in rows:
        record_json = json.dumps(
            row,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        if not current_records:
            candidate = [
                row
            ]
        else:
            candidate = (
                current_records
                + [row]
            )

        candidate_json = json.dumps(
            candidate,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        candidate_size = utf8_size(
            candidate_json
        )

        if (
            current_records
            and candidate_size > threshold_bytes
        ):
            yield current_records

            current_records = [
                row
            ]

            single_record_json = json.dumps(
                current_records,
                ensure_ascii=False,
                separators=(",", ":"),
            )

            if utf8_size(
                single_record_json
            ) > threshold_bytes:
                yield current_records
                current_records = []

        elif (
            not current_records
            and candidate_size > threshold_bytes
        ):
            yield current_records if current_records else [row]

            current_records = []

        else:
            current_records = candidate

        if record_json == "":
            continue

    if current_records:
        yield current_records


def write_json_chunk(
    records: list[dict[str, Any]],
    destination: Path,
) -> None:
    with destination.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            records,
            file,
            ensure_ascii=False,
            separators=(",", ":"),
        )


def split_xml(
    input_path: Path,
    output_dir: Path,
    threshold_bytes: int,
) -> list[Path]:
    tree = ET.parse(
        str(input_path)
    )

    root = tree.getroot()

    records = list(root)

    if not records:
        raise ValueError(
            "XML source does not contain any records."
        )

    chunks = xml_records_to_chunks(
        root,
        records,
        threshold_bytes,
    )

    output_files = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        destination = (
            output_dir
            / f"part-{index:03d}.xml"
        )

        write_xml_chunk(
            root,
            chunk,
            destination,
        )

        output_files.append(
            destination
        )

    return output_files


def xml_records_to_chunks(
    root: ET.Element,
    records: list[ET.Element],
    threshold_bytes: int,
) -> list[list[ET.Element]]:
    chunks: list[list[ET.Element]] = []

    current_chunk: list[ET.Element] = []

    for record in records:
        candidate = (
            current_chunk
            + [record]
        )

        candidate_bytes = xml_chunk_size(
            root,
            candidate,
        )

        if (
            current_chunk
            and candidate_bytes > threshold_bytes
        ):
            chunks.append(
                current_chunk
            )

            current_chunk = [
                record
            ]

            single_record_bytes = xml_chunk_size(
                root,
                current_chunk,
            )

            if (
                single_record_bytes
                > threshold_bytes
            ):
                chunks.append(
                    current_chunk
                )

                current_chunk = []

        elif (
            not current_chunk
            and candidate_bytes > threshold_bytes
        ):
            chunks.append(
                [record]
            )

            current_chunk = []

        else:
            current_chunk = candidate

    if current_chunk:
        chunks.append(
            current_chunk
        )

    return chunks


def xml_chunk_size(
    original_root: ET.Element,
    records: list[ET.Element],
) -> int:
    temporary_root = ET.Element(
        original_root.tag,
        original_root.attrib,
    )

    for record in records:
        temporary_root.append(
            clone_xml_element(record)
        )

    tree = ET.ElementTree(
        temporary_root
    )

    from io import BytesIO

    buffer = BytesIO()

    tree.write(
        buffer,
        encoding="utf-8",
        xml_declaration=True,
    )

    return len(
        buffer.getvalue()
    )


def write_xml_chunk(
    original_root: ET.Element,
    records: list[ET.Element],
    destination: Path,
) -> None:
    new_root = ET.Element(
        original_root.tag,
        original_root.attrib,
    )

    for record in records:
        new_root.append(
            clone_xml_element(record)
        )

    tree = ET.ElementTree(
        new_root
    )

    ET.indent(
        tree,
        space="  ",
    )

    tree.write(
        destination,
        encoding="utf-8",
        xml_declaration=True,
    )


def clone_xml_element(
    element: ET.Element,
) -> ET.Element:
    new_element = ET.Element(
        element.tag,
        element.attrib,
    )

    new_element.text = element.text
    new_element.tail = element.tail

    for child in element:
        new_element.append(
            clone_xml_element(child)
        )

    return new_element


def create_manifest(
    input_path: Path,
    output_dir: Path,
    threshold_bytes: int,
    output_files: list[Path],
) -> Path:
    manifest = {
        "source_file": str(
            input_path
        ),
        "source_file_name": input_path.name,
        "source_format": SUPPORTED_EXTENSIONS[
            input_path.suffix.lower()
        ],
        "source_file_size_bytes": input_path.stat().st_size,
        "threshold_bytes": threshold_bytes,
        "part_count": len(
            output_files
        ),
        "parts": [
            {
                "part_number": index,
                "file_name": output_file.name,
                "file_path": str(
                    output_file
                ),
                "file_size_bytes": output_file.stat().st_size,
                "within_threshold": (
                    output_file.stat().st_size
                    <= threshold_bytes
                ),
            }
            for index, output_file in enumerate(
                output_files,
                start=1,
            )
        ],
    }

    manifest_path = (
        output_dir
        / "manifest.json"
    )

    with manifest_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            manifest,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return manifest_path


def main() -> int:
    arguments = parse_arguments()

    try:
        input_path = validate_arguments(
            arguments
        )

        output_dir = Path(
            arguments.output_dir
        ).resolve()

        create_output_directory(
            output_dir
        )

        file_size = input_path.stat().st_size

        print(
            f"Input file: {input_path}"
        )

        print(
            f"Input size: {file_size} bytes"
        )

        print(
            f"Threshold: "
            f"{arguments.threshold_bytes} bytes"
        )

        if file_size <= arguments.threshold_bytes:
            print(
                "SOURCE_FILE_BELOW_THRESHOLD"
            )

            manifest_path = create_manifest(
                input_path,
                output_dir,
                arguments.threshold_bytes,
                [input_path],
            )

            print(
                f"Manifest: {manifest_path}"
            )

            return 0

        print(
            "SOURCE_FILE_ABOVE_THRESHOLD"
        )

        extension = input_path.suffix.lower()

        spark = None

        try:
            if extension in {
                ".csv",
                ".json",
            }:
                spark = create_spark_session()

            if extension == ".csv":
                output_files = split_csv(
                    spark,
                    input_path,
                    output_dir,
                    arguments.threshold_bytes,
                )

            elif extension == ".json":
                output_files = split_json(
                    spark,
                    input_path,
                    output_dir,
                    arguments.threshold_bytes,
                )

            elif extension == ".xml":
                output_files = split_xml(
                    input_path,
                    output_dir,
                    arguments.threshold_bytes,
                )

            else:
                raise ValueError(
                    f"Unsupported format: {extension}"
                )

        finally:
            if spark is not None:
                spark.stop()

        manifest_path = create_manifest(
            input_path,
            output_dir,
            arguments.threshold_bytes,
            output_files,
        )

        print(
            "SPLIT_COMPLETED"
        )

        print(
            f"Created parts: "
            f"{len(output_files)}"
        )

        for output_file in output_files:
            size = output_file.stat().st_size

            print(
                f"PART: {output_file} "
                f"SIZE: {size} bytes"
            )

        print(
            f"MANIFEST: {manifest_path}"
        )

        return 0

    except Exception as exception:
        print(
            "SPLIT_FAILED",
            file=sys.stderr,
        )

        print(
            str(exception),
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )




