from tradingview_ta import TA_Handler, Interval, Exchange

class TvAnalysis:
  def __init__ (self, symbol, screener,exchange, interval=Interval.INTERVAL_4_HOURS):
    self.symbol = symbol
    self.screener = screener
    self.exchange = exchange
    self.interval = interval

  def analysis(self):
    handler = TA_Handler(
        symbol = self.symbol,
        screener = self.screener,
        exchange = self.exchange,
        interval = self.interval
    )
    return handler.get_analysis()

  def get_indicators(self):
    return self.analysis().indicators

  def get_summary(self):
    return self.analysis().summary

  def get_statistics(self):
    temp = self.get_indicators()
    result = {}
    result["open"] = temp["open"]
    result["close"] = temp["close"]
    result["high"] = temp["high"]
    result["low"] = temp["low"]
    result["volume"] = temp["volume"]

    return result

  def rsi_analysis(self):
    rsi = self.get_indicators()["RSI"]
    result = {}
    result['rsi'] = rsi

    if (rsi >= 70):
      result['status'] = 'Overbought'
    elif (rsi <= 30):
      result['status'] = 'Oversold'
    else:
      result['status'] = 'Neutral'

    return result

  def moving_average_analysis(self):
    return

  def macd_analysis(self):
    return


if __name__ == "__main__":
  analyzer = TvAnalysis("AAPL","america","NASDAQ")
  print(analyzer.get_summary())
