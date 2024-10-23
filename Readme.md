# Calendar Service

This is a simple calendar service application built with Python and Docker.

## Prerequisites

- Docker
- Docker Compose

## Building the Application

To build the Docker image for the application, run the following command:

```sh
docker-compose build
```

## Running the Application

To start the application, run the following command:

```sh
docker-compose up
```

This will start the application and make it available at `http://localhost:5000`.

## Stopping the Application

To stop the application, press `Ctrl+C` in the terminal where the application is running. Alternatively, you can run:

```sh
docker-compose down
```

## Using the Application

### Adding an Event

To add an event, send a `POST` request to `/events` with the event details in JSON format. For example:

```sh
curl -X POST http://localhost:5000/events -H "Content-Type: application/json" -d '{
  "description": "Test Event",
  "time": "2024-01-01T12:00:00"
}'
```

### Getting an Event

To get an event, send a `GET` request to `/events/{event_id}`. For example:

```sh
curl http://localhost:5000/events/1
```

## Running Tests

To run the tests, use the following command:

```sh
docker-compose run app python -m unittest discover -s tests
```

## Project Structure

```
.gitignore
docker-compose.yml
Dockerfile
Readme.md
requirements.txt
src/
    __init__.py
    app.py
    models.py
tests/
    __init__.py
    test_app.py
```

- `Dockerfile`: Defines the Docker image for the application.
- `docker-compose.yml`: Defines the Docker services for the application.
- `requirements.txt`: Lists the Python dependencies for the application.
- `src/`: Contains the application source code.
