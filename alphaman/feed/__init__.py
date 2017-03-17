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

import datetime
import pandas as pd

from alphaman.utils import calculate_quarter_count, get_closest_quarter, quarterify


class DailyInstrumentData():
	"""class for holding daily, per instrument data.
	bar data, other daily data are stored in the class, per instrumently.
	NOTE: bar data is mandatory.
	"""
	def __init__(self, instrument, bar_data, extra_data, is_tradable=False):
		self.__instrument = instrument
		self.__bar_data = bar_data
		self.__extra_data = extra_data
		self.__is_tradable = is_tradable

	def getInstrument(self):
		return self.__instrument

	def getIsTradable(self):
		return self.__is_tradable
		
	def getBarData(self, key):
		return self.__bar_data[key]
		
	def getExtraData(self, key):
		return self.__extra_data[key]

	def addExtraData(self, key, value):
		self.__extra_data[key] = value


class QuarterlyInstrumentData():
	"""class for holding quarterly, per instrument data.
	finantial data, per instrumently
	"""
	def __init__(self, instrument, finance_data={}):
		self.__instrument = instrument
		self.__finance_data = finance_data
		
	def getInstrument(self):
		return self.__instrument
		
	def addFinanceData(self, key, value):
		self.__finance_data[key] = value


class DailyFeed():
	"""class for holding daily feed data
	DailyInstrumentData is accumulated for every date
	"""
	def __init__(self, cur_date=None, is_tradable=False):
		self.__cur_date = cur_date
		self.__is_tradable = is_tradable
		self.__daily_data = {}

	def setIsTradable(self, is_tradable):
		self.__is_tradable = is_tradable

	def getIsTradable(self):
		return self.__is_tradable

	def getCurDate(self):
		return self.__cur_date

	def getDailyInstrumentData(self, instrument):
		return self.__daily_data[instrument]

	def addDailyInstrumentData(self, daily_instrument_data):
		"""method for adding DailyInstrumentData.
		"""
		self.__daily_data[daily_instrument_data.getInstrument()] = daily_instrument_data
		if daily_instrument_data.getIsTradable():
			self.__is_tradable = True


class QuarterlyFeed():
	
	def __init__(self, cur_date=None):
		self.__cur_date = cur_date
		self.__quarterly_data = {}
		
	def getCurDate(self):
		return self.__cur_date
		
	def addQuarterlyInstrumentData(self, quarterly_instrument_data):
		"""method for adding QuarterlyInstrumentData.
		"""
		self.__quarterly_data[feed_data.getInstrument()] = quarterly_instrument_data
		

class Feed():
	"""Feed class which holds every feed data.
	:param start_date/end_date: The datetime object which indicates start/end of
		the feed data, respectively.
	:type start_date/end_date: datetime
	"""

	def __init__(self, start_date=None, end_date=None):
		self.__start_date = start_date
		self.__end_date   = end_date
		
		# check start_date / end_date
		if end_date < start_date:
			raise Exception("end_date must exceed start_date")
		
		# get date_delta and allocate daily feeds list
		self.__daily_feeds = []
		day_count = (end_date - start_date).days
		for cur_date in (start_date + datetime.timedelta(days=n)\
			for n in range(day_count+1)):
			self.__daily_feeds.append(DailyFeed(cur_date))

		# make list for quarterly feeds
		self.__quarterly_feeds = []
		quarter_count = calculate_quarter_count(start_date, end_date)
		year, quarter_num = get_closest_quarter(start_date, False)
		for _ in range(quarter_count):
			self.__quarterly_feeds.append(QuarterlyFeed(quarterify(year, quarter_num)))
			quarter_num += 1
			if quarter_num == 5:
				year += 1
				quarter_num -= 4
			
	def setStartDate(self, start_date):
		if self.__end_date != None and start_date > self.__end_date:
			raise Exception("end_date must exceed start_date")
		self.__start_date = start_date

	def setEndDate(self, end_date):
		if self.__start_date != None and end_date < self.__start_date:
			raise Exception("end_date must exceed start_date")
		self.__end_date = end_date

	def addDailyFeed(self, daily_feed, instrument):
		"""methods for adding Daily Feed.
		:param daily_feed: data to feed, which in form of DataFrame
		:type daily_feed: pd.DataFrame

		:param instrument: company code
		:type instrument: str
		"""
		# 1. get column names
		BAR_IND = ["Open", "Close", "High", "Low", "Adj Close", "Volume"]
		columns = daily_feed.columns
		bar_columns = filter(lambda x: x in BAR_IND, columns)
		extra_columns = filter(lambda x: x not in BAR_IND, columns)
		
		for index, data in daily_feed.iterrows():
			# index type?? string or datetime?
			index = str(index)
			index = index.split(" ")[0]
			year = int(index.split("-")[0])
			month = int(index.split("-")[1])
			day = int(index.split("-")[2])
			cur_date = datetime.datetime(year, month, day)
			day_count = (cur_date - self.__start_date).days
			# get daily_feed
			daily_feed = self.__daily_feeds[day_count]
			# make bar_data
			bar_data = {}
			for column in bar_columns:
				bar_data[column] = int(data[column])
			# make extra_data
			extra_data = {}
			for column in extra_columns:
				extra_data[column] = int(data[column])
			# make is_tradable
			is_tradable = True
			if data['Volume'] == 0:
				is_tradable = False
			# create daily_instrument_data
			daily_instrument_data = DailyInstrumentData(instrument, bar_data, extra_data, is_tradable)
			# add daily_instrument_data to daily_feed
			daily_feed.addDailyInstrumentData(daily_instrument_data)

	def trimDailyFeed(self):
		"""method for trimming untradable date
		"""
		self.__daily_feeds = filter(lambda x: x.getIsTradable(), self.__daily_feeds)

	def getDailyFeed(self, today_idx):
		#day_count = (cur_date - self.__start_date).days
		return self.__daily_feeds[today_idx]
	
	def getDailyInstrumentData(self, today_idx, instrument):
		return self.getDailyFeed(today_idx).getDailyInstrumentData(instrument)
	
	def getTradableDates(self):
		return len(self.__daily_feeds)

	def isEnablePriceOfInstrument(self, instrument, today_idx, price):
		daily_instrument_data = self.__daily_feeds[today_idx].getDailyInstrumentData(instrument)
		high = daily_instrument_data.getBarData('High')
		low = daily_instrument_data.getBarData('Low')
		if price <= high and price >= low:
			return True
		return False
			
	def getPriceOfInstrument(self, instrument, today):
		return self.__daily_feeds[today].getDailyInstrumentData(instrument).getBarData('Close')
	"""	
	def getFirstDailyFeed(self):
		for daily_feed in self.__daily_feeds:
			if daily_feed.getIsTradable() == True:
				self.__cur_date = daily_feed.getCurDate()
				return daily_feed
		raise Exception("there is no tradable date during the period")
		
	def getNextDailyFeed(self):
		for daily_feed in self.__daily_feeds:
			if daily_feed.getIsTradable() == True:
				self.__past_feeds.append(daily_feed)
			self.__daily_feeds.pop(daily_feed)
		self.__past_feeds = 
	"""
	
	def addQuarterlyFeed(self, quarterly_feed, instrument):
		"""methods for adding Quarterly Feed.
		:param quarterly_feed: data to feed, which in form of DataFrame
		:type quarterly_feed: pd.DataFrame

		:param instrument: company code
		:type instrument: str
		"""
		for index, data in quarterly_feed.iterrows():
			# get datetime from index
			index = str(index)
			index = index.split(" ")[0]
			year = int(index.split("-")[0])
			month = int(index.split("-")[1])
			day = int(index.split("-")[2])
			cur_date = datetime.datetime(year, month, day)
			# make QuarterlyInstrumentData
			finance_data = {}
			for column in quarterly_feed.columns:
				finance_data[column] = int(data[column])
			quarterly_instrument_data = QuarterlyInstrumentData(instrument, finance_data)
			self.__quarterly_feeds.append(quarterly_instrument_data)
	
	def getQuarterlyFeeds(self):
		return self.__quarterly_feeds

	def getQuarterlyFeed(self, cur_date):
		"""returns closest quarter's feed
		"""
		cur_year, cur_quarter_num = get_closest_quarter(cur_date)
		start_year, start_quarter_num = get_closest_quarter(self.__start_date, False)

		idx = (cur_year-start_year) * 4 - start_quarter_num + cur_quarter_num
		if idx < 0:
			return None
		else:
			return self.__quarterly_feeds[idx]
	'''
	def getTimeDict(self, instrument, key):
		time_dict = {}
		for daily_feed in self.__daily_feeds:
			date = daily_feed.getCurDate()
			try:
				time_dict[date] = daily_feed.getDailyInstrumentData(instrument).getBarData(key)
			except KeyError:
				time_dict[date] = daily_feed.getDailyInstrumentData(instrument).getExtraData(key)
		return time_dict
	'''
	def getTimeDict(self, instrument, key):
		time_series = []
		for daily_feed in self.__daily_feeds:
			try:
				time_series.append((daily_feed.getCurDate(), daily_feed.getDailyInstrumentData(instrument).getBarData(key)))
			except KeyError:
				time_series.append((daily_feed.getCurDate(), daily_feed.getDailyInstrumentData(instrument).getExtraData(key)))
		return time_series
	

	def getTimeSeries(self, instrument, key):
		"""returns list of certain data
		"""
		time_series = []
		for daily_feed in self.__daily_feeds:
			try:
				time_series.append(daily_feed.getDailyInstrumentData(instrument).getBarData(key))
			except KeyError:
				time_series.append(daily_feed.getDailyInstrumentData(instrument).getExtraData(key))
		return time_series
		
	def addTimeSeries(self, instrument, key, time_series):
		for idx in range(len(self.__daily_feeds)):
			daily_instrument_data = self.__daily_feeds[idx].getDailyInstrumentData(instrument)
			daily_instrument_data.addExtraData(key, time_series[idx])

	def addTechnicalData(self, technical_dict, instrument):
		for key, value in technical_dict.iteritems():
			self.addTimeSeries(instrument, key, value)