# Python Program to respond to text based spoken language type commands and generate varied responses
# Also to help organisation!
# NAME = ""
from os import path																					#Imports and set-up's
import time
import datetime
from random import *
from settings import *
from speechChoiceArrays import *
class Core:
	def __init__(self):
		#initial startup tasks here
		print("Upon initialization;")
		i = randrange(0,len(helloOps))																#Selects random number for respone at the range of 0 to the length of the speech options
		self.currentUpdate()

		print("")																					#Starts statement cycle of the program, ends initialization
		print(helloOps[i])
		self.input()

	def input(self):
		i = randrange(0,len(statementTakingOps))
		self.statment = input(statementTakingOps[i])
		if "what" and "time" in self.statment:														#Checks part of input for parameters
			self.currentUpdate()
			self.input()
		for i in range (0,len(couldOps)):															#Checks for all versions of "could"
			if (str(couldOps[i]) or "what") and "your" and "name" in self.statment:
				self.introduce()
				self.input()
			if (str(couldOps[i]) or "what") and "your" and "introduce" in self.statment:
				self.introduce()
				self.input()
		input("Error")
	def currentUpdate(self):
		now = datetime.datetime.now()
		i = randrange(0,len(timeUpdateOps))
		print("The current date and time",timeUpdateOps[i],":",now.strftime("%Y-%m-%d %H:%M"))
	def introduce(self):
		print(helloOps[randrange(0,len(helloOps))],nameOps[randrange(0,len(nameOps))],NAME,"!")
c = Core()		