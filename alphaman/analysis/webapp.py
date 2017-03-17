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
from threading import Thread
import socket
import time
import webbrowser

class OpenBrowser(Thread):

    def __init__(self):
        super(OpenBrowser, self).__init__()

    def notResponding(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1', 8888))

    def run(self):
        while self.notResponding():
            print('Did not respond')
        print('Responded')
        webbrowser.open_new('http://127.0.0.1:8888/') 

class WebApp(Flask):
	
	''' __instrument_datas is a list of tuples which holds instruments data
		In the tuple:
			first item is instrument
			second item is a list of bar data
			third item is a list of trade data
	'''
	__instrument_datas = []

	def setAssetDataList(self, asset_data_list):
		self.__asset_data_list = asset_data_list

	def getAssetDataDict(self):
		keys = self.__asset_data_list[0].toDict().keys()
		asset_dict = {}
		for key in keys:
			asset_dict[key] = map(lambda x: x.toDict()[key], self.__asset_data_list)
		return asset_dict
		#return map(lambda x: x.toDict(), self.__asset_data_list)

	def addInstrumentData(self, instrument, bar_data, trade_data):
		self.__instrument_datas.append((instrument, bar_data, trade_data))

	def getInstrumentDatas(self):
		instrument_list = []
		for instrument_data in self.__instrument_datas:
			instrument_dict = {}
			instrument_dict['instrument'] = instrument_data[0]

			instrument_dict['bar_data']   = {'x': map(lambda x: x.toDict()['x'], instrument_data[1]), 'price': map(lambda x: x.toDict()['price'], instrument_data[1])}
			instrument_list.append(instrument_dict)
		return instrument_dict
		#return map(lambda x: {"instrument":x[0], "bar_data":map(lambda y:y.toDict(), x[1]), "trade_data":map(lambda y:y.toDict(), x[2])}, self.__instrument_datas)

	def execute(self):
		op = OpenBrowser()
		op.start()
		self.run(host='0.0.0.0', port='8888')


app = WebApp(__name__)

@app.route("/")
def show():
	#return render_template('show2.html', asset=app.getAssetDataDict(), instrument=app.getInstrumentDatas())
	return render_template('show2.html', asset=app.getAssetDataDict(), instrument=app.getInstrumentDatas())