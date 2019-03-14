# Python Program to respond to text based spoken language type commands and generate varied responses
# Also to help organisation!
# NAME = "Alfred"
import os
from os import path																					#Imports and set-up's
import time
import datetime
import calendar
import sqlite3
from sqlite3 import Error
from random import *
from settings import *
from speechChoiceArrays import *
from threading import Thread
#from gtts import gTTS

class Core:
	def __init__(self):
		#initial startup tasks here
		print("Upon initialization;")
		i = randrange(0,len(helloOps))																#Selects random number for respone at the range of 0 to the length of the speech options
		self.currentUpdate()
		self.todo()
		print("")																					#Starts statement cycle of the program, ends initialization
		print(helloOps[i])
		self.checkAlarm()
		t = Thread(target=self.getTime)																#Starts a parallel function in the background that becomes the clock.
		t.start()
		self.input()


	def getTime(self):																				#Used in background clock
		timer = True
		while timer:
			time.sleep(0.8)
			now = datetime.datetime.now()															#Loop running in background constantly updates to the current time
			self.currenttime = now.strftime("%H:%M:%S")
			for i in range (0, len(self.alarmtimes)):
				if self.alarmtimes[i][0] == self.currenttime:
					print(self.alarmname[i][0])
					os.system('glorious.mp3')														#Plays alarm song on detection
			

	def checkAlarm(self):
		cur.execute("SELECT ALARMTIME FROM ALARM");
		self.alarmtimes = cur.fetchall()
		for i in range (0, len(self.alarmtimes)):
			print(self.alarmtimes[i][0])
		cur.execute("SELECT NAME FROM ALARM");
		self.alarmname = cur.fetchall()

	def todo(self):
		day = datetime.datetime.now()
		self.currentday = day.strftime("%A")
		for i in range (0,6):
			if self.currentday == calendar.day_name[i]:
				self.currentdayint = i
		print("Today is "+self.currentday+", sir.")
		cur.execute("SELECT TITLE FROM DAILY WHERE DATEPART='"+self.currentday+"'");
		self.daily = cur.fetchall()
		print("For today, sir, you have: ")
		for i in range (0,len(self.daily)):
			print(str(self.daily[i][0])+".")
		print("Good luck, sir")
		print(day.strftime("%H:%M"))

	def input(self):
		i = randrange(0,len(statementTakingOps))
		self.statment = input(statementTakingOps[i])
		if ("new" in self.statment) and ("alarm" in self.statment):
			print("TEST2")
			self.newAlarm()
		if ("remove" in self.statment) and ("alarm" in self.statment):
			print("TEST1")
			self.delAlarm()
		if "what" and "time" in self.statment:														#Checks part of input for parameters
			self.currentUpdate()
			self.input()
		for i in range (0,len(couldOps)):															#Checks for all versions of "could"
			if (str(couldOps[i]) or "what") and "your" and "name" in self.statment:					# >> FIX ALL STATEMENT LOGIC <<
				self.introduce()
				self.input()
			if (str(couldOps[i]) or "what") and "your" and "introduce" in self.statment:
				self.introduce()
				self.input()
		if ("new" or "make") and "event" in self.statment:
			self.newEvent()
		if "new" and "daily" in self.statment:
			self.newReminder()
		os.system('cls')
		self.input()

	def newEvent(self):
		self.title = input("What for, sir? ")													#>>GIVE ALL OPTIONS<<
		self.date = str(input("And when will this be for? "))
		self.who = input("With anyone in particular? ")
		if "no" in self.who:
			self.who = "NULL"
		self.desc = input("Would you like to add a description? ")
		if "no" in self.desc:
			self.desc = "NULL"
		self.more = input("Will there be anything else, sir? ")
		conn.execute("INSERT INTO EVENTS (TITLE,DATEPART,DESCRIPTION) \
			VALUES ('"+self.title+"','"+self.date+"','"+self.desc+"')");							#WORKING ON EVENT FORGING - Currently adds events to database
		conn.commit()
		print(yesWillDoOps[randrange(0,len(yesWillDoOps))])
		self.input()

	def currentUpdate(self):
		now = datetime.datetime.now()
		i = randrange(0,len(timeUpdateOps))
		print("The current date and time "+timeUpdateOps[i]+":"+now.strftime("%Y-%m-%d %H:%M"))

	def introduce(self):
		print(helloOps[randrange(0,len(helloOps))]+nameOps[randrange(0,len(nameOps))]+NAME+"!")

	def newReminder(self):
		self.title = input("What is the title sir? ")
		self.day = input("What day for, sir? ")
		self.time = input("Would you like to set a time? ")
		if "no" in self.time:
			self.time = "NULL"
		conn.execute("INSERT INTO DAILY (TITLE, DATEPART, TIMEPART) \
			VALUES('"+self.title+"','"+self.day+"','"+self.time+"')");
		conn.commit()
		print("New daily reminder created for "+self.day+", sir.")

	def newAlarm(self):
		self.alName = input("What's the alarm name? ")
		self.alTime = input("Time for alarm? ")
		conn.execute("INSERT INTO ALARM (NAME, ALARMTIME) \
			VALUES('"+self.alName+"','"+self.alTime+":00')");
		conn.commit()

	def delAlarm(self):
		self.delAl = input("Which alarm would you like to remove, sir? ")
		conn.execute("DELETE FROM ALARM WHERE NAME='"+self.delAl+"'");
		conn.commit()
		print("Done, sir")

conn = sqlite3.connect('storage.db')																	#Database Initialization
cur = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS EVENTS
		(ID INTEGER PRIMARY KEY		NOT NULL,
		TITLE 			TEXT 	NOT NULL,
		DATEPART 		TEXT 	NOT NULL,
		DESCRIPTION 	CHAR(150),
		WITH 			CHAR(30),
		ADDRESS			CHAR(250));''')	#For making new databases
conn.execute('''CREATE TABLE IF NOT EXISTS DAILY
		(ID INTEGER PRIMARY KEY		NOT NULL,
		TITLE 			TEXT 	NOT NULL,
		DATEPART 		TEXT 	NOT NULL,
		TIMEPART 		TEXT);''')
conn.execute('''CREATE TABLE IF NOT EXISTS ALARM
		(ID INTEGER PRIMARY KEY		NOT NULL,
		NAME 			TEXT 	NOT NULL,
		ALARMTIME 		TEXT 	NOT NULL);''')

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