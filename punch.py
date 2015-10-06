from threading import Thread
from hyphen import Hyphenator, dict_info
from hyphen.dictools import *
from queue import Queue
import os
import pyttsx
from textgenerator import TextGenerator
from pythonosc import osc_message_builder
from pythonosc import udp_client
import argparse
import RPi.GPIO as GPIO
import time

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
			channel = inputQueue.get()
			if channel == 'quit':
				break
			syllable = speaker.get_next_syllable()
			try:
				msg = osc_message_builder.OscMessageBuilder(address = "/punch")
				msg.add_arg(channel)
				msg.add_arg(speaker.generatorName)
				msg.add_arg(syllable)
				msg = msg.build()
				client.send(msg)
				print(speaker.generatorName + ": " + syllable)
				#ttsEngine.say(syllable)
				#ttsEngine.runAndWait()	
			except UnicodeEncodeError:
				print("unicode error")

#setup osc
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="10.0.0.6", help="The ip to listen on")
parser.add_argument("--port", type=int, default=1337, help="the port to listen on")
args = parser.parse_args()

client = udp_client.UDPClient(args.ip, args.port)



#setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

				
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
inputQueue2 = Queue()
speaker1thread = Thread(target = process, args = (textGen1, inputQueue1))
speaker2thread = Thread(target = process, args = (textGen2, inputQueue2))
speaker1thread.start()
print("\n" + worders[worder1] + " ready!")
speaker2thread.start()
print("\n" + worders[worder2] + " ready!")

prev_input1 = 0
prev_input2 = 0

while 1:
	#userInput = input()
	input1 = GPIO.input(24)
	input2 = GPIO.input(25)
	try: 
		if (not prev_input1) and input1:
			inputQueue1.put('1')
		elif (not prev_input2) and input2:
			inputQueue2.put('2')
		#elif userInput == 'quit':
		#	inputQueue1.put('quit')
		#	inputQueue2.put('quit')
		#	quit()
		prev_input1 = input1
		prev_input2 = input2
		time.sleep(0.05)
	except UnicodeEncodeError:
		print("unicode error")
