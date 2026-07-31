# ----------------------------------------------------
# Stage 1 : Build
# ----------------------------------------------------
FROM maven:3.9.6-eclipse-temurin-21 AS build

WORKDIR /app

# Copy only pom.xml first
COPY pom.xml .

# Download and cache Maven dependencies
RUN mvn dependency:go-offline

# Copy source code only after dependencies are cached
COPY src ./src

# Build application
RUN mvn clean package -DskipTests

# ----------------------------------------------------
# Stage 2 : Runtime
# ----------------------------------------------------
FROM eclipse-temurin:21-jre-jammy

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]