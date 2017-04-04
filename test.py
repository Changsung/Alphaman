import datetime
import pandas_datareader.data as web
import pandas as pd
from alphaman.feed import DailyInstrumentData, DailyFeed, Feed
from alphaman.strategy import BaseStrategy
from alphaman import Alphaman
from alphaman.technical import Technical
from alphaman.utils import daily, weekly, tech_key

class MyStrategy(BaseStrategy):
	def __init__(self, instrument):
		self.__instrument = instrument

	def handleData(self):
		#daily_feed = feed.getDailyFeed(today)
		sma1 = self.get(self.__instrument, tech_key('Close', 20, 'sma'), daily(-2, 0))
		sma2 = self.get(self.__instrument, tech_key('Close', 60, 'sma'), daily(-2, 0))
		if (sma1[0] > sma2[0]) and (sma1[-1] < sma2[-1]):
			self.orderTarget(self.__instrument, 0.7)
		elif (sma1[0] < sma2[0]) and (sma1[-1] > sma2[-1]):
			self.orderTarget(self.__instrument, 0.2)

start_date 	= datetime.datetime(2006,1,1)
end_date	= datetime.datetime(2016,12,31)

instrument = "007700"

df = web.DataReader(instrument+".KS", "yahoo", start_date, end_date)

feed = Feed(start_date, end_date)

feed.addDailyFeed(df, instrument)

# sma
tech = Technical(feed)
feed.addTechnicalData(tech.sma(instrument, 'Close', 60), instrument)
feed.addTechnicalData(tech.sma(instrument, 'Close', 20), instrument)

alphaman = Alphaman(start_date, end_date)
alphaman.setFeed(feed)
alphaman.setStrategy(MyStrategy(instrument))
alphaman.run()
alphaman.show()
