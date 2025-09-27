# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python scripts
COPY *.py /app/

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME AgentTools

# Make the script executable
RUN chmod +x /app/process_agents.py

# Default command (can be overridden)
ENTRYPOINT ["python", "process_agents.py"]

# Default arguments (show help)
CMD ["--help"]
