from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
import logging

app = Flask(__name__)

events_file = "events.json"

# Default datetime format
datetime_format = "%Y-%m-%dT%H:%M:%S"

# Load events from file if it exists
if os.path.exists(events_file):
    with open(events_file, "r") as f:
        events = json.load(f)
else:
    events = {}


@app.route("/events", methods=["POST"])
def add_event():
    event = request.get_json()
    event_id = len(events) + 1
    event["id"] = event_id
    events[event_id] = event

    # Save the events to a file
    with open(events_file, "w") as f:
        json.dump(events, f)

    return jsonify(event), 201


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    dt_format = request.args.get("datetime_format", datetime_format)
    if event_id in events:
        event = events[event_id]
        event_time = datetime.strptime(event["time"], datetime_format).strftime(
            dt_format
        )
        event["time"] = event_time
        return jsonify(event)
    else:
        return jsonify({"error": "Event not found"}), 404


@app.route("/events", methods=["GET"])
def get_events():
    dt_format = request.args.get("datetime_format", datetime_format)

    if "from_time" in request.args:
        from_time_str = request.args.get("from_time")
    else:
        from_time_str = (
            datetime.now()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .strftime(datetime_format)
        )

    if "to_time" in request.args:
        to_time_str = request.args.get("to_time")
    else:
        to_time_str = datetime.now().strftime(datetime_format)

    from_time = datetime.strptime(from_time_str, dt_format)
    to_time = datetime.strptime(to_time_str, dt_format)
    logging.debug(f"From time: {from_time_str}, To time: {to_time_str}")

    result = []
    for event in events.values():
        event_time = datetime.strptime(event["time"], datetime_format)
        logging.debug(f"Event time: {event_time}")
        if from_time <= event_time <= to_time:
            event["time"] = event_time.strftime(dt_format)
            result.append(event)
    logging.debug(f"Filtered events: {result}")
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
