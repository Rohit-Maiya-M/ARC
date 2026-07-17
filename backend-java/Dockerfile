# --- Stage 1: Build Phase (Updated to maven with JDK 21) ---
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

# Copy pom.xml and source configurations
COPY pom.xml .
COPY src ./src

# Compile and package the jar, skipping unit test validation loops to accelerate builds
RUN mvn clean package -DskipTests

# --- Stage 2: Runtime Execution Phase (Updated to JRE 21) ---
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

# Copy the compiled JAR artifact from the build layer
COPY --from=build /app/target/*.jar app.jar

# Expose Spring Boot's internal web server port
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]