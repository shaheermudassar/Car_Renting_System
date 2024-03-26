# Use the official Python image from the DockerHub
FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHODONTWRITEBYTECODE 1

# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . ./app

RUN apt-get update
# Install any dependencies

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["sh", "./start.sh"]
# EXPOSE 8000

# ENTRYPOINT [ "gunicorn", "Car_Renting_System.wsgi:application" ]