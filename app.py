from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets  # Used to generate session tokens

app = Flask(__name__)
CORS(app)

SECURITY_KEY = "EricStiefel8"
ACTIVE_TOKENS = set()  # Stores session tokens

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate user and return a session token."""
    data = request.json

    print("Received Data:", data)

    
    if not data or data.get("securityKey") != SECURITY_KEY:
        return jsonify({"error": "Unauthorized access"}), 403

    # Generate a secure session token
    token = secrets.token_hex(16)
    ACTIVE_TOKENS.add(token)
    
    return jsonify({"token": token})

@app.route('/compute_fv', methods=['POST'])
def compute_fv():
    """Compute FV only if the user has a valid session token."""
    data = request.json
    token = data.get("token")

    if token not in ACTIVE_TOKENS:
        return jsonify({"error": "Invalid session"}), 403  # Access denied

    try:
        pv = float(data.get('pv'))
        rate = float(data.get('rate')) / 100
        years = int(data.get('years'))

        fv = pv * (1 + rate) ** years
        return jsonify({'fv': fv})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
