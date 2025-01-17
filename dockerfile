# Use a minimal Python base image
FROM python:3.12-slim

# Create a non-root user and group for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies as root
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code into the container
COPY . /app

# Set up permissions for the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Define the default command to run the app
CMD ["python", "ai_recruiter.py"]
