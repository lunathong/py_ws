# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables for non-buffered output, which is good for viewing logs
ENV PYTHONUNBUFFERED 1

# Install any OS dependencies if needed (e.g., for some Python packages)
# RUN apt-get update && apt-get install -y \
#    libpq-dev \
#    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current project directory into the container's working directory
COPY . .

# Expose the port your application runs on (e.g., 8000 for Django/FastAPI/Flask)
EXPOSE 5000

# Define the command to run your application (Replace with your actual startup command)
# Example for a simple Flask app:
CMD ["python", "app.py"]

# Example for a Gunicorn server (common for production):
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]
# or
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_app:create_app()"]