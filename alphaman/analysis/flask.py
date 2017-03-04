from flask import render_template
from flask import Flask


app = Flask(__name__)

__display_data = None


@app.route("/")
def show():
    return render_template('show.html', name=name)

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