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
from __future__ import division
from alphaman.utils import tech_key
import math

class MovingWindow():
	def __init__(self, window_size):
		assert(window_size > 0)
		assert(isinstance(window_size, int))
		self.__window_size = window_size
		#self.__values = np.zeros(window_size, dtype)
		self.__values = []
		#self.__value_num = 0
		self.__mean = 0.
		self.__square_mean = 0.

	def getWindowSize(self):
		return self.__window_size

	def addNewValue(self, value):
		assert(value != None)
		if self.isWindowFull():
			# update mean, square mean
			self.__mean -= self.__values[0] / self.__window_size
			self.__square_mean -= self.__values[0] * self.__values[0] / self.__window_size
			del self.__values[0]
		# update mean, square mean
		self.__mean += value / self.__window_size
		self.__square_mean += value * value / self.__window_size
		self.__values.append(value)

	def getValues(self):
		return self.__values

	def isWindowFull(self):
		return len(self.__values) == self.__window_size

	def mean(self):
		if self.isWindowFull():
			return self.__mean
		else:
			return -1

	def stddev(self):
		if self.isWindowFull():
			# stddev is sqrt(square_mean - mean**2)
			return math.sqrt(self.__square_mean - self.__mean * self.__mean)
		else:
			return -1


class Technical():
	def __init__(self, feed):
		feed.trimDailyFeed()
		self.__feed = feed

	# simple moving average
	def sma(self, instrument, key, period):
		time_series = self.__feed.getTimeSeries(instrument, key)
		moving_window = MovingWindow(period)
		tech_time_series = []
		for value in time_series:
			moving_window.addNewValue(value)
			tech_time_series.append(moving_window.mean())
		# generate dictionary
		tech_dict = {tech_key(key, period, 'sma'): tech_time_series}
		return tech_dict

	def stddev(self, instrument, key, period):
		time_series = self.__feed.getTimeSeries(instrument, key)
		moving_window = MovingWindow(period)
		tech_time_series = []
		for value in time_series:
			moving_window.addNewValue(value)
			tech_time_series.append(moving_window.stddev())
		# generate dictionary
		tech_dict = {tech_key(key, period, 'stddev'): tech_time_series}
		return tech_dict