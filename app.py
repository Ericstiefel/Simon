import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time

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
def gather_data():
    """Receives CSV file, emailMe, and email values and returns them for confirmation."""
    try:
        if 'CSVfile' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        custom_list = request.form.get('custom_list', 'false') == 'true'
        if custom_list:
            csv_file = request.files['CSVfile']
        
        email_me = request.form.get('emailMe', 'false') == 'true'
        if email_me:
            email = request.form.get('email', '')
        
        return jsonify({
            'message': 'File received successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/progress')
def progress():
    def generate():
        for i in range(1, 101):
            time.sleep(1)  # Simulate a delay (e.g., processing)
            estimated_time_remaining = (100 - i) * 1  # Example calculation
            percentage_completion = i
            yield f"data: {jsonify({'progress': percentage_completion, 'time_remaining': estimated_time_remaining})}\n\n"

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
