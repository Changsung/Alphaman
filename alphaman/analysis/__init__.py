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

import operator
from alphaman.analysis.webapp import app
from alphaman.analysis.DisplayData import DisplayData
import webbrowser

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
		self.__app = app

	def projectOnGraph(self, day):
		self.__recordData.append(AnalysisRecord())

	def record(self, day, key, value):
		self.__recordData[-1].setRecordData(key, value)

	def setAlphaman(self, alphaman):
		self.__alphaman = alphaman

	def makeAssetDataList(self, records):
		result = []
		for item in records:
			display_data = DisplayData(item.getDay().strftime("%Y-%m-%d"), [("asset", item.getAsset()), ("cash", item.getCash())])
			result.append(display_data)
		return result

	def makeBarDataList(self, instrument):
		result = []
		bar_data = self.__alphaman.getPriceTimeDict(instrument)
		for key, value in bar_data.iteritems():
			display_data = DisplayData(key.strftime("%Y-%m-%d"), [("price", value)])
			result.append(display_data)
		return result

	def makeTradeDataList(self, instrument, records):
		return None

	def plot(self, records):
		# x = map(lambda x: x.getDay(), records)
		# y_1 = map(lambda x: x.getAsset(), records)
		# y_2 = map(lambda x: x.getCash(), records)
		# self.__app.setAssetData(DisplayData(("days", x), [("asset", y_1), ("cash", y_2)]))
		
		# make instrument data & add
		top_instruments = self.getTopInstruments(records)
		num_rep = min(len(top_instruments), 8)
		top_instruments = top_instruments[-num_rep:]
		for instrument in top_instruments:
		 	self.__app.addInstrumentData(instrument, self.makeBarDataList(instrument), self.makeTradeDataList(instrument, records))
		# make asset data
		assetDataList = self.makeAssetDataList(records)
		self.__app.setAssetDataList(assetDataList)
		
		webbrowser.open_new("http://127.0.0.1:8888/")
		self.__app.run(host='0.0.0.0', port='8888')

	def makeClassData(self, instrument, records):
		dic 	= self.__alphaman.getPriceTimeDict(instrument)
		dic 	= sorted(dic.items(), key=operator.itemgetter(0))
		days 	= map(lambda x:x[0], dic)
		prices 	= map(lambda x:x[1], dic)
		return DisplayData(("days", days), [("prices", prices)])

	def getTopInstruments(self, records):
		''' return instrument code list which are sorted by trading volume'''
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

		return map(lambda x: x[0] ,sorted(dic.items(), key=lambda x: x[1]))


