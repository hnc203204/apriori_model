# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set environment variables (optional)
# ENV FLASK_ENV=development

# Expose port 5000 to the outside world
EXPOSE 5522

# Define the command to run the application
CMD ["python3", "server.py"]
