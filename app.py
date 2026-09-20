from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_data = {
    "distance": 0,
    "rain": False,
    "float": False,
    "alert": False
}

@app.route("/")
def home():
    return "Ari Flood Monitoring API is running!"

@app.route("/sensor-data")
def sensor_data():
    return jsonify(latest_data)

@app.route("/update", methods=["GET"])
def update_data():
    from flask import request

    distance = request.args.get("distance", type=float)
    rain = request.args.get("rain", default="false").lower() == "true"
    float_water = request.args.get("float", default="false").lower() == "true"

    if distance is not None:
        latest_data["distance"] = distance

    latest_data["rain"] = rain
    latest_data["float"] = float_water
    latest_data["alert"] = (
        latest_data["distance"] <= 5.0
        or rain
        or float_water
    )

    return jsonify({
        "status": "updated",
        "data": latest_data
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)