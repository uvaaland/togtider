# server.py
import logging
from flask import Flask, jsonify, request
from jattavagen_departures.service import get_upcoming_departures, format_departures

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('togtider-server')

app = Flask(__name__)

@app.route('/departures', methods=['GET'])
def departures():
    """
    Endpoint to get departures from Jåttåvågen station.
    Returns JSON with northbound and southbound departures.
    """
    try:
        logger.info(f"Request received from {request.remote_addr}")
        deps = get_upcoming_departures()
        formatted = format_departures(deps)
        
        # Add metadata to the response
        response = {
            "data": formatted,
            "station": "Jåttåvågen",
            "timestamp": formatted.get("timestamp", None)
        }
        
        logger.info(f"Returning {sum(len(deps) for deps in formatted.values() if isinstance(deps, list))} departures")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error processing departure request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Failed to retrieve departure information",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    logger.info("Starting Togtider server on port 5001")
    app.run(host='127.0.0.1', port=5001, debug=False)
