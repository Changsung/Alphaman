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

class BaseStrategy:
	''' class for strategy. 
		write an algorithm in this class'''

	__signals = {}

	def __init__(self):
		pass

	def addSignals(self, key, signal):
		self.__signals[key] = signal
		signal.setStrategy(self)

	def getSignal(self, key):
		return self.__signals[key].getSignal()

	def handleData(self):
		raise NotImplementedError()

	def setAlphaman(self, alphaman):
		self.__alphaman = alphaman

	def buy(self, instrument, volume, limit_price=None, stop_price=None, days=None):
		self.__alphaman.buy(instrument, volume, limit_price, stop_price, days)

	def sell(self, instrument, volume, limit_price=None, stop_price=None, days=None):
		self.__alphaman.sell(instrument, volume, limit_price, stop_price, days)

	def orderTarget(self, instrument, percentage, limit_price=None, stop_price=None, days=None):
		self.__alphaman.orderTarget(instrument, percentage, limit_price, stop_price, days)

	def getSchedules(self):
		return self.__alphaman.getSchedules()		
	
	def getFeed(self):
		return self.__alphaman.getFeed()

	def get(self, instrument, key, date_idx):
		# assert to only access to previous data
		feed = self.getFeed()
		if isinstance(date_idx, int):
			assert(date_idx <= 0)
			today_idx = self.__alphaman.getTodayIdx() + date_idx
			if today_idx < 0:
				today_idx = 0
			try:
				return feed.getDailyInstrumentData(today_idx, instrument).getBarData(key)
			except KeyError:
				return feed.getDailyInstrumentData(today_idx, instrument).getExtraData(key)
		elif isinstance(date_idx, list):
			assert(date_idx[-1] <= 0)
			today_idx_list = map(lambda x: x+self.__alphaman.getTodayIdx(), date_idx)
			#today_idx_list = list(set(today_idx_list)).sort()
			data_list = []
			for today_idx in today_idx_list:
				if today_idx < 0:
					continue
				try:
					data_list.append(feed.getDailyInstrumentData(today_idx, instrument).getBarData(key))
				except KeyError:
					data_list.append(feed.getDailyInstrumentData(today_idx, instrument).getExtraData(key))
			return data_list
		else:
			raise Exception('date_idx must be int or list of int')
	
