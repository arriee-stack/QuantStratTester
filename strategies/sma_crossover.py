from .strategy import Strategy
import vectorbt as vbt


class SMACrossover(Strategy):
    data = None
    dataEntries = []
    dataExits = []
    portfolio = None
    sma_fast = 0
    sma_slow = 0

    def __init__(self, data, sma_fast=20, sma_slow=50):
        super().__init__()
        self.data = data
        self.sma_fast = sma_fast
        self.sma_slow = sma_slow
        print("_________________________________")
        print(type(self.data))
        print(self.data)
        print(type(self.data))
        print(len(self.data))
        print("_________________________________")

    def entries(self):
        fast_ma = vbt.MA.run(self.data, self.sma_fast)
        slow_ma = vbt.MA.run(self.data, self.sma_slow)

        self.dataEntries = fast_ma.ma_crossed_above(slow_ma)
        return self.dataEntries

    def exits(self):
        fast_ma = vbt.MA.run(self.data, self.sma_fast)
        slow_ma = vbt.MA.run(self.data, self.sma_slow)
        self.dataExits = fast_ma.ma_crossed_below(slow_ma)
        return self.dataExits

    def results(self):
        self.portfolio = vbt.Portfolio.from_signals(
            self.data, self.entries(), self.exits()
        )
        return self.portfolio
