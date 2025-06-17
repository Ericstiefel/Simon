from io import StringIO
import os
import threading
import csv
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from stock import Stock, runStock
from data import getData
from Email import email
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  


SECURITY_KEY = 'Simon'

progress_data = {}
results_data = {}  # Store results for each request

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@app.route('/authenticate', methods=['POST', 'OPTIONS'])
def authenticate():
    if request.method == 'OPTIONS':
        # CORS preflight
        return jsonify({'status': 'OK'}), 200

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

            csv_content = csv_file.stream.read().decode("utf-8")
            csv_reader = csv.reader(StringIO(csv_content))

            ticker_list = [row[0] for row in csv_reader if row]

            email_me = request.form.get('emailMe', 'false') == 'true'
            if email_me:
                email_address = request.form.get('email', '')
            else:
                email_address = None

            request_id = str(time.time()) 
            progress_data[request_id] = 0

            threading.Thread(target=run, args=(ticker_list, request_id, email_address)).start()

            return jsonify({
                'message': 'File received successfully',
                'request_id': request_id,  
            }), 200

        else:
            return jsonify({'error': 'custom_list must be true to upload a file'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/progress/<request_id>', methods=['GET'])
def progress(request_id):
    progress_value = progress_data.get(request_id, 0)
    return jsonify({'progress': progress_value})

@app.route('/results/<request_id>', methods=['GET'])
def results(request_id):
    results = results_data.get(request_id)
    if results:
        return jsonify(results)
    else:
        return jsonify({"error": "Results not found"}), 404
    
def run(tickers: list[str], request_id, email_address=None):
    """Function to process the ticker list and update progress."""
    have_winners: list[Stock] = []
    not_processed = []
    total_tickers = len(tickers)

    for i, tick in enumerate(tickers):
        try:
            stock = Stock(tick)
            put_ticks, strikes, bids, asks, exp_dates = getData(stock) 
            
            runStock(stock, put_ticks, strikes, bids, asks, exp_dates) 

            if stock.winners:
                have_winners.append(stock)

        except Exception as e:
            print(f"An error occurred while processing {tick}: {e}")
            not_processed.append(tick)

        progress = int((i + 1) / total_tickers * 100)
        progress_data[request_id] = progress

    progress_data[request_id] = 101 

    final_results = []
    for stock in have_winners:
        processed_winners_list = []
        
        for put1, put2, midpoint, yield_val, max_loss in stock.winners:
            processed_winners_list.append({
                "put1": {
                    "strike": put1.strike,
                    "bid": put1.bid,
                    "ask": put1.ask,
                    "exp_date": put1.exp_date,
                    "tick": put1.tick,
                },
                "put2": {
                    "strike": put2.strike,
                    "bid": put2.bid,
                    "ask": put2.ask,
                    "exp_date": put2.exp_date,
                    "tick": put2.tick
                },
                "midpoint": midpoint,
                "yield": yield_val,
                "Max_Loss": max_loss,
            })
        
        stock_results = {
            "tick": stock.tick,
            "price": stock.price, 
            "winners": processed_winners_list
        }
        final_results.append(stock_results)

        # If email is enabled, send an email per ticker (only for actual winners)
        if email_address and stock.winners:
            full_body = "\n\n".join(
                f"Put1: Strike {put1.strike}, Bid {put1.bid}, Ask {put1.ask}, Exp {put1.exp_date}, Tick {put1.tick}\n"
                f"Put2: Strike {put2.strike}, Bid {put2.bid}, Ask {put2.ask}, Exp {put2.exp_date}, Tick {put2.tick}\n"
                f"Max Loss: {max_loss}, Midpoint: {midpoint}, Yield: {yield_val}"
                for put1, put2, midpoint, yield_val, max_loss in stock.winners
            )
            full_body = f"Stock: {stock.tick}\n\n{full_body}"
            email(address=email_address, subject=stock.tick, body=full_body)

        
    results_data[request_id] = {"have_winners": final_results, "not_processed": not_processed}
    return have_winners, not_processed 

    
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)
    print(run(['NIO', 'PEP'], time.time()))


