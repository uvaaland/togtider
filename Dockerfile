FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Create a non-root user to run the app
RUN groupadd -r togtider && \
    useradd -r -g togtider -d /app togtider && \
    chown -R togtider:togtider /app

USER togtider

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["python", "server.py"]
