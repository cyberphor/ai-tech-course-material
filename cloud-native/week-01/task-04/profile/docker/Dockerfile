#TODO: Fill me in!
FROM maven:3.8.4-openjdk-17-slim

LABEL Author="Victor Fernandez III, @cyberphor"

WORKDIR /opt/cloudchat/

COPY src src

COPY pom.xml pom.xml

RUN mvn clean package

ENTRYPOINT [ "java", "-jar", "target/profile-0.1.0.jar" ]