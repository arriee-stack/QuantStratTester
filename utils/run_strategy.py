class runStrategy():
    strategy = None
    def __init__(self, strategy):
        self.strategy = strategy

    def tradesChart(self):
        fig = self.strategy.results().trades.plot()
        return fig
    
    def equityCurveData(self):
        equity_curve = self.strategy.results().value()
        df = equity_curve.reset_index()
        df.columns = ['time', 'equity']
        return df


