package com.amexlumi.beam.parser;

import com.amexlumi.beam.model.EmployeeRecord;
import com.amexlumi.beam.model.ParsedRecord;
import com.amexlumi.beam.security.FieldEncryptor;
import com.amexlumi.beam.validation.EmployeeValidator;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class XmlParser {

    private XmlParser() {
        // Utility class.
    }

    /**
     * Production entry point.
     *
     * Uses FIELD_ENCRYPTION_KEY from the environment.
     */
    public static List<ParsedRecord> parse(Path filePath)
            throws IOException {

        FieldEncryptor encryptor =
                new FieldEncryptor();

        return parse(filePath, encryptor);
    }

    /**
     * Testable entry point.
     *
     * Allows tests to provide a temporary Fernet key.
     */
    public static List<ParsedRecord> parse(
            Path filePath,
            FieldEncryptor encryptor)
            throws IOException {

        if (filePath == null) {
            throw new IllegalArgumentException(
                    "XML file path must not be null"
            );
        }

        if (encryptor == null) {
            throw new IllegalArgumentException(
                    "FieldEncryptor must not be null"
            );
        }

        if (!Files.exists(filePath)) {
            throw new IOException(
                    "XML source file does not exist: " + filePath
            );
        }

        if (!Files.isRegularFile(filePath)) {
            throw new IOException(
                    "XML source path is not a regular file: " + filePath
            );
        }

        try (InputStream inputStream =
                     Files.newInputStream(filePath)) {

            DocumentBuilderFactory factory =
                    DocumentBuilderFactory.newInstance();

            configureSecureXml(factory);

            DocumentBuilder builder =
                    factory.newDocumentBuilder();

            Document document =
                    builder.parse(inputStream);

            document.getDocumentElement().normalize();

            Element root =
                    document.getDocumentElement();

            if (root == null) {
                throw new IOException(
                        "XML document does not contain a root element"
                );
            }

            return parseRecords(
                    root,
                    encryptor
            );

        } catch (IOException exception) {
            throw exception;

        } catch (Exception exception) {
            throw new IOException(
                    "Unable to parse XML source file: " + filePath,
                    exception
            );
        }
    }

    private static List<ParsedRecord> parseRecords(
            Element root,
            FieldEncryptor encryptor) {

        List<ParsedRecord> results =
                new ArrayList<>();

        NodeList recordNodes =
                root.getElementsByTagName("record");

        for (int i = 0;
             i < recordNodes.getLength();
             i++) {

            Node node =
                    recordNodes.item(i);

            if (!(node instanceof Element recordElement)) {
                continue;
            }

            Map<String, Object> rawRecord =
                    elementToMap(recordElement);

            /*
             * Validate the original XML values first.
             */
            List<String> violations =
                    EmployeeValidator.validate(rawRecord);

            if (!violations.isEmpty()) {

                /*
                 * Keep invalid records unencrypted.
                 */
                results.add(
                        ParsedRecord.error(
                                rawRecord,
                                violations
                        )
                );

                continue;
            }

            /*
             * Preserve the existing XML normalization behavior.
             */
            Map<String, Object> normalizedRecord =
                    normalizeRecord(rawRecord);

            EmployeeRecord employeeRecord =
                    new EmployeeRecord(
                            normalizedRecord
                    );

            /*
             * Encrypt sensitive fields only after
             * validation and normalization.
             *
             * FieldEncryptor handles:
             *
             * phone_number
             * salary
             * emergency_contact.phone
             * emergency_contact_phone
             */
            EmployeeRecord encryptedRecord =
                    encryptor.encryptEmployeeRecord(
                            employeeRecord
                    );

            results.add(
                    ParsedRecord.valid(
                            encryptedRecord
                    )
            );
        }

        return results;
    }

    private static Map<String, Object> elementToMap(
            Element element) {

        Map<String, Object> result =
                new LinkedHashMap<>();

        NodeList children =
                element.getChildNodes();

        for (int i = 0;
             i < children.getLength();
             i++) {

            Node child =
                    children.item(i);

            if (child.getNodeType()
                    != Node.ELEMENT_NODE) {
                continue;
            }

            Element childElement =
                    (Element) child;

            String fieldName =
                    childElement.getTagName();
//Detect nested elements
            if (hasElementChildren(childElement)) {

                result.put(
                        fieldName,
                        elementToMap(childElement)
                );

            } else {

                result.put(
                        fieldName,
                        childElement.getTextContent()
                );
            }
        }

        return result;
    }

    private static boolean hasElementChildren(
            Element element) {

        NodeList children =
                element.getChildNodes();

        for (int i = 0;
             i < children.getLength();
             i++) {

            if (children.item(i).getNodeType()
                    == Node.ELEMENT_NODE) {

                return true;
            }
        }

        return false;
    }

    private static Map<String, Object> normalizeRecord(
            Map<String, Object> rawRecord) {

        Map<String, Object> normalized =
                new LinkedHashMap<>();

        for (Map.Entry<String, Object> entry :
                rawRecord.entrySet()) {

            Object value =
                    entry.getValue();

            if (value == null) {

                normalized.put(
                        entry.getKey(),
                        " "
                );

            } else if (value instanceof String
                    && ((String) value).isEmpty()) {

                normalized.put(
                        entry.getKey(),
                        " "
                );

            } else if (value instanceof Map<?, ?> nestedMap) {

                normalized.put(
                        entry.getKey(),
                        normalizeNestedMap(nestedMap)
                );

            } else {

                normalized.put(
                        entry.getKey(),
                        value
                );
            }
        }

        return normalized;
    }

    private static Map<String, Object> normalizeNestedMap(
            Map<?, ?> nestedMap) {

        Map<String, Object> normalized =
                new LinkedHashMap<>();

        for (Map.Entry<?, ?> entry :
                nestedMap.entrySet()) {

            String key =
                    String.valueOf(entry.getKey());

            Object value =
                    entry.getValue();

            if (value == null) {

                normalized.put(
                        key,
                        " "
                );

            } else if (value instanceof String
                    && ((String) value).isEmpty()) {

                normalized.put(
                        key,
                        " "
                );

            } else if (value instanceof Map<?, ?> nested) {

                normalized.put(
                        key,
                        normalizeNestedMap(nested)
                );

            } else {

                normalized.put(
                        key,
                        value
                );
            }
        }

        return normalized;
    }

    /**
     * Configure the XML parser to prevent XXE attacks.
     */
    private static void configureSecureXml(
            DocumentBuilderFactory factory)
            throws Exception {

        factory.setFeature(
                "http://apache.org/xml/features/disallow-doctype-decl",
                true
        );

        factory.setFeature(
                "http://xml.org/sax/features/external-general-entities",
                false
        );

        factory.setFeature(
                "http://xml.org/sax/features/external-parameter-entities",
                false
        );

        factory.setFeature(
                "http://apache.org/xml/features/nonvalidating/load-external-dtd",
                false
        );

        factory.setXIncludeAware(false);

        factory.setExpandEntityReferences(false);
    }
}
