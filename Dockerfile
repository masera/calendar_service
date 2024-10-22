# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run gunicorn server when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
