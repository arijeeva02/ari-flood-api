from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(name)
CORS(app)

SENSOR DATA

latest_data = {
"distance": 0,
"rain": False,
"float": False,
"alert": False,
"sensor_available": False
}

HOME API

@app.route("/")
def home():
return "Ari Flood Monitoring API with FloodGuard AI is running!"

SENSOR DATA API

@app.route("/sensor-data")
def sensor_data():
return jsonify(latest_data)

UPDATE SENSOR DATA

@app.route("/update", methods=["GET"])
def update_data():
distance = request.args.get("distance", type=float)
rain = request.args.get("rain", default="false").lower() == "true"
float_water = request.args.get("float", default="false").lower() == "true"

if distance is not None:
    latest_data["distance"] = distance
    latest_data["rain"] = rain
    latest_data["float"] = float_water
    latest_data["alert"] = (
        distance <= 5.0 or rain or float_water
    )
    latest_data["sensor_available"] = True

return jsonify({
    "status": "updated",
    "data": latest_data
})

FREE FLOODGUARD AI CHATBOT

@app.route("/chat", methods=["POST"])
def chatbot():
try:
data = request.get_json(silent=True) or {}
message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"reply": "Please enter your question."}), 400

    message = message.lower().strip()
    sensor = latest_data.copy()

    if any(word in message for word in ["hello", "hi", "hey"]):
        reply = (
            "Hello! I am FloodGuard AI. I can help you with flood monitoring, "
            "water levels, rainfall, shelter information and emergency safety."
        )

    elif any(word in message for word in ["project", "system", "about"]):
        reply = (
            "Our project is an IoT-based Flood Detection, Shelter Occupancy "
            "Monitoring and Citizen Alert System. It uses ESP32, ultrasonic "
            "sensors, rain sensors, float sensors, GSM alerts, YOLOv5 person "
            "detection and a live dashboard."
        )

    elif any(word in message for word in [
        "shelter", "occupancy", "people", "doctor", "police"
    ]):
        reply = (
            "Demonstration shelter data: 26 occupants, including 21 civilians, "
            "3 doctors and 2 police personnel. This is sample data, not a live "
            "occupancy count."
        )

    elif any(word in message for word in ["rain", "rainfall"]):
        if not sensor["sensor_available"]:
            reply = (
                "Live rainfall information is currently unavailable because "
                "no sensor update has been received."
            )
        else:
            reply = (
                "Rain sensor status: "
                + ("Rain detected." if sensor["rain"] else "No rain detected.")
            )

    elif any(word in message for word in ["water", "level", "distance"]):
        if not sensor["sensor_available"]:
            reply = (
                "Live water-level readings are currently unavailable. "
                "Please check the ESP32 connection."
            )
        else:
            reply = (
                f"Current sensor distance: {sensor['distance']} cm. "
                + (
                    "High water-level warning!"
                    if sensor["distance"] <= 5.0
                    else "Water level is normal based on the configured threshold."
                )
            )

    elif any(word in message for word in ["flood", "alert", "status"]):
        if not sensor["sensor_available"]:
            reply = (
                "Live flood status is currently unavailable. "
                "No sensor update has been received."
            )
        else:
            reply = (
                "Flood monitoring status: "
                + (
                    "WARNING! Flood alert is active."
                    if sensor["alert"]
                    else "No flood alert is currently active."
                )
                + f" Water distance: {sensor['distance']} cm."
                + f" Rain: {'Detected' if sensor['rain'] else 'Not detected'}."
                + f" Float sensor: {'Water detected' if sensor['float'] else 'Normal'}."
            )

    elif any(word in message for word in [
        "emergency", "help", "danger", "safety"
    ]):
        reply = (
            "Emergency safety advice: Move to higher ground, avoid walking or "
            "driving through floodwater, keep your phone charged and follow "
            "official emergency instructions. Contact local emergency services "
            "if you are in danger."
        )

    else:
        reply = (
            "I am FloodGuard AI. Please ask me about flood status, water levels, "
            "rainfall, shelter occupancy, emergency safety or our project."
        )

    return jsonify({"reply": reply})

except Exception as e:
    print("Chatbot Error:", e)
    return jsonify({
        "reply": "Sorry! Something went wrong. Please try again."
    }), 500

if name == "main":
app.run(host="0.0.0.0", port=5000)
