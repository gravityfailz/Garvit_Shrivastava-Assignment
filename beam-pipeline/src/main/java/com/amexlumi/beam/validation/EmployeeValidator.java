package com.amexlumi.beam.validation;

import com.amexlumi.beam.model.EmployeeRecord;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class EmployeeValidator {

    private static final Map<String, LengthConstraint> FIELD_LENGTH_CONSTRAINTS;

    static {
        Map<String, LengthConstraint> constraints = new LinkedHashMap<>();

        constraints.put("employee_id", new LengthConstraint(7, 7));
        constraints.put("first_name", new LengthConstraint(3, 15));
        constraints.put("last_name", new LengthConstraint(0, 15));
        constraints.put("email", new LengthConstraint(13, 30));
        constraints.put("phone_number", new LengthConstraint(10, 10));
        constraints.put("hire_date", new LengthConstraint(10, 10));
        constraints.put("department", new LengthConstraint(0, 20));
        constraints.put("job_title", new LengthConstraint(0, 30));
        constraints.put("currency", new LengthConstraint(3, 3));
        constraints.put("employment_status", new LengthConstraint(3, 13));
        constraints.put("manager_id", new LengthConstraint(7, 7));
        constraints.put("is_active", new LengthConstraint(4, 4));

        FIELD_LENGTH_CONSTRAINTS =
                Collections.unmodifiableMap(constraints);
    }

    private EmployeeValidator() {
        // Utility class.
    }

    /**
     * Validates an employee record using the same length-based rules
     */
    public static List<String> validate(EmployeeRecord record) {

        if (record == null) {
            return List.of("record: record is null");
        }

        return validate(record.toMap());
    }

    /**
     * Validates a raw employee map.
     */
    public static List<String> validate(Map<String, Object> record) {

        List<String> violations = new ArrayList<>();

        if (record == null) {
            violations.add("record: record is null");
            return violations;
        }

        for (Map.Entry<String, LengthConstraint> entry
                : FIELD_LENGTH_CONSTRAINTS.entrySet()) {

            String field = entry.getKey();
            LengthConstraint constraint = entry.getValue();

            Object value = record.get(field);

            /*
             * value = record.get(field)
             * if value is None:
             *     continue
             */
            if (value == null) {
                continue;
            }

            String stringValue = String.valueOf(value);
            int length = stringValue.length();

            if (!constraint.isValid(length)) {
                violations.add(
                        String.format(
                                "%s: length %d not in [%d,%d] (value=%s)",
                                field,
                                length,
                                constraint.minLength(),
                                constraint.maxLength(),
                                formatValue(value)
                        )
                );
            }
        }

        return violations;
    }

    public static boolean isValid(EmployeeRecord record) {
        return validate(record).isEmpty();
    }

    public static boolean isValid(Map<String, Object> record) {
        return validate(record).isEmpty();
    }

    public static Map<String, LengthConstraint> getFieldLengthConstraints() {
        return FIELD_LENGTH_CONSTRAINTS;
    }

    private static String formatValue(Object value) {

        if (value instanceof String) {
            return "'" + value + "'";
        }

        return String.valueOf(value);
    }

    public record LengthConstraint(int minLength, int maxLength) {

        public boolean isValid(int length) {
            return length >= minLength && length <= maxLength;
        }
    }
}
