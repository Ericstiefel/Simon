from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable cross-origin requests

app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

# API endpoint to receive data and compute future value
@app.route('/compute_fv', methods=['POST'])
def compute_fv():
    try:
        # Parse JSON data sent from frontend
        data = request.json
        pv = float(data.get('pv'))
        rate = float(data.get('rate')) / 100
        years = int(data.get('years'))
        
        # Compute Future Value (FV)
        fv = pv * (1 + rate) ** years
        
        # Send response back to frontend
        return jsonify({'fv': fv})

    except (ValueError, TypeError, KeyError):
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Run backend at http://127.0.0.1:5000/
