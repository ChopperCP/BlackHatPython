# encoding=utf8
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random


# Payload generator
class Fuzzer(IIntruderPayloadGenerator):
	def __init__(self, extender, attack):
		self._extender = extender
		self._helpers = extender._helpers
		self._attack = attack
		self.max_payloads = 10
		self.cnt_iterations = 0

		return

	def hasMorePayloads(self):  # type: () -> bool
		if self.cnt_iterations <= self.max_payloads:
			return True
		else:
			return False

	def getNextPayload(self, baseValue):  # type: (bytearray) -> bytearray
		# baseValue is the stuff between §   §
		payload = "".join(chr(b) for b in baseValue)

		# Mutate the payload
		payload = self.mutate_payload(payload)

		self.cnt_iterations += 1
		return payload

	def reset(self):
		self.cnt_iterations = 0
		return

	def mutate_payload(self, original_payload):
		# choose a random mutating method
		picker = random.randint(1, 1)
		payload = ""

		if picker == 1:
			payload += "index.html"

		return payload


# All Extender must implement
class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
	# Factory class, produce a payload generator
	def registerExtenderCallbacks(self, callbacks):  # type: (IBurpExtenderCallbacks) -> ()
		self._callbacks = callbacks
		self._helpers = callbacks.getHelpers()

		callbacks.registerIntruderPayloadGeneratorFactory(self)
		return

	def getGeneratorName(self):  # type: () -> str
		return "Fuzzer Generator"

	def createNewInstance(self, attack):  # type: (IIntruderAttack) -> IIntruderPayloadGenerator
		return Fuzzer(self, attack)
