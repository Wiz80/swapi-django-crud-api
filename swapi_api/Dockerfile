# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing pyc files to disk
ENV PYTHONUNBUFFERED 1         # Prevent Python from buffering stdout and stderr

# Set the working directory
WORKDIR /app

# Install netcat-openbsd for database readiness checks
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Expose the port that Django will run on
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run Gunicorn instead of Django's development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
