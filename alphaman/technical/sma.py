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

from alphaman.technical import MovingWindow
import numpy as np

class SimpleMovingAverage():
	def __init__(self, feed, instrument, key, window_size, dtype=float):
		self.__feed = feed
		self.__instrument = instrument
		self.__key = key
		self.__time_series = feed.getTimeSeries(instrument, key)
		self.__today_idx = 0
		self.__moving_window = MovingWindow(window_size, dtype)
		#while !self.__moving_window.isWindowFull():
		#	self.__moving_window.addNewValue(self.__time_series[self.__today_idx])
		#	self.__today_idx += 1

	def getTimeSeries(self):
		values = self.__moving_window.getValues()
		sma_time_series = []
		for idx in range(len(self.__time_series)):
			self.__moving_window.addNewValue(self.__time_series[idx])
			if self.__moving_window.isWindowFull():
				sma_time_series.append(np.average(values))
			else:
				sma_time_series.append(-1)
		return sma_time_series
		#self.__feed.addTimeSeries(sma_time_series, self.__instrument, 'Close_SMA')