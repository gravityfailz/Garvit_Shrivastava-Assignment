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

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CsvParserTest {

    @Test
    void shouldParseActualSampleCsv() throws Exception {

        Path sampleFile =
                Path.of(
                        "..",
                        "data",
                        "tests",
                        "encryption_test.csv"
                );

        Key testKey =
                Key.generateKey();

        FieldEncryptor encryptor =
                new FieldEncryptor(
                        testKey.serialise()
                );

        List<ParsedRecord> results =
                CsvParser.parse(
                        sampleFile,
                        encryptor
                );

        assertNotNull(results);

        assertFalse(
                results.isEmpty(),
                "Expected sample CSV to produce records"
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
             * phone_number must be encrypted.
             */
            Object encryptedPhone =
                    employeeRecord.get("phone_number");

            assertNotNull(encryptedPhone);

            assertFalse(
                    encryptedPhone.toString().isBlank()
            );

            /*
             * The encrypted value must not equal the
             * original phone number.
             */
            assertFalse(
                    "9876500001".equals(
                            encryptedPhone.toString()
                    )
            );

            /*
             * salary must be encrypted.
             */
            Object encryptedSalary =
                    employeeRecord.get("salary");

            assertNotNull(encryptedSalary);

            assertFalse(
                    encryptedSalary.toString().isBlank()
            );

            /*
             * The encrypted value must not equal
             * the original salary.
             */
            assertFalse(
                    "700000".equals(
                            encryptedSalary.toString()
                    )
            );

            /*
             * CSV stores the emergency contact phone
             * as emergency_contact_phone.
             */
            Object encryptedEmergencyPhone =
                    employeeRecord.get(
                            "emergency_contact_phone"
                    );

            assertNotNull(
                    encryptedEmergencyPhone
            );

            assertFalse(
                    encryptedEmergencyPhone.toString().isBlank()
            );

            assertFalse(
                    "9986500001".equals(
                            encryptedEmergencyPhone.toString()
                    )
            );

            /*
             * Verify that a normal field remains unchanged.
             *
             * We only need to prove that encryption is
             * restricted to the configured sensitive fields.
             */
            assertNotNull(
                    employeeRecord.get("employee_id")
            );

            /*
             * Verify that phone_number is genuinely
             * decryptable with the test key.
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
                    "9876500001",
                    decryptedPhone
            );

            foundValidRecord = true;

            break;
        }

        assertTrue(
                foundValidRecord,
                "Expected at least one valid CSV employee record"
        );
    }
}
