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

from Schedule import ScheduleManager

class Broker:
	'''class for asset management with cash and holdings.
	'''

	def __init__(self, alphaman):
		self.__alphaman = alphaman
		self.__cash = 10000000
		self.__holdings = {} 
		'''a dictionay whose keys are instruments, values are holding amount
		'''
		self.__scheduleManager = ScheduleManager(self)

	def getCash(self):
		return self.__cash

	def setCash(self, cash):
		self.__cash = cash

	def orderTargetPercent(self, instrument, percent, limit_price = None, stop_price = None, days = None):
		if limit_price == None or self.isEnablePriceOfInstrument(instrument, limit_price) :
			buyCash = self.getTotalAsset() * percent
			price 	= limit_price and limit_price or self.__alphaman.getPriceOfInstrument(instrument)
			volume  = int(buyCash / price)
			currentVolume = self.getVolumeOfInstrument(instrument)
			if currentVolume > volume :
				self.sell(instrument, currentVolume - volume, limit_price, stop_price, days)
			elif currentVolume < volume :
				self.buy(instrument, volume - currentVolume, limit_price, stop_price, days)
		else:
			self.__scheduleManager.addScheduleByPortion(instrument, limit_price, percent, stop_price, days)

	def disaposeOfInstrument(self, instrument):
		volume = self.getVolumeOfInstrument(instrument)
		if volume > 0:
			self.sell(instrument, volume)
		else:
			self.buy(instrument, volume)

	def __orderScheduleByVolume(self, instrument, volume, limit_price, is_buy, stop_price = None, days = None):
		if is_buy:
			if self.__cash < limit_price * volume: 
				print "not afford to buy that volume"
				return
			else :
				self.__cash -= limit_price * volume
		self.__scheduleManager.addScheduleByVolme(instrument, volume, limit_price, is_buy, stop_price, days)

	def buy(self, instrument, volume, limit_price = None, stop_price = None, days = None):
		if limit_price != None:
			if self.isEnablePriceOfInstrument(instrument, limit_price):
				self.__buy(instrument, limit_price, volume)
			else :
				self.__orderScheduleByVolume(instrument, volume, limit_price, True, stop_price, days)
		else :
			self.__buy(instrument, self.__alphaman.getPriceOfInstrument(instrument), volume)

	def sell(self, instrument, volume, limit_price = None, stop_price = None, days = None):
		if limit_price != None:
			if self.isEnablePriceOfInstrument(instrument, limit_price) :
				self.__sell(instrument, limit_price, volume)
			else :
				self.__orderScheduleByVolume(instrument, volume, limit_price, False, stop_price, days)
		else :
			self.__sell(instrument, self.__alphaman.getPriceOfInstrument(instrument), volume)

	def __buy(self, instrument, price, volume):
		if self.__cash < price * volume: 
			#print "not afford to buy %d shares", volume
			affordable_volme = self.__cash / price
			volume = affordable_volme
			#print "afford to buy only %d shares", volume
		self.__cash -= price * volume
		self.__buyInstrument(instrument, volume)
		self.__alphaman.buyCallBack(instrument, volume, price)

	def __sell(self, instrument, price, volume):
		if not self.isShortSelling():
			if volume - self.getVolumeOfInstrument(instrument) > 0 :
				print "%s hasn't been held that volume", instrument
				return self.__sell(instrument, price, self.getVolumeOfInstrument(instrument))
		self.__cash += price * volume
		self.__sellInstrument(instrument, volume)
		self.__alphaman.sellCallBack(instrument, volume, price)

	def buyBySchedule(self, instrument, price, volume):
		self.__buyInstrument(instrument, volume)

	def sellBySchedule(self, instrument, price, volume):
		self.__cash += price * volume
		self.__sellInstrument(instrument, volume)

	def __buyInstrument(self, instrument, volume):
		if instrument not in self.__holdings.keys():
			self.__holdings[instrument] = volume
		else:
			self.__holdings[instrument] += volume

	def __sellInstrument(self, instrument, volume):
		if instrument not in self.__holdings.keys():
			self.__holdings[instrument] = -volume
		else:
			self.__holdings[instrument] -= volume

	def getVolumeOfInstrument(self, instrument):
		if instrument not in self.__holdings:
			return 0
		return self.__holdings[instrument]

	def getScheduleCash(self):
		return self.__scheduleManager.getScheduleCash()

	def getTotalAsset(self):
		asset = self.__cash + self.getScheduleCash()
		for key, value in self.__holdings.items():
			asset += self.__getInstrumentValue(key, value)
		return asset

	def getHoldings(self):
		return self.__holdings

	def getHoldingAssets(self):
		result = {}
		for key, volume in self.__holdings.iteritems():
			result[key] = self.__alphaman.getPriceOfInstrument(key) * volume
		return result

	def __getInstrumentValue(self, instrument, volume):
		return self.__alphaman.getPriceOfInstrument(instrument) * volume

	def isEnablePriceOfInstrument(self, instrument, price):
		return self.__alphaman.isEnablePriceOfInstrument(instrument, price)

	def isShortSelling(self):
		return self.__alphaman.isShortSelling()

	def getTodayIdx(self):
		return self.__alphaman.getTodayIdx()

	def increaseCashBySchedule(self, cash):
		self.__cash += cash

	def getSchedules(self):
		return self.__scheduleManager.getSchedules()

	def cancelSchedule(self, schedule):
		self.__scheduleManager.cancelSchedule(schedule)

	def operateSchedule(self):
		self.__scheduleManager.operateSchedule()

