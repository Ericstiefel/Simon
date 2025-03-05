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
    """Receives CSV file, emailMe, and email values and returns them for confirmation."""
    try:
        if 'CSVfile' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        csv_file = request.files['CSVfile']
        if csv_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        email_me = request.form.get('emailMe', 'false') == 'true'
        email = request.form.get('email', '')

        # Save file (optional)
        csv_file.save(os.path.join("uploads", csv_file.filename))

        return jsonify({
            'message': 'File received successfully',
            'filename': csv_file.filename,
            'emailMe': email_me,
            'email': email
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
