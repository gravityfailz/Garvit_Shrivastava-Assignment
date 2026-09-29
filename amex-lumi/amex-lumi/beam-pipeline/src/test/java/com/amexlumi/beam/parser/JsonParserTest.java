package com.amexlumi.beam.parser;

import com.amexlumi.beam.model.EmployeeRecord;
import com.amexlumi.beam.model.ParsedRecord;
import com.amexlumi.beam.security.FieldEncryptor;
import com.macasaet.fernet.Key;
import com.macasaet.fernet.StringValidator;
import com.macasaet.fernet.Token;
import org.junit.jupiter.api.Test;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class JsonParserTest {

    @Test
    void shouldParseActualSampleEmployeeJson() throws Exception {

        Path filePath =
                Path.of(
                        "..",
                        "data",
                        "sample_employee.json"
                );

        Key testKey =
                Key.generateKey();

        FieldEncryptor encryptor =
                new FieldEncryptor(
                        testKey.serialise()
                );

        List<ParsedRecord> results =
                JsonParser.parse(
                        filePath,
                        encryptor
                );

        assertNotNull(results);

        assertFalse(
                results.isEmpty(),
                "Expected sample JSON to produce records"
        );

        boolean foundValidRecord = false;

        for (ParsedRecord result : results) {

            assertNotNull(result);

            if (!result.isValid()) {
                continue;
            }

            foundValidRecord = true;

            EmployeeRecord employeeRecord =
                    result.getEmployeeRecord();

            assertNotNull(employeeRecord);

            /*
             * Verify phone_number is encrypted.
             */
            Object encryptedPhone =
                    employeeRecord.get("phone_number");

            assertNotNull(encryptedPhone);

            assertFalse(
                    encryptedPhone.toString().isBlank()
            );

            assertFalse(
                    "9876500009".equals(
                            encryptedPhone.toString()
                    )
            );

            /*
             * Verify salary is encrypted.
             */
            Object encryptedSalary =
                    employeeRecord.get("salary");

            assertNotNull(encryptedSalary);

            assertFalse(
                    "700000".equals(
                            encryptedSalary.toString()
                    )
            );

            /*
             * Verify nested emergency contact phone
             * is encrypted.
             */
            Object emergencyContact =
                    employeeRecord.get(
                            "emergency_contact"
                    );

            assertNotNull(emergencyContact);

            assertTrue(
                    emergencyContact instanceof Map<?, ?>
            );

            Map<?, ?> contact =
                    (Map<?, ?>) emergencyContact;

            Object encryptedEmergencyPhone =
                    contact.get("phone");

            assertNotNull(
                    encryptedEmergencyPhone
            );

            assertFalse(
                    "9986500001".equals(
                            encryptedEmergencyPhone.toString()
                    )
            );

            /*
             * Verify that a non-sensitive field remains unchanged.
             */
            assertEquals(
                    "E000010",
                    employeeRecord.get("employee_id")
            );

            /*
             * Verify that the encrypted phone can actually
             * be decrypted using the same test key.
             */
            String decryptedPhone =
                    Token.fromString(
                            encryptedPhone.toString()
                    ).validateAndDecrypt(
                            testKey,
                            new StringValidator() {
                            }
                    );

            assertEquals(
                    "9876500009",
                    decryptedPhone
            );

            break;
        }

        assertTrue(
                foundValidRecord,
                "Expected at least one valid employee record"
        );
    }
}
