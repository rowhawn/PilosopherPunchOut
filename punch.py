from pymarkovchain import MarkovChain

class TextGenerator:
	def __init__(self, generatorName, trainString):
		self.generatorName = generatorName
		self.chain = MarkovChain()
		self.chain.generateDatabase(trainString, n=3)
		self.currState = []
		while (len(self.currState) < 2):
			self.currState = self.chain.generateString().split()[-3:-1]
	
	def get_next_word(self):
		nextword = ""
		try: 
			nextword = self.chain._nextWord((self.currState[0], self.currState[1]))
			self.currState = [self.currState[1], nextword]
		except UnicodeEncodeError:
			print("unicode error")
		return nextword
		
	def get_next_syllable(self):
		return "nextsyllable"
		
text1 = open("C:\\Users\\dc9169\\Documents\\GitHub\\PilosopherPunchOut\\resources\\text\\prideandprejudice.txt").read()
text2 = open("C:\\Users\\dc9169\\Documents\\GitHub\\PilosopherPunchOut\\resources\\text\\huckleberryfinn.txt").read()

prideGen = TextGenerator("pride", text1)
huckGen = TextGenerator("huck", text2)
speakers = [prideGen, huckGen]
while 1:
	userInput = input()
	try: 
		if userInput == '1':
			print(speakers[0].generatorName + ": " + speakers[0].get_next_word())
		elif userInput == '2':
			print(speakers[1].generatorName + ": " + speakers[1].get_next_word())
	except UnicodeEncodeError:
		print("unicode error")