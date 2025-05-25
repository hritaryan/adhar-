from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

otp_store = {}
FAST2SMS_API_KEY = "YOUR_API_KEY_HERE"  # <-- Put your real key

def send_sms_otp(mobile, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "variables_values": otp,
        "route": "otp",
        "numbers": mobile
    }
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    aadhaar = data.get("aadhaar")

    if not aadhaar or len(aadhaar) != 12 or not aadhaar.isdigit():
        return jsonify({"status": "error", "message": "Invalid Aadhaar number"}), 400

    mobile = "9999999999"  # Change to your test number added in Fast2SMS contacts
    otp = "123456"
    otp_store[aadhaar] = otp
    result = send_sms_otp(mobile, otp)

    if result.get("return"):
        return jsonify({"status": "success", "message": "OTP sent successfully."})
    else:
        return jsonify({"status": "error", "message": "Failed to send OTP."}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    aadhaar = data.get("aadhaar")
    otp = data.get("otp")

    if otp_store.get(aadhaar) == otp:
        return jsonify({"status": "success", "message": "OTP verified successfully"})
    else:
        return jsonify({"status": "error", "message": "Invalid OTP"}), 400

if __name__ == '__main__':
    app.run(debug=True)
