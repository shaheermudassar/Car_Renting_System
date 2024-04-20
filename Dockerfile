# Use the official Python image from the DockerHub
FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHODONTWRITEBYTECODE 1

# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Install PostgreSQL server and client libraries
RUN apt-get update && apt-get install -y postgresql postgresql-contrib libpq-dev

# Create a volume for persistent PostgreSQL data
VOLUME /var/lib/postgresql/data

# Database credentials (**Not recommended for production due to security concerns**)
ENV POSTGRES_DB=DaisyRoomDjango
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=hangon1@
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432

# Copy initial database schema (if needed)
COPY ./localhost_dump.sql .

# Initialize and populate the database using PostgreSQL client
RUN psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB;" \
  && psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" < localdump.sql

# Expose the Django development port
EXPOSE 8000

# Create a volume for media files
VOLUME /app/media

# Start the Django development server with adjusted settings
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
