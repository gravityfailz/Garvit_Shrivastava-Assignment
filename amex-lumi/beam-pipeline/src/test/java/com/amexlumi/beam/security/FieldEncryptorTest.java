package com.amexlumi.beam.security;

import com.amexlumi.beam.model.EmployeeRecord;
import com.macasaet.fernet.Key;
import com.macasaet.fernet.Token;
import com.macasaet.fernet.StringValidator;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class FieldEncryptorTest {

    @Test
    void shouldEncryptAndDecryptValue() {

        Key testKey = Key.generateKey();

        FieldEncryptor encryptor =
                new FieldEncryptor(
                        testKey.serialise()
                );

        String original =
                "9876543210";

        String encrypted =
                encryptor.encrypt(original);

        assertNotNull(encrypted);

        assertFalse(
                encrypted.isBlank()
        );

        assertNotEquals(
                original,
                encrypted
        );

        String decrypted =
                Token.fromString(encrypted)
                        .validateAndDecrypt(
                                testKey,
                                new StringValidator() {
                                }
                        );

        assertEquals(
                original,
                decrypted
        );
    }

    @Test
    void shouldEncryptConfiguredEmployeeFields() {

        Key testKey = Key.generateKey();

        FieldEncryptor encryptor =
                new FieldEncryptor(
                        testKey.serialise()
                );

        Map<String, Object> emergencyContact =
                new HashMap<>();

        emergencyContact.put(
                "phone",
                "9876543210"
        );

        emergencyContact.put(
                "name",
                "Emergency Contact"
        );

        Map<String, Object> fields =
                new HashMap<>();

        fields.put(
                "employee_id",
                "EMP1001"
        );

        fields.put(
                "phone_number",
                "9876543210"
        );

        fields.put(
                "salary",
                "75000"
        );

        fields.put(
                "emergency_contact",
                emergencyContact
        );

        EmployeeRecord original =
                new EmployeeRecord(fields);

        EmployeeRecord encrypted =
                encryptor.encryptEmployeeRecord(
                        original
                );

        assertEquals(
                "EMP1001",
                encrypted.get("employee_id")
        );

        assertNotEquals(
                "9876543210",
                encrypted.get("phone_number")
        );

        assertNotEquals(
                "75000",
                encrypted.get("salary")
        );

        Map<?, ?> encryptedContact =
                (Map<?, ?>) encrypted.get(
                        "emergency_contact"
                );

        assertNotEquals(
                "9876543210",
                encryptedContact.get("phone")
        );

        assertEquals(
                "Emergency Contact",
                encryptedContact.get("name")
        );
    }
}
