package com.amexlumi.beam.security;

import com.amexlumi.beam.model.EmployeeRecord;
import com.macasaet.fernet.Key;
import com.macasaet.fernet.Token;

import java.util.LinkedHashMap;
import java.util.Map;

public final class FieldEncryptor {

    private static final String ENVIRONMENT_VARIABLE =
            "FIELD_ENCRYPTION_KEY";

    private final Key key;

    /**
     * Creates an encryptor using the FIELD_ENCRYPTION_KEY
     * environment variable.
     */
    public FieldEncryptor() {
        this(System.getenv(ENVIRONMENT_VARIABLE));
    }

    /**
     * Creates an encryptor using an explicitly supplied
     * Fernet key.
     *
     * This constructor is mainly useful for tests.
     */
    public FieldEncryptor(String keyValue) {

        if (keyValue == null || keyValue.isBlank()) {
            throw new IllegalStateException(
                    "FIELD_ENCRYPTION_KEY environment variable " +
                            "is missing or empty"
            );
        }

        try {
            this.key = new Key(keyValue.trim());
        } catch (RuntimeException exception) {
            throw new IllegalStateException(
                    "FIELD_ENCRYPTION_KEY is not a valid Fernet key",
                    exception
            );
        }
    }

    /**
     * Encrypts a plain-text value using Fernet.
     */
    public String encrypt(String plainText) {

        if (plainText == null) {
            return null;
        }

        return Token.generate(key, plainText).serialise();
    }

    /**
     * Encrypts an arbitrary value by converting it to text first.
     */
    public String encryptValue(Object value) {

        if (value == null) {
            return null;
        }

        return encrypt(String.valueOf(value));
    }

    /**
     * Encrypts the sensitive fields used by JSON/XML records.
     *
     * Fields:
     * - phone_number
     * - salary
     * - emergency_contact.phone
     */
    public EmployeeRecord encryptEmployeeRecord(
            EmployeeRecord employeeRecord) {

        if (employeeRecord == null) {
            throw new IllegalArgumentException(
                    "Employee record must not be null"
            );
        }

        Map<String, Object> encrypted =
                employeeRecord.toMap();

        encryptTopLevelField(
                encrypted,
                "phone_number"
        );

        encryptTopLevelField(
                encrypted,
                "salary"
        );

        encryptNestedPhone(
                encrypted
        );

        /*
         * CSV uses emergency_contact_phone as a flat field.
         */
        encryptTopLevelField(
                encrypted,
                "emergency_contact_phone"
        );

        return new EmployeeRecord(encrypted);
    }

    private void encryptTopLevelField(
            Map<String, Object> record,
            String fieldName) {

        if (!record.containsKey(fieldName)) {
            return;
        }

        Object value = record.get(fieldName);

        if (value == null) {
            return;
        }

        record.put(
                fieldName,
                encryptValue(value)
        );
    }

    @SuppressWarnings("unchecked")
    private void encryptNestedPhone(
            Map<String, Object> record) {

        Object emergencyContact =
                record.get("emergency_contact");

        if (!(emergencyContact instanceof Map<?, ?>)) {
            return;
        }

        Map<String, Object> contact =
                new LinkedHashMap<>(
                        (Map<String, Object>) emergencyContact
                );

        if (!contact.containsKey("phone")) {
            return;
        }

        Object phone =
                contact.get("phone");

        if (phone == null) {
            return;
        }

        contact.put(
                "phone",
                encryptValue(phone)
        );

        record.put(
                "emergency_contact",
                contact
        );
    }
}
