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


class DailyInstrumentData():
	"""class for holding daily, per instrument data.
	bar data, other daily data are stored in the class, per instrumently.
	"""
	def __init__(self, instrument, bar_data, extra_data={}, technical_data={},\
					is_tradable=False):
		self.__instrument = instrument
		self.__bar_data = bar_data
		self.__extra_data = extra_data
		self.__technical_data = technical_data
		self.__is_tradable = is_tradable

	def getInstrument(self):
		return self.__instrument

	def addExtraData(self, key, value):
		self.__extra_data[key] = value

	def addTechnicalData(self, key, value):
		self.__technical_data[key] = value


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

	def addDailyInstrumentData(self, feed_data):
		"""methods for adding DailyCompanyData.
		"""
		self.__daily_data[feed_data.getInstrument()] = feed_data


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
		

	def setStartDate(self, start_date):
		if self.__end_date != None and start_date > self.__end_date:
			raise Exception("end_date must exceed start_date")
		self.__start_date = start_date

	def setEndDate(self, end_date):
		if self.__start_date != None and end_date < self.__start_date:
			raise Exception("end_date must exceed start_date")
		self.__end_date = end_date

	def addDailyFeed(self, feed_data, instrument):
		"""methods for adding Daily Feed from feed_data.
		:param feed_data: data to feed, which in form of DataFrame
		:type feed_data: pd.DataFrame

		:param instruments: company code
		:type instruments: str
		"""
		pass

	def getDailyFeed(self, cur_date):
		day_count = (cur_date - self.__start_date).days
		return self.__daily_feeds[day_count]