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
import plotly.plotly as py
import plotly.graph_objs as go

class AnalysisRecord:

	def __init__(self):
		self.__recordDict = {}

	def setRecordData(self,day, key, value):
		self.__recordDict[key] = value
		self.__day = day

	def getRecordDict(self):
		return self.__recordDict

	def getDay(self):
		return self.__day

class BaseAnalysis:
	'''class for plotting the data'''

	def __init__(self):
		self.__recordData = []

	def projectOnGraph(self, day):
		self.__recordData.append(AnalysisRecord())

	def record(self, day, key, value):
		self.__recordData[-1].setRecordData(key, value)

	def setAlphaman(self, alphaman):
		self.__alphaman = alphaman

	def plot(self, records):
		x = map(lambda x: x.getDay(), records) 
		y = map(lambda x: x.getAsset(), records) 
		data = [go.Scatter(
            x=x,
            y=y)]

		py.iplot(data)
