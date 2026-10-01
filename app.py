import os
from flask import Flask, jsonify, request

app = Flask(__name__)

ADMIN_SECRET = "alpha_sidath_secret_123"

rollover_data = {
    "currentDay": 1,
    "totalOdds": 2.00,
    "isApproved": False,
    "matches": []
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Karibu kwenye Alpha & Sidath 30-Day Rollover API!"
    }), 200

@app.route('/api/rollover', methods=['GET'])
def get_rollover():
    if not rollover_data["isApproved"]:
        return jsonify({
            "status": "pending",
            "message": "Mkeka wa leo bado unahakikiwa na Alpha & Sidath..."
        }), 200

    return jsonify({
        "status": "success",
        "day": rollover_data["currentDay"],
        "totalOdds": rollover_data["totalOdds"],
        "matches": rollover_data["matches"]
    }), 200

@app.route('/api/admin/approve', methods=['POST'])
def approve_rollover():
    data = request.get_json()

    if not data or data.get("secretKey") != ADMIN_SECRET:
        return jsonify({"error": "Huruhusiwi kufanya kitendo hiki!"}), 401

    global rollover_data
    rollover_data = {
        "currentDay": data.get("day", 1),
        "totalOdds": data.get("totalOdds", 2.00),
        "isApproved": True,
        "matches": data.get("matches", [])
    }

    return jsonify({
        "message": f"Mkeka wa Siku ya {rollover_data['currentDay']} umethibitishwa kikamilifu!",
        "data": rollover_data
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
