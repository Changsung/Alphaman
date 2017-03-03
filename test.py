import datetime
import pandas_datareader.data as web
import pandas as pd
from alphaman.feed import DailyInstrumentData, DailyFeed, Feed
from alphaman.strategy import BaseStrategy
from alphaman import Alphaman


class MyStrategy(BaseStrategy):
	def __init__(self, instrument):
		self.__instrument = instrument
		
	def handleData(self, feed, today):
		daily_feed = feed.getDailyFeed(today)
		daily_data = daily_feed.getDailyInstrumentData(self.__instrument)
		if daily_data.getBarData()['Close'] < 30000:
			self.buy(self.__instrument, 10)
		else :
			self.sell(self.__instrument, 10)

start_date = datetime.datetime(2015,1,1)
end_date = datetime.datetime(2016,12,31)



instrument = "000660"

df = web.DataReader(instrument+".KS", "yahoo", start_date, end_date)

feed = Feed(start_date, end_date)

feed.addDailyFeed(df, instrument)
feed.trimDailyFeed()
dates = feed.getTradableDates()

alphaman = Alphaman(start_date, end_date)
alphaman.setFeed(feed)
alphaman.setShortSelling(True)
alphaman.setStrategy(MyStrategy(instrument))
alphaman.run()
#alphaman.showAsset()
alphaman.show()

# print dates
# daily_feed = feed.getDailyFeed(0)
# daily_instrument_data = daily_feed.getDailyInstrumentData(instrument)
#
# print daily_instrument_data.getBarData()