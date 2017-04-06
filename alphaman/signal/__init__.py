from enum import Enum

class BuySignal(Enum):
	Short 	= 0
	Long 	= 1
	Hold 	= 2

class BaseSignal:

	__strategy = None

	def setStrategy(self, strategy):
		self.__strategy = strategy

	def getSignal(self):
		return self.calculateSignal()

	def calculateSignal(self):
		raise NotImplementedError()

	def get(self, instrument, key, date_idx):
		return self.__strategy.get(instrument, key, date_idx)
