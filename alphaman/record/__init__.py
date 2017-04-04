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

class RecordCompany:
	'''class for recording the holding company'''

	def __init__(self, instrument, volume, price):
		self.instrument = instrument
		self.volume = volume
		self.price = price

class Record:
	'''class for recording the assets'''

	def __init__(self, day):
		self.__buy = {}
		self.__day = day
		self.__sell = {}
		self.__asset = 0
		self.__cash  = 0
		self.__holdings = None  
		''' 
		__holdings is a dictionary whoose key is instrument string and value is a dictonary which contains volume and asset
		ex) __holdings = {"000960":{"volume":3, "aset": 109,000}, ...}
		'''

	def setCash(self, cash):
		self.__cash = cash

	def getCash(self):
		return self.__cash

	def setAsset(self, asset):
		self.__asset = asset

	def getAsset(self):
		return self.__asset

	def setHoldings(self, holdings):
		self.__holdings = holdings
		
	def getHoldings(self):
		return self.__holdings

	def buy(self, instrument, volume, price):
		self.__buy[instrument] = RecordCompany(instrument, volume, price)

	def sell(self, instrument, volume, price):
		self.__sell[instrument] = RecordCompany(instrument, volume, price)

	def getDay(self):
		return self.__day

	def getBuys(self):
		return self.__buy;

	def getSells(self):
		return self.__sell


