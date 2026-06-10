from flask import Flask, request, jsonify
from datetime import datetime
from models import GeigerReading
from pydantic import ValidationError
from database import init_db, save_reading, cleanup_old_rows

app = Flask(__name__)


@app.route("/api/readings", methods=["POST"])
def add_reading():
    try:
        readings = GeigerReading(**request.get_json())
        readings.ensure_timestamp()

    except ValidationError as e:
        return jsonify({
            "error": "validation_error",
            "details": e.errors()
        }), 400
    
    save_reading(readings)
    cleanup_old_rows()

    return jsonify({
        "status": "ok",
        "saved": readings.model_dump_json()
    }), 201



if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)