from datetime import date
import datetime
from dotenv import load_dotenv
import os
from polygon.rest import RESTClient
import math

class Put:
    def __init__(self, strike: int, bid: float, ask: float, exp_date: int, tick):
        self.strike = strike
        self.bid = bid
        self.ask = ask
        self.exp_date = exp_date
        self.tick = tick

class Stock:
    def __init__(self, tick: str):
        """
        Invalid if:
            >9 mo out
            negative midpoint
            bid = 0
            same strike        
        """
        load_dotenv()
        POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
        self.tick = tick
        self.puts: list[Put] = []
        self.yld = [i for i in range(6, 11)] #yield values 6-10
        self.winners: list[tuple[Put, Put, float, int, float]] = [] #P1, P2, Midpoint, Yield, Max Loss
        client = RESTClient(POLYGON_API_KEY)
        stock = client.get_last_quote(self.tick)
        self.price = stock.ask_price

    @staticmethod
    def days_until(date_str: str): 
        date_object = datetime.datetime.strptime(date_str, "%m/%d/%y").date() 
        today = datetime.date.today()
        return (date_object - today).days

    @staticmethod
    def midpoint(P1_bid: float, P1_ask: float, P2_bid: float, P2_ask: float) -> float:
        aggresive = -P1_bid + P2_ask
        conservative = -P1_ask + P2_bid
        return round((aggresive + conservative) / 2, 3)
    
    @staticmethod
    def validCompare(p1: Put, p2: Put, max_strike_split: float = .25) -> bool:
        strike_diff: bool = abs((p1.strike - p2.strike) / p2.strike) < max_strike_split
        return (p1 != p2) and (p1.exp_date == p2.exp_date) and (p1.strike != p2.strike) and strike_diff
    
    @staticmethod
    def maxLoss(p1: Put, p2: Put, midpoint: float) -> float:
        k1, k2 = p1.strike, p2.strike
        return round((abs(k1 - k2) - midpoint) / max(k1, k2), 4)

    def evaluate(self, p1: Put, p2: Put, cap_loss: float = 0.1):
        exp = p1.exp_date
        days_out = self.days_until(exp)

        midpoint = self.midpoint(p1.bid, p1.ask, p2.bid, p2.ask)
        if midpoint <= 0:
            return
        
        max_loss = self.maxLoss(p1, p2, midpoint)

        if max_loss > cap_loss:
            return

        for y in reversed(self.yld):
            score = (y/36500)*days_out*max(p1.strike, p2.strike)
            if score < midpoint:
                self.winners.append((p1, p2, midpoint, y, max_loss))
                return

    def populate_winners(self) -> None:
        seen = set()
        for p1_idx in range(len(self.puts)):
            for p2_idx in range(p1_idx, len(self.puts)):
                p1, p2 = self.puts[p1_idx], self.puts[p2_idx]
                if p1.strike > p2.strike:
                    dummy: Put = p2
                    p2 = p1
                    p1 = dummy
                if (p1, p2) not in seen:
                    seen.add((p1,p2))
                    if self.validCompare(p1, p2):
                        self.evaluate(p1, p2)
                       

def runStock(stock: Stock, put_tickers: list[str], strikes: list[float], bids: list[float], asks: list[float], exp_dates_yyyy_mm_dd: list[str]):
    # Populate Puts
    puts = []
    for idx in range(len(put_tickers)):
        # Convert YYYY-MM-DD string to datetime object
        date_obj = datetime.datetime.strptime(exp_dates_yyyy_mm_dd[idx], "%Y-%m-%d").date()
        # Format datetime object to MM/DD/YY string
        formatted_exp_date = date_obj.strftime("%m/%d/%y")
        
        put = Put(strikes[idx], bids[idx], asks[idx], formatted_exp_date, put_tickers[idx])
        puts.append(put)
    stock.puts = puts

    stock.populate_winners()






