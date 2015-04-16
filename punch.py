from pymarkovchain import MarkovChain
from threading import Thread
from queue import Queue
import os
import pyttsx

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
	for filename in os.listdir(textDir):
		#print(filename)
		file = open(textDir + "/" + filename)
		linetext = "\n"
		while linetext != "":
			try:
				linetext = file.readline()
			except UnicodeDecodeError:
				print("unicode decode error")
				linetext = " "
			text += linetext				
	return text
	
def process(speaker, inputQueue):
	#ttsEngine = pyttsx.init()

	while True:
		if not inputQueue.empty():
			if inputQueue.get() == 'quit':
				break
			word = speaker.get_next_word()
			try:
				print(speaker.generatorName + ": " + word)
				#ttsEngine.say(word)
				#ttsEngine.runAndWait()	
			except UnicodeEncodeError:
				print("unicode error")
		
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

inputQueue1 = Queue()
speaker1thread = Thread(target = process, args = (textGen1, inputQueue1))
inputQueue2 = Queue()
speaker2thread = Thread(target = process, args = (textGen2, inputQueue2))
speaker1thread.start()
print("\n" + worders[worder1] + " ready!")
speaker2thread.start()
print("\n" + worders[worder2] + " ready!")

while 1:
	userInput = input()
	try: 
		if userInput == '1':
			inputQueue1.put('1')
		elif userInput == '2':
			inputQueue2.put('2')
		elif userInput == 'quit':
			inputQueue1.put('quit')
			inputQueue2.put('quit')
			quit()
	except UnicodeEncodeError:
		print("unicode error")
