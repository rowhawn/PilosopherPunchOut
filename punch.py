from threading import Thread
from hyphen import Hyphenator, dict_info
from hyphen.dictools import *
from queue import Queue
import os
import pyttsx
from textgenerator import TextGenerator

def load_text_dir_as_string(textDir):
	text = ""
	for filename in os.listdir(textDir):
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
			syllable = speaker.get_next_syllable()
			try:
				print(speaker.generatorName + ": " + syllable)
				#ttsEngine.say(syllable)
				#ttsEngine.runAndWait()	
			except UnicodeEncodeError:
				print("unicode error")

#install english hyphenator dictionary if necessary
if not is_installed("en_US"): install("en_US")				
				
#read resources directory to determine list of worders				
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
