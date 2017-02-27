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

class OrderSchedule:

	def __init__(self, scheduleIdx, instrument, volume, order_price, todayIdx, is_buy, days = None, stop_price = None):
		self.idx = scheduleIdx
		self.instrument = instrument
		self.volume = volume
		self.order_price = order_price
		self.todayIdx = todayIdx
		self.is_buy = is_buy
		self.days = days
		self.stop_price = stop_price

class ScheduleManager:

	def __init__(self, broker):
		self.__broker = broker
		self.__scheduleIdx = 0
		self.__schedules = []
		self.__scheduleCash = 0

	def addSchedule(self, instrument, volume, limit_price, is_buy, stop_price = None, days = None):
		if is_buy:
			self.__scheduleCash += limit_price * volume
		newSchedule = OrderSchedule(self.__scheduleIdx, instrument, volume, limit_price, self.__broker.getTodayIdx(), is_buy, stop_price, days)
		self.__scheduleIdx += 1
		self.__schedules.append(newSchedule)

	def cancelSchedule(self, schedule):
		if schedule.is_buy:
			self.__scheduleCash -= schedule.volume * schedule.order_price
			self.__broker.increaseCashBySchedule(schedule.volume * schedule.order_price)
			self.__schedules.remove(schedule)
		else :
			self.__schedules.remove(schedule)

	def operateSchedule(self):
		for scheduleItem in self.__schedules:
			if self.__broker.isEnablePriceOfInstrument(instrument, scheduleItem.order_price):
				self.__executeSchedule(scheduleItem)
				self.__schedules.remove(scheduleItem)
			else :
				if self.checkExpired(schedule):
					self.cancelSchedule(schedule)

	def __checkExpired(self, schedule):
		if schedule.days != None :
			if self.__broker.getTodayIdx() > schedule.days + schedule.todayIdx :
				return True
		if schedule.stop_price != None :
			return self.__broker.isEnablePriceOfInstrument(schedule.instrument, schedule.stop_price)
		return False

	def getScheduleCash(self):
		return self.__scheduleCash

	def getSchedules(self):
		return self.__schedules

	def __executeSchedule(self, schedule):
		if schedule.is_buy :
			self.__broker.buyBySchedule(schedule.instrument, price, volume)
			self.__scheduleCash -= price * volume
		else :
			self.__broker.sellBySchedule(schedule.instrument, price, volume)

