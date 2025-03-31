import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import time
import json
from io import StringIO
import threading
import csv

from stock import Stock, runStock
from data import getData

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

SECURITY_KEY = "EricStiefel8"

progress_data = {}
results_data = {}  # Store results for each request

def run(tickers: list[str], request_id):
    """Function to process the ticker list and update progress."""
    have_winners: list[Stock] = []
    not_processed = []
    total_tickers = len(tickers)

    for i, tick in enumerate(tickers):
        try:
            put_ticks, strikes, bids, asks, exp_dates = getData(tick)
            stock = Stock(tick)
            runStock(stock, put_ticks, strikes, bids, asks, exp_dates)

            if stock.winners:
                have_winners.append(stock)

        except Exception as e:
            print(f"An error occurred while processing {tick}: {e}")
            not_processed.append(tick)

        progress = int((i + 1) / total_tickers * 100)
        progress_data[request_id] = progress

    progress_data[request_id] = 100
    results_data[request_id] = {"have_winners": [
        {
            "tick": stock.tick,
            "winners": [
                {
                    "put1": {
                        "strike": put1.strike,
                        "bid": put1.bid,
                        "ask": put1.ask,
                        "exp_date": put1.exp_date,
                    },
                    "put2": {
                        "strike": put2.strike,
                        "bid": put2.bid,
                        "ask": put2.ask,
                        "exp_date": put2.exp_date,
                    },
                    "midpoint": midpoint,
                    "yield": yield_val,
                }
                for put1, put2, midpoint, yield_val in stock.winners
            ],
        }
        for stock in have_winners
    ], "not_processed": not_processed}
    return have_winners, not_processed

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

            # Read the CSV file content
            csv_content = csv_file.stream.read().decode("utf-8")
            csv_reader = csv.reader(StringIO(csv_content))

            # Convert CSV data to a list of tickers (assuming first column)
            ticker_list = [row[0] for row in csv_reader if row]

            email_me = request.form.get('emailMe', 'false') == 'true'
            if email_me:
                email = request.form.get('email', '')

            # Generate a unique request ID
            request_id = str(time.time())

            # Initialize progress
            progress_data[request_id] = 0

            # Start the processing in a separate thread, passing request_id
            threading.Thread(target=run, args=(ticker_list, request_id)).start()

            return jsonify({
                'message': 'File received successfully',
                'request_id': request_id,  # return the request ID
            }), 200

        else:
            return jsonify({'error': 'custom_list must be true to upload a file'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/progress/<request_id>', methods=['GET'])
def progress(request_id):
    def generate():
        while True:
            progress_value = progress_data.get(request_id, 0)
            yield f"data: {json.dumps({'progress': progress_value})}\n\n"
            
            if progress_value == 100:
                break

            yield ": keep-alive\n\n"
            time.sleep(5) 
    return Response(generate(), mimetype='text/event-stream')


@app.route('/results/<request_id>', methods=['GET'])
def results(request_id):
    results = results_data.get(request_id)
    if results:
        return jsonify(results)
    else:
        return jsonify({"error": "Results not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
