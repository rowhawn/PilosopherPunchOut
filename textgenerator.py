from pymarkovchain import MarkovChain
from queue import Queue
from hyphen import Hyphenator, dict_info
from hyphen.dictools import *
import re


class TextGenerator:
	def __init__(self, generatorName, trainString, prefixLength):
		self.generatorName = generatorName
		self.chain = MarkovChain()
		self.chain.generateDatabase(trainString, n=prefixLength)
		self.currState = []
		self.hyphenator = Hyphenator('en_US')
		self.syllableQ = Queue()
		self.stripPattern = re.compile('[\W_]+')
		while (len(self.currState) < prefixLength):
			self.currState = self.chain.generateString().split()[-(prefixLength+1):-1]
	
	def load_next_word(self):
		nextword = ""
		try:
			while nextword == "":
				nextword = self.stripPattern.sub('', self.chain._nextWord(self.currState))
				self.currState = self.currState[1:]
				self.currState.append(nextword)
			if len(nextword) < 4:
				self.syllableQ.put(nextword)
			else: 
				for syllable in self.hyphenator.syllables(nextword):
					self.syllableQ.put(syllable)
		except UnicodeEncodeError:
			print("unicode error")
		
	def get_next_syllable(self):
		if (self.syllableQ.empty()):
			self.load_next_word()
		return self.syllableQ.get()