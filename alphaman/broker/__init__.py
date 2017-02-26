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


class Broker:
	'''class for asset management with cash and holdings.
	'''

	def __init__(self, alphaman):
		self.__alphaman = alphaman
		self.__cash = 10000000
		self.__holdings = {} 
		'''a dictionay whose keys are instruments, values are holding amount
		'''

	def getCash(self, cash):
		return self.__cash

	def setCash(self, cash):
		self.__cash = cash

	def buy(self, instrument, price, volume):
		if self.__cash < price * volume: 
			raise Exception("not afford to buy that volume ")
			return 
		self.__cash -= price * volume
		self.__buyInstrument(instrument, volume)

	def sell(self, instrument, price, volume):
		if instrument not in self.__holdings.keys():
			print "%s hasn't been held", instrument
			return
		if self.__holdings[instrument] < volume:
			print "%s hasn't been held that volume", instrument
			return
		self.__cash += price * volume
		self.__sellInstrument(instrument, volume)

	def __buyInstrument(self, instrument, volume):
		if instrument not in self.__holdings.keys():
			self.__holdings[instrument] = volume
		else:
			self.__holdings[instrument] += volume

	def __sellInstrument(self, instrument, volume):
		self.__holdings[instrument] -= volume

	def getVolumnOfInstrument(self, instrument):
		if instrument not in self.__holdings:
			return 0
		return self.__holdings[instrument]

	def getTotalAsset(self):
		asset = self.__cash
		for key, value in self.__holdings.items():
			asset += self.__getInstrumentValue(key, value)
		return asset

	def getHoldings(self):
		return self.__holdings

	def __getInstrumentValue(self, instrument, volume):
		return self.__alphaman.getPriceOfInstrument(instrument) * volume
