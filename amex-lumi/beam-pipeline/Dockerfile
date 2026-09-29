FROM eclipse-temurin:17-jre

WORKDIR /opt/lumi

COPY target/lumi-beam-pipeline-1.0.0.jar /opt/lumi/lumi-beam-pipeline-1.0.0.jar

ENTRYPOINT ["java", "-Duser.timezone=UTC", "-jar", "/opt/lumi/lumi-beam-pipeline-1.0.0.jar"]
