# Use a standard, stable Python base image to maximize reliability
# This avoids issues with finding and downloading specific TensorFlow images
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container first to leverage Docker's layer caching
COPY requirements.txt .

# --- NEW: Upgrade pip to the latest version to ensure reliability ---
RUN pip install --upgrade pip

# Install the Python dependencies
# We now install tensorflow-cpu via pip, which is a very reliable method
# UPDATED timeout to 1800 seconds (30 minutes)
RUN pip install --no-cache-dir --timeout=1800 -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5000

# Define the command to run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

