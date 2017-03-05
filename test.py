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
		sma = self.get(self.__instrument, tech_key('Close', 60, 'sma'), daily(-2, 0))
		stddev = self.get(self.__instrument, tech_key('Close', 60, 'stddev'), weekly(-2, 0))
		today_price = self.get(self.__instrument, 'Close', 0)
		yesterday_price = self.get(self.__instrument, 'Close', -1)
		print stddev
		if today_price < 35000:
			self.buy(self.__instrument, 10)
		else:
			self.sell(self.__instrument, 10)
		

start_date = datetime.datetime(2016,1,1)
end_date = datetime.datetime(2016,12,31)

instrument = "000660"

df = web.DataReader(instrument+".KS", "yahoo", start_date, end_date)

feed = Feed(start_date, end_date)

feed.addDailyFeed(df, instrument)

# sma
tech = Technical(feed)
feed.addTechnicalData(tech.sma(instrument, 'Close', 60), instrument)
feed.addTechnicalData(tech.stddev(instrument, 'Close', 60), instrument)

alphaman = Alphaman(start_date, end_date)
alphaman.setFeed(feed)
#alphaman.setShortSelling(True)
alphaman.setStrategy(MyStrategy(instrument))
alphaman.run()
#alphaman.showAsset()
alphaman.show()

# print dates
# daily_feed = feed.getDailyFeed(0)
# daily_instrument_data = daily_feed.getDailyInstrumentData(instrument)
#
# print daily_instrument_data.getBarData()