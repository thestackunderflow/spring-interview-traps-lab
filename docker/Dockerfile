# Runtime for every episode: the jar is copied in, so `docker run` needs no bind mount (no host path in the capture).
FROM eclipse-temurin:21.0.12.1_1-jdk-noble@sha256:107215954359f1ab0be058a247d7c64ed6e69c71c1682d471d38ef751ec8e964
ARG JAR
COPY ${JAR} /app/app.jar
# exec form: java is PID 1; arguments after the image name go to the app (profile, --debug ...)
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
