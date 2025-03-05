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

    return jsonify(True)

@app.route('/compute_fv', methods=['POST'])
def compute_fv():
    """Compute FV only if the user has a valid session token."""
    data = request.json

    try:
        pv = float(data.get('pv'))
        rate = float(data.get('rate')) / 100
        years = int(data.get('years'))

        fv = pv * (1 + rate) ** years
        return jsonify({'fv': fv})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
