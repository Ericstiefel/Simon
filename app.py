import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

SECURITY_KEY = "EricStiefel8"

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    
    if not data or data.get("securityKey") != SECURITY_KEY:
        return jsonify({"error": "Unauthorized access"}), 403

    return jsonify({"message": "Authentication successful"}), 200

@app.route('/findOptions', methods=['POST'])
def find_options():
    """Receives emailMe and email values and returns them for confirmation."""
    data = request.json

    try:
        email_me = data.get('emailMe', False)
        email = data.get('email', '')

        return jsonify({'emailMe': email_me, 'email': email}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
