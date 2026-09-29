package com.amexlumi.ingestion.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties(prefix = "lumi")
public class LumiProperties {

    private String postgresDsn;

    public String getPostgresDsn() { return postgresDsn; }
    public void setPostgresDsn(String postgresDsn) { this.postgresDsn = postgresDsn; }
}
