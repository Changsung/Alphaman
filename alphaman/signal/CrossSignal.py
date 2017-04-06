from alphaman.signal import BaseSignal, BuySignal
from alphaman.utils import daily, weekly, tech_key

class CrossSignal(BaseSignal):

	__instrument = None

	def __init__(self, instrument):
		self.__instrument = instrument

	def calculateSignal(self):
		sma1 = self.get(self.__instrument, tech_key('Close', 20, 'sma'), daily(-2, 0))
		sma2 = self.get(self.__instrument, tech_key('Close', 60, 'sma'), daily(-2, 0))
		if (sma1[0] > sma2[0]) and (sma1[-1] < sma2[-1]):
			return BuySignal.Short
		elif (sma1[0] < sma2[0]) and (sma1[-1] > sma2[-1]):
			return BuySignal.Long
		else:
			return BuySignal.Hold
