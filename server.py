# server.py
from flask import Flask, jsonify
from jattavagen_departures.service import get_upcoming_departures, format_departures

app = Flask(__name__)

@app.route('/departures', methods=['GET'])
def departures():
    try:
        deps = get_upcoming_departures()
        formatted = format_departures(deps)
        return jsonify(formatted), 200
    except Exception as e:
        # Log error here as needed
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
