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
"""
class Alphaman:
	'''Alphaman class which manages overall the library.
	'''
	__broker = Broker(self)

	def __init__(self, start_date, end_date):
		self.__start_date 	= start_date
		self.__end_date 	= end_date
		self.__feed 		= Feed(start_date, end_date)

	def addInstrumentData(self, data):
		pass

	def setStrategy(self, strategy):
		self.__strategy = strategy
		self.__strategy.setAlphaman(self)

	def setAnalysis(self, analysis):
		self.__analysis = analysis
		self.__analysis.setAlphaman(self)
	
	def buy(self, instrument, price, volumn):
		self.__brocker.buy(instrument, price, volumn)

	def sell(self, instrument, price, volumn):
		self.__brocker.sell(instrument, price, volumn)

	def run(self):
		pass
"""

