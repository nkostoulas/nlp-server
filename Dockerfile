# Use the official Python image
FROM python:3.10-slim

# Unbuffered stdin/stderr
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py /app/
COPY secrets /app/secrets
COPY server /app/server

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app using Uvicorn
CMD ["python", "main.py"]

