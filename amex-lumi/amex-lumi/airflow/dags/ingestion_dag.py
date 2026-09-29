import glob   
import logging
import os
import subprocess
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from configparser import ConfigParser


import psycopg2


from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.operators.python import PythonOperator


DAG_ID = "lumi_ingestion_dag"


BEAM_IMAGE = os.environ.get(
    "LUMI_BEAM_IMAGE",
    "amex-lumi-case-study-beam-runner",
)


HOST_PROJECT_DIR = os.environ.get(
    "LUMI_HOST_PROJECT_DIR",
    "C:/Users/Garvit Shrivastava/amex-lumi-case-study",
)


DOCKER_NETWORK = os.environ.get(
    "LUMI_DOCKER_NETWORK",
    "amex-lumi-case-study_default",
)


DEFAULT_POSTGRES_DSN = os.environ.get(
    "LUMI_POSTGRES_DSN",
    "postgresql://lumi_user:change_me@postgres:5432/lumi_warehouse",
)


ERROR_DIRECTORY = "/opt/errors"


DATA_DIRECTORY = "/opt/data"


SUPPORTED_EXTENSIONS = {
    ".json": "JSON",
    ".csv": "CSV",
    ".xml": "XML",
}


DOCKER_TIMEOUT_SECONDS = 600


logger = logging.getLogger(__name__)


def read_control_file(control_file_path):
   

    if not control_file_path:
        raise AirflowException(
            "Missing required DAG parameter: "
            "control_file_path"
        )

    control_path = (
        Path(control_file_path)
        .resolve()
    )

    data_directory = (
        Path(DATA_DIRECTORY)
        .resolve()
    )

    try:
        control_path.relative_to(
            data_directory
        )
    except ValueError as exc:
        raise AirflowException(
            "control_file_path must be inside "
            f"{DATA_DIRECTORY}: {control_file_path}"
        ) from exc

    if not control_path.exists():
        raise AirflowException(
            "Control file does not exist: "
            f"{control_file_path}"
        )

    if not control_path.is_file():
        raise AirflowException(
            "Control file path is not a regular file: "
            f"{control_file_path}"
        )

    properties = ConfigParser(
        interpolation=None
    )

    try:
        with open(
            control_path,
            "r",
            encoding="utf-8",
        ) as control_file:

            raw_lines = [
                line
                for line in control_file
                if line.strip()
                and not line.lstrip().startswith("#")
                and not line.lstrip().startswith(";")
            ]

        normalized_content = "[control]\n" + "".join(
            raw_lines
        )

        properties.read_string(
            normalized_content
        )

    except Exception as exc:
        raise AirflowException(
            "Unable to read control file: "
            f"{control_file_path}. "
            f"Error: {exc}"
        ) from exc

    if not properties.has_option(
        "control",
        "record_count",
    ):
        raise AirflowException(
            "Control file must contain the "
            "'record_count' property: "
            f"{control_file_path}"
        )

    record_count_value = properties.get(
        "control",
        "record_count",
    ).strip()

    if not record_count_value:
        raise AirflowException(
            "The 'record_count' property in the "
            "control file must not be empty: "
            f"{control_file_path}"
        )

    try:
        expected_record_count = int(
            record_count_value
        )

    except ValueError as exc:
        raise AirflowException(
            "The 'record_count' property must be a "
            "non-negative integer. "
            f"Received: {record_count_value}"
        ) from exc

    if expected_record_count < 0:
        raise AirflowException(
            "The 'record_count' property must not be "
            "negative. "
            f"Received: {expected_record_count}"
        )

    logger.info(
        "Control file validated successfully."
    )

    logger.info(
        "Control file: %s",
        control_file_path,
    )

    logger.info(
        "Expected record count: %s",
        expected_record_count,
    )

    return expected_record_count


def validate_input(**context):
    """
    STEP 1
    Validate all input files received from the
    ingestion API and validate the Phase 3
    control file.
    """

    dag_run = context.get("dag_run")

    if dag_run is None:
        raise AirflowException(
            "DAG run context is missing."
        )

    conf = dag_run.conf or {}

    execution_id = conf.get(
        "execution_id"
    )

    if not execution_id:
        execution_id = str(
            uuid.uuid4()
        )

    try:
        uuid.UUID(
            execution_id
        )
    except ValueError as exc:
        raise AirflowException(
            f"Invalid execution_id: {execution_id}"
        ) from exc

    file_paths = conf.get(
        "file_paths"
    )

    if not file_paths:

        file_path = conf.get(
            "file_path"
        )

        if not file_path:
            raise AirflowException(
                "Missing required DAG parameter: "
                "file_path or file_paths"
            )

        file_paths = [
            file_path
        ]

    if not isinstance(
        file_paths,
        list
    ) or not file_paths:

        raise AirflowException(
            "file_paths must be a non-empty list."
        )

    validated_files = []

    for file_path in file_paths:

        if not file_path:
            raise AirflowException(
                "A file path in file_paths is empty."
            )

        if not os.path.isfile(
                file_path):

            raise AirflowException(
                f"Input file does not exist: "
                f"{file_path}"
            )

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension not in SUPPORTED_EXTENSIONS:

            raise AirflowException(
                "Unsupported file type: "
                f"{file_path}. "
                f"Supported extensions: "
                f"{list(SUPPORTED_EXTENSIONS.keys())}"
            )

        validated_files.append(
            file_path
        )

    postgres_dsn = conf.get(
        "postgres_dsn",
        DEFAULT_POSTGRES_DSN,
    )

    encryption_key = os.environ.get(
        "FIELD_ENCRYPTION_KEY"
    )

    if not encryption_key:
        raise AirflowException(
            "FIELD_ENCRYPTION_KEY is not configured."
        )

    control_file_path = conf.get(
        "control_file_path"
    )

    expected_record_count = (
        read_control_file(
            control_file_path
        )
    )

    os.makedirs(
        ERROR_DIRECTORY,
        exist_ok=True,
    )

    result = {
        "file_paths": validated_files,
        "execution_id": execution_id,
        "postgres_dsn": postgres_dsn,
        "control_file_path": control_file_path,
        "expected_record_count": expected_record_count,
    }

    logger.info(
        "Input validation successful."
    )

    logger.info(
        "Execution ID: %s",
        execution_id,
    )

    logger.info(
        "Number of input files: %s",
        len(validated_files),
    )

    logger.info(
        "Control file: %s",
        control_file_path,
    )

    logger.info(
        "Expected record count: %s",
        expected_record_count,
    )

    for index, file_path in enumerate(
            validated_files,
            start=1):

        logger.info(
            "Input file %s: %s",
            index,
            file_path,
        )

    return result


def run_beam_ingestion(**context):
    """
    STEP 2
    Run Java Beam sequentially for every prepared
    source file.
    """

    ti = context["ti"]

    input_details = ti.xcom_pull(
        task_ids="validate_input"
    )

    if not input_details:
        raise AirflowException(
            "Input details were not returned by "
            "validate_input."
        )

    file_paths = input_details[
        "file_paths"
    ]

    execution_id = input_details[
        "execution_id"
    ]

    postgres_dsn = input_details[
        "postgres_dsn"
    ]

    successful_files = []

    for index, file_path in enumerate(
            file_paths,
            start=1):

        error_output_path = os.path.join(
            ERROR_DIRECTORY,
            f"{execution_id}_part_{index:03d}",
        )

        logger.info(
            "=========================================="
        )

        logger.info(
            "Starting Java Beam for file %s/%s",
            index,
            len(file_paths),
        )

        logger.info(
            "Execution ID: %s",
            execution_id,
        )

        logger.info(
            "Input file: %s",
            file_path,
        )

        logger.info(
            "Error output prefix: %s",
            error_output_path,
        )

        command = [
            "docker",
            "run",
            "--rm",
            "--network",
            DOCKER_NETWORK,
            "--env",
            "FIELD_ENCRYPTION_KEY",
            "--volume",
            f"{HOST_PROJECT_DIR}/data:/opt/data",
            "--volume",
            f"{HOST_PROJECT_DIR}/errors:/opt/errors",
            BEAM_IMAGE,
            "--file_path",
            file_path,
            "--execution_id",
            execution_id,
            "--postgres_dsn",
            postgres_dsn,
            "--error_output_path",
            error_output_path,
        ]

        process = None

        try:

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            logger.info(
                "Java Beam worker started with PID: %s",
                process.pid,
            )

            if process.stdout is not None:

                for line in process.stdout:

                    line = line.rstrip()

                    if line:
                        logger.info(
                            "Java Beam: %s",
                            line,
                        )

            return_code = process.wait(
                timeout=DOCKER_TIMEOUT_SECONDS
            )

        except subprocess.TimeoutExpired as exc:

            logger.error(
                "Java Beam worker exceeded "
                "%s seconds.",
                DOCKER_TIMEOUT_SECONDS,
            )

            if process is not None:

                process.kill()

                try:
                    process.wait(
                        timeout=10
                    )

                except subprocess.TimeoutExpired:

                    logger.error(
                        "Unable to terminate Java Beam "
                        "worker cleanly."
                    )

            raise AirflowException(
                "Java Beam Docker worker timed out."
            ) from exc

        except OSError as exc:

            logger.exception(
                "Unable to start Docker worker."
            )

            raise AirflowException(
                "Unable to execute Java Beam Docker "
                f"worker: {exc}"
            ) from exc

        if return_code != 0:

            raise AirflowException(
                "Java Beam Docker worker failed "
                f"for file {file_path} with "
                f"exit code {return_code}."
            )

        successful_files.append(
            file_path
        )

        logger.info(
            "Java Beam completed successfully "
            "for file: %s",
            file_path,
        )

    return {
        "execution_id": execution_id,
        "file_paths": successful_files,
        "file_count": len(successful_files),
    }


def validate_results(**context):
    

    ti = context["ti"]

    input_details = ti.xcom_pull(
        task_ids="validate_input"
    )

    if not input_details:
        raise AirflowException(
            "Input details are unavailable."
        )

    execution_id = input_details[
        "execution_id"
    ]

    postgres_dsn = input_details[
        "postgres_dsn"
    ]

    file_paths = input_details[
        "file_paths"
    ]

    control_file_path = input_details[
        "control_file_path"
    ]

    expected_record_count = input_details[
        "expected_record_count"
    ]

    logger.info(
        "Validating ingestion results."
    )

    logger.info(
        "Execution ID: %s",
        execution_id,
    )

    logger.info(
        "Control file: %s",
        control_file_path,
    )

    logger.info(
        "Expected record count: %s",
        expected_record_count,
    )

    connection = None

    try:

        connection = psycopg2.connect(
            postgres_dsn
        )

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ingested_records
                WHERE execution_id = %s
                """,
                (
                    execution_id,
                ),
            )

            valid_record_count = cursor.fetchone()[0]

    except Exception as exc:

        raise AirflowException(
            "Unable to validate PostgreSQL "
            f"results: {exc}"
        ) from exc

    finally:

        if connection is not None:
            connection.close()

    error_files = sorted(
        glob.glob(
            os.path.join(
                ERROR_DIRECTORY,
                f"{execution_id}_part_*.txt",
            )
        )
    )

    error_record_count = 0

    for error_file in error_files:

        with open(
            error_file,
            "r",
            encoding="utf-8",
        ) as file:

            error_record_count += sum(
                1
                for line in file
                if line.strip()
            )

    logger.info(
        "Input files processed: %s",
        len(file_paths),
    )

    logger.info(
        "Valid records written to PostgreSQL: %s",
        valid_record_count,
    )

    logger.info(
        "Invalid records written to error output: %s",
        error_record_count,
    )

    logger.info(
        "Error files generated: %s",
        len(error_files),
    )

    if valid_record_count != expected_record_count:

        error_message = (
            "Record count validation failed: "
            f"expected {expected_record_count} "
            f"records but actually loaded "
            f"{valid_record_count} records."
        )

        logger.error(
            error_message
        )

        raise AirflowException(
            error_message
        )

    logger.info(
        "Record count validation successful: "
        "expected=%s, actual=%s",
        expected_record_count,
        valid_record_count,
    )

    result = {
        "execution_id": execution_id,
        "input_file_count": len(file_paths),
        "expected_record_count": expected_record_count,
        "valid_record_count": valid_record_count,
        "error_record_count": error_record_count,
        "error_files": error_files,
        "record_count_validation": "PASSED",
    }

    return result


def finalize_ingestion(**context):
    """
    STEP 4
    Finalize the ingestion run and log the summary.
    """

    ti = context["ti"]

    result = ti.xcom_pull(
        task_ids="validate_results"
    )

    if not result:
        raise AirflowException(
            "No validation result received."
        )

    logger.info(
        "=========================================="
    )

    logger.info(
        "LUMI INGESTION COMPLETED"
    )

    logger.info(
        "Execution ID: %s",
        result["execution_id"],
    )

    logger.info(
        "Input files processed: %s",
        result["input_file_count"],
    )

    logger.info(
        "Expected records: %s",
        result["expected_record_count"],
    )

    logger.info(
        "Valid records: %s",
        result["valid_record_count"],
    )

    logger.info(
        "Invalid records: %s",
        result["error_record_count"],
    )

    logger.info(
        "Record count validation: %s",
        result["record_count_validation"],
    )

    logger.info(
        "Error files: %s",
        result["error_files"],
    )

    logger.info(
        "=========================================="
    )

    return result


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(
        minutes=1
    ),
}


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description=(
        "Amex Lumi employee ingestion using "
        "Airflow, Java Apache Beam, and PySpark"
    ),
    start_date=datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    ),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=[
        "amex",
        "lumi",
        "ingestion",
        "beam",
        "pyspark",
    ],
) as dag:

    validate_input_task = PythonOperator(
        task_id="validate_input",
        python_callable=validate_input,
    )

    run_beam_ingestion_task = PythonOperator(
        task_id="run_beam_ingestion",
        python_callable=run_beam_ingestion,
    )

    validate_results_task = PythonOperator(
        task_id="validate_results",
        python_callable=validate_results,
    )

    finalize_ingestion_task = PythonOperator(
        task_id="finalize_ingestion",
        python_callable=finalize_ingestion,
    )

    (
        validate_input_task
        >> run_beam_ingestion_task
        >> validate_results_task
        >> finalize_ingestion_task
    )
