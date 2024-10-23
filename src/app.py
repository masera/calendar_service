from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import logging
import signal
import sys

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Default datetime format
datetime_format = "%Y-%m-%dT%H:%M:%S"

# Initialize SQLite database
db_file = "events.db"


def init_db():
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    time TEXT NOT NULL
                )
                """
            )
            conn.commit()
        logging.debug("Database initialized.")
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")


@app.before_request
def initialize_database():
    if not hasattr(app, "db_initialized"):
        init_db()
        app.db_initialized = True


@app.route("/events", methods=["POST"])
def add_event():
    event = request.get_json()
    description = event["description"]
    time = event["time"]
    logging.debug(f"Received event: {event}")
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO events (description, time) VALUES (?, ?)",
                (description, time),
            )
            conn.commit()  # Ensure data is written
            event_id = cursor.lastrowid
            logging.debug(f"Event added with ID: {event_id}")
        event["id"] = event_id
        return jsonify(event), 201
    except sqlite3.Error as e:
        logging.error(f"Failed to add event: {e}")
        return jsonify({"error": "Failed to add event"}), 500


@app.route("/events", methods=["GET"])
def get_events():
    dt_format = request.args.get("datetime_format", datetime_format)

    from_time_str = request.args.get("from_time")
    to_time_str = request.args.get("to_time")

    query = "SELECT id, description, time FROM events"
    params = []

    if from_time_str or to_time_str:
        query += " WHERE"
        if from_time_str:
            query += " time >= ?"
            params.append(from_time_str)
        if to_time_str:
            if from_time_str:
                query += " AND"
            query += " time <= ?"
            params.append(to_time_str)

    logging.debug(f"Executing query: {query} with params: {params}")

    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            logging.debug(f"Events fetched: {rows}")
        events = [
            {
                "id": row[0],
                "description": row[1],
                "time": datetime.strptime(row[2], datetime_format).strftime(dt_format),
            }
            for row in rows
        ]
        return jsonify(events)
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch events: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500


def signal_handler(sig, frame):
    print("Exiting gracefully")
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=5000, debug=True)
