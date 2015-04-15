from pymarkovchain import MarkovChain
import os

class TextGenerator:
	def __init__(self, generatorName, trainString, prefixLength):
		self.generatorName = generatorName
		self.chain = MarkovChain()
		self.chain.generateDatabase(trainString, n=prefixLength)
		self.currState = []
		while (len(self.currState) < prefixLength):
			self.currState = self.chain.generateString().split()[-(prefixLength+1):-1]
	
	def get_next_word(self):
		nextword = ""
		try:
			while nextword == "":
				nextword = self.chain._nextWord(self.currState)
				self.currState = self.currState[1:]
				self.currState.append(nextword)
		except UnicodeEncodeError:
			print("unicode error")
		return nextword
		
	def get_next_syllable(self):
		return "nextsyllable"

def load_text_dir_as_string(textDir):
	text = ""
	for file in os.listdir(textDir):
		text = text + open(textDir + "/" + file).read()
	return text
		
wordsDir = os.getcwd() + "/resources/text"
worders = [d for d in os.listdir(wordsDir) if os.path.isdir(os.path.join(wordsDir, d))]

print("In one corner we have:")
for index, worder in enumerate(worders):
	print (str(index + 1) + ": " + worder)
worder1 = int(input()) -1
print("\n" + worders[worder1] + "!!")
print("and in the other corner we have:") 
for index, worder in enumerate(worders):
	print (str(index + 1) + ": " + worder)
worder2 = int(input())-1
print("\n" + worders[worder2] + "!!")
	
textGen1 = TextGenerator(worders[worder1], load_text_dir_as_string(wordsDir + "/" + worders[worder1]), 3)
textGen2 = TextGenerator(worders[worder2], load_text_dir_as_string(wordsDir + "/" + worders[worder2]), 3)
speakers = [textGen1, textGen2]

while 1:
	userInput = input()
	try: 
		if userInput == '1':
			print(speakers[0].generatorName + ": " + speakers[0].get_next_word())
		elif userInput == '2':
			print(speakers[1].generatorName + ": " + speakers[1].get_next_word())
		elif userInput == 'quit':
			quit()
	except UnicodeEncodeError:
		print("unicode error")