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
import matplotlib as mpl
import operator
mpl.use("TkAgg")
import matplotlib.pyplot as plt, mpld3


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
		self.__numberOfRepresent = 8
		self.__recordData = []

	def projectOnGraph(self, day):
		self.__recordData.append(AnalysisRecord())

	def record(self, day, key, value):
		self.__recordData[-1].setRecordData(key, value)

	def setAlphaman(self, alphaman):
		self.__alphaman = alphaman

	def plot(self, records):
		top_instruments = self.getTopInstruments(records)
		num_rep = min(len(top_instruments), 8)
		fig, ax = plt.subplots(min(len(top_instruments), 8) + 1, 1, sharex="col", sharey="row", figsize=(8, 8))
		x = map(lambda x: x.getDay(), records) 
		y = map(lambda x: x.getAsset(), records)
		ax[0].plot(x, y, color='green')
		y = map(lambda x: x.getCash(), records) 
		ax[0].plot(x, y, color='blue')
		ax[0].set_title("Assets changes", size=20)
		# labels = self.makeLabels(records)
		# tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels) 
		# mpld3.plugins.connect(fig, tooltip)
		top_num = top_instruments[-num_rep:]
		for idx, value in enumerate(top_num):
			self.showInstruments(value[0], value[0], ax[idx+1], fig)
		mpld3.show()

	def showInstruments(self, instrument, records, ax, fig):
		dic 	= self.__alphaman.getPriceTimeDict(instrument)
		dic 	= sorted(dic.items(), key=operator.itemgetter(0))
		days 	= map(lambda x:x[0], dic)
		prices 	= map(lambda x:x[1], dic)
		ax.plot(days, prices)
		ax.set_title(instrument, size=20)

	def makeLabels(self, records):
		# labels = ['point {0}'.format(idx + 1) for idx, value in enumerate(records)]
		# print labels
		pass

	def getTopInstruments(self, records):
		dic = {}
		for record in records:
			buys = record.getBuys()
			sells = record.getSells()
			for key, item in buys.iteritems():
				if key in dic:
					dic[key] += item.volume
				else :
					dic[key] = item.volume
			for key, item in sells.iteritems():
				if key in dic:
					dic[key] += item.volume
				else :
					dic[key] = item.volume

		return sorted(dic.items(), key=lambda x: x[1])


