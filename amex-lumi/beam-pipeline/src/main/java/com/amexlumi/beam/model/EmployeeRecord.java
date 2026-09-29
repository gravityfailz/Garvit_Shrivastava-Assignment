package com.amexlumi.beam.model;

import java.io.Serializable;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

public class EmployeeRecord implements Serializable {

    private static final long serialVersionUID = 1L;

    private final Map<String, Object> fields;

    public EmployeeRecord() {
        this.fields = new LinkedHashMap<>();
    }

    public EmployeeRecord(Map<String, Object> fields) {
        this.fields = new LinkedHashMap<>();

        if (fields != null) {
            this.fields.putAll(fields);
        }
    }

    public Map<String, Object> getFields() {
        return Collections.unmodifiableMap(fields);
    }

    public Object get(String fieldName) {
        return fields.get(fieldName);
    }

    public void put(String fieldName, Object value) {
        fields.put(fieldName, value);
    }

    public boolean containsField(String fieldName) {
        return fields.containsKey(fieldName);
    }

    public int size() {
        return fields.size();
    }

    public boolean isEmpty() {
        return fields.isEmpty();
    }

    public Map<String, Object> toMap() {
        return new LinkedHashMap<>(fields);
    }

    @Override
    public String toString() {
        return "EmployeeRecord{" +
                "fields=" + fields +
                '}';
    }
}
