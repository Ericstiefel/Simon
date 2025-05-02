from datetime import date
import datetime

class Put:
    def __init__(self, strike: int, bid: float, ask: float, exp_date: int):
        self.strike = strike
        self.bid = bid
        self.ask = ask
        self.exp_date = exp_date

class Stock:
    def __init__(self, tick: str):
        """
        Invalid if:
            >9 mo out
            negative midpoint
            bid = 0
            same strike        
        """
        self.tick = tick
        self.puts: list[Put] = []
        self.yld = [i for i in range(6, 11)] #yield values 6-10
        self.winners: list[tuple[Put, Put, float, int]] = [] #P1, P2, Midpoint, Yield

    @staticmethod
    def days_until(date: str):
        date_object = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        year = date_object.year
        month = date_object.month
        day = date_object.day
        tgt = datetime.date(year, month, day)
        today = datetime.date.today()
        return (tgt-today).days

    @staticmethod
    def midpoint(P1_bid: float, P1_ask: float, P2_bid: float, P2_ask: float) -> float:
        aggresive = -P1_bid + P2_ask
        conservative = -P1_ask + P2_bid
        return (aggresive + conservative) / 2
    
    @staticmethod
    def validCompare(p1: Put, p2: Put, max_strike_split: float = .25) -> bool:
        strike_diff: bool = abs((p1.strike - p2.strike) / p2.strike) < max_strike_split
        return (p1 != p2) and (p1.exp_date == p2.exp_date) and (p1.strike != p2.strike) and strike_diff

    
    def evaluate(self, p1: Put, p2: Put):
        exp = p1.exp_date
        days_out = self.days_until(exp)

        midpoint = self.midpoint(p1.bid, p1.ask, p2.bid, p2.ask)
        if midpoint <= 0:
            return

        for y in reversed(self.yld):
            score = (y/36500)*days_out*max(p1.strike, p2.strike)
            if score < midpoint:
                self.winners.append((p1, p2, midpoint, y))
                return

    def populate_winners(self) -> None:
        seen = set()
        for p1_idx in range(len(self.puts)):
            for p2_idx in range(p1_idx, len(self.puts)):
                p1, p2 = min(self.puts[p2_idx].strike, self.puts[p1_idx].strike), max(self.puts[p2_idx].strike, self.puts[p1_idx].strike)
                if (p1, p2) not in seen:
                    seen.add((p1,p2))
                    if self.validCompare(p1, p2):
                        self.evaluate(p1, p2)
                       

def runStock(stock: Stock, put_tickers: list[str], strikes: list[float], bids: list[float], asks: list[float], exp_dates: list[str]):
    #Populate Puts
    puts = []
    for idx in range(len(put_tickers)):
        put = Put(strikes[idx], bids[idx], asks[idx], exp_dates[idx])
        puts.append(put)
    stock.puts = puts

    #Populate Winners
    stock.populate_winners()






