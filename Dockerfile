# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
# COPY . .
# Copy all files from the src directory into the current working directory
COPY src/ .   


# Install Flask
RUN pip install Flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME CalendarService

# Run app.py when the container launches
CMD ["python", "app.py"]
