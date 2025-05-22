from polygon.rest import RESTClient
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from random import uniform
from datetime import datetime, timedelta


# Import API key from environment variables
load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def getData(ticker: str):
    def fetch_quote(contract):
            try:
                sleep(uniform(0.05, 0.2))  # Stagger to avoid burst
                quote = client.get_last_quote(contract.ticker)
                if quote and quote.bid_price > 0:
                    return (contract, quote)
            except Exception as e:
                print(f"Error getting quote for {contract.ticker}: {e}")
            return None


    client = RESTClient(POLYGON_API_KEY)

    put_ticks, strikes, bids, asks, exp_date = [], [], [], [], []

    earliest = (datetime.today() + timedelta(days=61)).strftime("%Y-%m-%d")
    future_date = (datetime.today() + timedelta(days=270)).strftime("%Y-%m-%d") 

    curr_stock = client.get_last_quote(ticker)
    
    curr_price = curr_stock.ask_price
    
    pct_barrier = 0.2

    max_b = (1+pct_barrier)*curr_price

    try:
        contracts = list(client.list_options_contracts(
            underlying_ticker=ticker,
            contract_type="put",
            expiration_date_gte=earliest,
            expiration_date_lte=future_date,
            strike_price_lt=max_b
        ))

        print(f"🔢 Length of contracts: {len(contracts)}")

        

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(fetch_quote, c) for c in contracts]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    contract, quote = result
                    put_ticks.append(contract.ticker)
                    bids.append(quote.bid_price)
                    asks.append(quote.ask_price)
                    strikes.append(contract.strike_price)
                    exp_date.append(contract.expiration_date)

    except Exception as e:
        print(f"An error occurred: {e}")

    return put_ticks, strikes, bids, asks, exp_date