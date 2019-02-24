# Python Program to respond to text based spoken language type commands and generate varied responses
# Also to help organisation!
# NAME = "Alfred"
from os import path																					#Imports and set-up's
import time
import datetime
import sqlite3
from sqlite3 import Error
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
		self.idnum = "1"
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
		if ("new" or "make") and "event" in self.statment:
			self.title = input("What for, sir? ")
			self.date = str(input("And when will this be for? "))
			self.who = input("With anyone in particular? ")
			if "no" in self.who:
				self.who = "NULL"
			self.more = input("Will there be anything else, sir? ")
			conn.execute("INSERT INTO EVENTS (ID,TITLE,DATEPART) \
				VALUES ("+self.idnum+",'"+self.title+"','"+self.date+"')");							#WORKING ON EVENT FORGING - Currently adds events to database
			conn.commit()
			print(yesWillDoOps[randrange(0,len(yesWillDoOps))])
		input("Error with statement")
	def currentUpdate(self):
		now = datetime.datetime.now()
		i = randrange(0,len(timeUpdateOps))
		print("The current date and time",timeUpdateOps[i],":",now.strftime("%Y-%m-%d %H:%M"))
	def introduce(self):
		print(helloOps[randrange(0,len(helloOps))],nameOps[randrange(0,len(nameOps))],NAME,"!")

conn = sqlite3.connect('storage.db')																	#Database Initialization
"""conn.execute('''CREATE TABLE EVENTS
		(ID INT PRIMARY KEY		NOT NULL,
		TITLE 			TEXT 	NOT NULL,
		DATEPART 			TEXT 	NOT NULL,
		DESCRIPTION 	CHAR(50),
		WITH 			CHAR(30),
		ADDRESS			CHAR(250));''')"""	#For making new databases

c = Core()
""" TO-DO
>	Impliment speech recognition
>	Create constant time check for dates and times (possibly using update)
>	Add function to create dates to be informed of.
>	Store dates in database? - SQL for python? - More likely MYSQLite (As is already imported) < DONE - NEEDS TWEAKING
>	Make alarm feature - if time = alarm variable, fire alartm function which plays music until a given input - have multiple, easy set alarms
>	Add Daily description of events - Queries databse for all events on current day upon startup? - Puts events into variables for later use?
"""
conn.close()