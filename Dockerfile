# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, including Graphviz
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Set Python path to include the root directory
ENV PYTHONPATH=/app

# Print directory contents for debugging
RUN echo "Contents of /app:" && ls -la

# Run wsgi.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:80", "wsgi:app"]