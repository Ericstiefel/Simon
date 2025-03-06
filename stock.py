from metrics import *
import typing as tt

class Stock:
    def __init__(self):
        self.calls: tt.Dict[str: list[float]] = {} #self.calls[Tick] = [low, high]
        self.puts: tt.Dict[str: list[float]] = {}