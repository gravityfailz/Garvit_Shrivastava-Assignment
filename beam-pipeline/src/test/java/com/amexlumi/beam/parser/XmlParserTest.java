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

class XmlParserTest {

    @Test
    void shouldParseActualSampleXml() throws Exception {

        Path sampleFile =
                Path.of(
                        "..",
                        "data","tests",
                        "xml_valid.xml"
                ).toAbsolutePath().normalize();

        Key testKey =
                Key.generateKey();

        FieldEncryptor encryptor =
                new FieldEncryptor(
                        testKey.serialise()
                );

        List<ParsedRecord> results =
                XmlParser.parse(
                        sampleFile,
                        encryptor
                );

        assertNotNull(results);

        assertFalse(
                results.isEmpty(),
                "Expected sample XML to produce records"
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

            /*
             * Verify salary is encrypted.
             */
            Object encryptedSalary =
                    employeeRecord.get("salary");

            assertNotNull(encryptedSalary);

            assertFalse(
                    encryptedSalary.toString().isBlank()
            );

            /*
             * XML stores emergency contact information
             * as a nested object:
             *
             * emergency_contact:
             *     phone
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
                    encryptedEmergencyPhone.toString().isBlank()
            );

            /*
             * Verify phone_number can actually be
             * decrypted using the test key.
             */
            String decryptedPhone =
                    Token.fromString(
                            encryptedPhone.toString()
                    ).validateAndDecrypt(
                            testKey,
                            new StringValidator() {
                            }
                    );

            /*
             * The XML sample may contain a different
             * phone number, so we only verify that the
             * encrypted value is a valid Fernet token.
             */
            assertNotNull(decryptedPhone);

            assertFalse(
                    decryptedPhone.isBlank()
            );

            /*
             * Verify salary can also be decrypted.
             */
            String decryptedSalary =
                    Token.fromString(
                            encryptedSalary.toString()
                    ).validateAndDecrypt(
                            testKey,
                            new StringValidator() {
                            }
                    );

            assertNotNull(decryptedSalary);

            assertFalse(
                    decryptedSalary.isBlank()
            );

            /*
             * Verify emergency contact phone can be
             * decrypted as well.
             */
            String decryptedEmergencyPhone =
                    Token.fromString(
                            encryptedEmergencyPhone.toString()
                    ).validateAndDecrypt(
                            testKey,
                            new StringValidator() {
                            }
                    );

            assertNotNull(
                    decryptedEmergencyPhone
            );

            assertFalse(
                    decryptedEmergencyPhone.isBlank()
            );

            break;
        }

        assertTrue(
                foundValidRecord,
                "Expected at least one valid XML employee record"
        );
    }
}
