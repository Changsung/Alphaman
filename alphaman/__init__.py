# MIT License
#
# Copyright (c) 2017 Changsung
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from alphaman.broker import Broker
from alphaman.record import Record
from alphaman.analysis import BaseAnalysis

class Alphaman:
	'''Alphaman class which manages overall the library.
	'''
	def __init__(self, start_date, end_date):
		self.__start_date 	= start_date
		self.__end_date 	= end_date
		self.__broker = Broker(self)
		self.__record = []
		self.__today_idx = 0
		self.setAnalysis(BaseAnalysis())
		self.__short_selling = False

	def setShortSelling(self, short_selling):
		self.__short_selling = short_selling

	def isShortSelling(self):
		return self.__short_selling

	def setFeed(self, feed):
		feed.trimDailyFeed()
		self.__feed = feed

	def addInstrumentData(self, data):
		pass

	def setStrategy(self, strategy):
		self.__strategy = strategy
		self.__strategy.setAlphaman(self)

	def setAnalysis(self, analysis):
		self.__analysis = analysis
		self.__analysis.setAlphaman(self)

	def orderTarget(self, instrument, percentage, limit_price = None, stop_price = None, days = None):
		self.__broker.orderTargetPercent(instrument, percentage, limit_price, stop_price, days)
	
	def buy(self, instrument, volume, limit_price = None, stop_price = None, days = None):
		self.__broker.buy(instrument, volume, limit_price, stop_price, days)

	def sell(self, instrument, volume, limit_price = None, stop_price = None, days = None):
		self.__broker.sell(instrument, volume, limit_price, stop_price, days)
	
	def buyCallBack(self, instrument, price, volume):
		self.__currentRecord().buy(instrument, price, volume)

	def sellCallBack(self, instrument, price, volume):
		self.__currentRecord().sell(instrument, price, volume)

	def getPriceOfInstrument(self, instrument):
		return self.__feed.getPriceOfInstrument(instrument, self.__today_idx)

	def isEnablePriceOfInstrument(self, instrument, price):
		return self.__feed.isEnablePriceOfInstrument(instrument, self.__today_idx, price)
		
	def getSchedules(self):
		return self.__broker.getSchedules()		

	def getTodayIdx(self):
		return self.__today_idx

	def getFeed(self):
		return self.__feed
	
	def __currentRecord(self):
		return self.__record[-1]

	def getPriceTimeDict(self, instrument):
		return self.__feed.getTimeDict(instrument, 'Close')

	def run(self):
		#feed = self.__feed.getFirstDailyFeed()
		feed = self.__feed
		tradable_dates = feed.getTradableDates()
		for today in range(tradable_dates):
			self.__today_idx = today
			daily_feed = feed.getDailyFeed(today)
			self.__record.append(Record(daily_feed.getCurDate()))
			#self.__strategy.handleData(feed, today)
			self.__strategy.handleData()
			self.__broker.operateSchedule()
			self.__recordData()

	def __recordData(self):
		record = self.__currentRecord()
		record.setAsset(self.__broker.getTotalAsset())
		record.setCash(self.__broker.getCash() + self.__broker.getScheduleCash())
		holdings = {}
		holdingAssets = self.__broker.getHoldingAssets()
		for item, volume in self.__broker.getHoldings().iteritems():
			holdings[item] = {"volume":volume, "asset":holdingAssets[item]}
		record.setHoldings(holdings)

	def showAsset(self):
		for item in self.__record:
			print item.getAsset()
			print item.getHoldings()

	def show(self):
		self.__analysis.plot(self.__record)
