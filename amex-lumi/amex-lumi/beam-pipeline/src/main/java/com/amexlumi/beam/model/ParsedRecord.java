package com.amexlumi.beam.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ParsedRecord implements Serializable {

    private static final long serialVersionUID = 1L;

    public enum Status {
        VALID,
        ERROR
    }

    private final Status status;
    private final EmployeeRecord employeeRecord;
    private final Map<String, Object> sourceRecord;
    private final List<String> violations;

    private ParsedRecord(
            Status status,
            EmployeeRecord employeeRecord,
            Map<String, Object> sourceRecord,
            List<String> violations) {

        this.status = status;
        this.employeeRecord = employeeRecord;

        this.sourceRecord = sourceRecord == null
                ? new LinkedHashMap<>()
                : new LinkedHashMap<>(sourceRecord);

        this.violations = violations == null
                ? new ArrayList<>()
                : new ArrayList<>(violations);
    }

    public static ParsedRecord valid(
            EmployeeRecord employeeRecord) {

        return new ParsedRecord(
                Status.VALID,
                employeeRecord,
                employeeRecord == null
                        ? Collections.emptyMap()
                        : employeeRecord.toMap(),
                Collections.emptyList()
        );
    }

    public static ParsedRecord error(
            Map<String, Object> sourceRecord,
            List<String> violations) {

        EmployeeRecord employeeRecord =
                sourceRecord == null
                        ? new EmployeeRecord()
                        : new EmployeeRecord(sourceRecord);

        return new ParsedRecord(
                Status.ERROR,
                employeeRecord,
                sourceRecord,
                violations
        );
    }

    public Status getStatus() {
        return status;
    }

    public EmployeeRecord getEmployeeRecord() {
        return employeeRecord;
    }

    public Map<String, Object> getSourceRecord() {
        return Collections.unmodifiableMap(sourceRecord);
    }

    public List<String> getViolations() {
        return Collections.unmodifiableList(violations);
    }

    public boolean isValid() {
        return status == Status.VALID;
    }

    public boolean isError() {
        return status == Status.ERROR;
    }

    @Override
    public String toString() {

        return "ParsedRecord{" +
                "status=" + status +
                ", employeeRecord=" + employeeRecord +
                ", sourceRecord=" + sourceRecord +
                ", violations=" + violations +
                '}';
    }
}
