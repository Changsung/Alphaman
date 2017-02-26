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

class Alphaman:
	'''Alphaman class which manages overall the library.
	'''

	def __init__(self, start_date, end_date):
		self.__start_date 	= start_date
		self.__end_date 	= end_date
		self.__feed 		= Feed(start_date, end_date)
		self.__broker = Broker(self)
		self.__record = []

	def addInstrumentData(self, data):
		pass

	def setStrategy(self, strategy):
		self.__strategy = strategy
		self.__strategy.setAlphaman(self)

	def setAnalysis(self, analysis):
		self.__analysis = analysis
		self.__analysis.setAlphaman(self)
	
	def buy(self, instrument, price, volumn):
		self.__broker.buy(instrument, price, volumn)
		self.__currentRecord().buy(instrument, volumn, price)

	def sell(self, instrument, price, volumn):
		self.__broker.sell(instrument, price, volumn)
		self.__currentRecord().sell(instrument, volumn, price)

	def getPriceOfInstrument(self, insturment):
		self.__feed.getPriceOfInstrument(instrument)

	def __currentRecord(self):
		return self.__record[-1]

	def run(self):
		feed = self.__feed.getFirstDailyFeed()
		while feed != NULL:
			self.__record.append(Record(feed.day))
			self.__strategy.handle_data(feed)
			record = self.__currentRecord()
			record.setAsset(self.__brocker.getTotalAsset())
			record.setHoldings(self.__brocker.getHoldings())
			feed = self.__feed.getNextDailyFeed()

	def show(self):
		self.__analysis.plot(self.__record)
		