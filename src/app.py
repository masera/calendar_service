from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

events = {}

# Default datetime format
datetime_format = "%Y-%m-%dT%H:%M:%S"


@app.route("/events", methods=["POST"])
def add_event():
    event = request.get_json()
    event_id = len(events) + 1
    event["id"] = event_id
    events[event_id] = event
    return jsonify(event), 201


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    dt_format = request.args.get("datetime_format", datetime_format)
    if event_id in events:
        event = events[event_id]
        event["time"] = datetime.strptime(event["time"], datetime_format).strftime(
            dt_format
        )
        return jsonify(event)
    else:
        return jsonify({"error": "Event not found"}), 404


@app.route("/events", methods=["GET"])
def get_events():
    dt_format = request.args.get("datetime_format", datetime_format)
    from_time = request.args.get("from_time", datetime.now().strftime(datetime_format))
    to_time = request.args.get("to_time", datetime.now().strftime(datetime_format))

    from_time = datetime.strptime(from_time, dt_format)
    to_time = datetime.strptime(to_time, dt_format)

    result = [
        event
        for event in events.values()
        if from_time <= datetime.strptime(event["time"], datetime_format) <= to_time
    ]
    for event in result:
        event["time"] = datetime.strptime(event["time"], datetime_format).strftime(
            dt_format
        )

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
