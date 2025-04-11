from polygon.rest import RESTClient
from dotenv import load_dotenv
import os

# Import API key from environment variables
load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
def getData(ticker: str):

    client = RESTClient((POLYGON_API_KEY))

    put_ticks, strikes, bids, asks, exp_date = [], [], [], [], []

    try:
        contracts = client.list_options_contracts(underlying_ticker=ticker)

        if contracts:
            for contract in contracts:
                if contract.contract_type == 'put':
                    try:
                        quote = client.get_last_quote(contract.ticker)
                        if quote and quote.bid_price > 0:
                            put_ticks.append(contract.ticker)
                            bids.append(quote.bid_price)
                            asks.append(quote.ask_price)
                            strikes.append(contract.strike_price)
                            exp_date.append(contract.expiration_date)

                    except Exception as quote_error:
                        print(f"Error getting quote for {contract.ticker}: {quote_error}")
        else:
            print(f"No option contracts found for {ticker}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return (put_ticks, strikes, bids, asks, exp_date)
