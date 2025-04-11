# webhook_server.py

from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/trigger', methods=['POST'])
def trigger_app():
    try:
        # Run app.py in the background
        subprocess.Popen(['python3', 'app.py'])
        return 'Triggered app.py', 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
