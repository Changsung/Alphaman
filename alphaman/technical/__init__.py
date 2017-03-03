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


class MovingWindow():
	def __init__(self, window_size, dtype=float):
		assert(window_size > 0)
		assert(isinstance(window_size, int))
		self.__window_size = window_size
		#self.__values = np.zeros(window_size, dtype)
		self.__values = []
		#self.__value_num = 0

	def getWindowSize(self):
		return self.__window_size

	def addNewValue(self, value):
		assert(value != None)
		if self.isWindowFull():
			del self.__values[0]
			#np.delete(self.__values, 0)
			#self.__value_num -= 1
		self.__values.append(value)
		#np.insert(self.__values, (self.__window_size-1), value)

	def getValues(self):
		return self.__values

	def isWindowFull(self):
		return len(self.__values) == self.__window_size