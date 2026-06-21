FROM postgres:15-alpine

ENV POSTGRES_USER=course_user
ENV POSTGRES_PASSWORD=course_pass
ENV POSTGRES_DB=course_db

COPY database.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
