from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def show():
	return str(app.y[0])
    #return render_template('show.html', json=json)
"""
def run(display_data):
	__display_data = display_data
	app.run()


class DisplayData:

	def __init__(self, records, instrument_datas):
		self.__records = records
		self.__instrument_datas = instrument_datas

	def getRecords(self):
		return self.__records

	def getCompanyDatas(self):
		return self.__instrument_datas

class InstrumentData:

	def __init__(self, instrument, prices, holdings_info):
		self.__instrument = instrument
		self.prices = prices
		self.holdings_info = holdings_info
"""