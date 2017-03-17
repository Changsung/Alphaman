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

from flask import Flask, render_template

class WebApp(Flask):

	__instrumentDatas = []
	''' __instrumentDatas is a list of tuples which holds instruments data
		In the tuple:
			first item is instrument
			second item is a list of bar data
			third item is a list of trade data
	'''

	def setAssetDataList(self, asset_data_list):
		self.__assetDataList = asset_data_list

	def getAssetDataDict(self):
		return map(lambda x: x.toDict(), self.__assetDataList)

	def addInstrumentData(self, instrument, bar_data, trade_data):
		self.__instrumentDatas.append((instrument, bar_data, trade_data))

	def getInstrumentDatas(self):
		return map(lambda x: {"instrument":x[0], "bar_data":map(lambda y:y.toDict(), x[1]), "trade_data":map(lambda y:y.toDict(), x[2])}, self.__instrumentDatas)

app = WebApp(__name__)

@app.route("/")
def show():
	return render_template('show.html', asset=app.getAssetDataDict(), instrument=app.getInstrumentDatas())