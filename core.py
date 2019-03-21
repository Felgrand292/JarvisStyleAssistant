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
		self.checkEvent()
		t = Thread(target=self.getTime)																#Starts a parallel function in the background that becomes the clock.
		t.start()
		self.input()


	def getTime(self):																				#Used in background clock
		timer = True
		while timer:
			time.sleep(0.8)
			now = datetime.datetime.now()															#Loop running in background constantly updates to the current time
			self.currenttime = now.strftime("%H:%M:%S")
			for i in range (0, len(self.onAlarmTimes)):
				if self.onAlarmTimes[i][0] == self.currenttime:
					os.system('glorious.mp3')														#Plays alarm song on detection
			

	def checkAlarm(self):
		cur.execute("SELECT ALARMTIME FROM ALARM");
		self.alarmtimes = cur.fetchall()
		cur.execute("SELECT ALARMTIME FROM ALARM WHERE SETTING='1'");
		self.onAlarmTimes = cur.fetchall()
		cur.execute("SELECT NAME FROM ALARM WHERE SETTING='1'");
		self.onAlarmNames = cur.fetchall()
		cur.execute("SELECT NAME FROM ALARM");
		self.alarmname = cur.fetchall()
		for i in range (0, len(self.alarmtimes)):
			print(self.alarmtimes[i][0]+"	"+self.alarmname[i][0])

	def checkEvent(self):
		cur.execute("SELECT TITLE FROM EVENTS WHERE DATEPART='"+self.currentday+"'");
		self.todaysEvents = cur.fetchall()
		cur.execute("SELECT TITLE FROM EVENTS");
		self.allTodaysEvents = cur.fetchall()

	def todo(self):
		day = datetime.datetime.now()
		self.currentday = day.strftime("%A")
		for i in range (0,6):
			if self.currentday == calendar.day_name[i]:
				self.currentdayint = i
		print("Today is "+self.currentday+", sir.")
		cur.execute("SELECT TITLE FROM DAILY WHERE DATEPART='"+self.currentday+"'");
		self.daily = cur.fetchall()
		if len(self.daily) != 0:
			print("For today, sir, you have: ")
			for i in range (0,len(self.daily)):
				print(str(self.daily[i][0])+".")
			print("Good luck, sir")
			print(day.strftime("%H:%M"))
		if len(self.daily) == 0:
			print("No daily tasks for today, sir! ")

	def input(self):
		i = randrange(0,len(statementTakingOps))
		self.statment = input(statementTakingOps[i])
		#self.statmentlist = self.prestatment.split(' ')											# >> FOR SPLITTING INPUT INTO LIST <<
		if ("turn" in self.statment) and ("alarm" in self.statment):
			for i in range (0, len(self.alarmtimes)):
				if self.alarmname[i][0] in self.statment:
					if "on" in self.statment:
						print("POINT 3")
						conn.execute("UPDATE ALARM SET SETTING='1' WHERE NAME='"+self.alarmname[i][0]+"'");
						conn.commit()
					if "off" in self.statment:
						conn.execute("UPDATE ALARM SET SETTING='0' WHERE NAME='"+self.alarmname[i][0]+"'");
						conn.commit()

		if ("what" in self.statment) and (("todo" in self.statment) or ("to do" in self.statment) or ("on" in self.statment)):
			self.todo()
		if ("new" in self.statment) and ("alarm" in self.statment):
			self.newAlarm()
		if ("remove" in self.statment or "delete" in self.statment) and ("alarm" in self.statment):
			self.delAlarm()
		if ("what" in self.statment) and ("time" in self.statment):														#Checks part of input for parameters
			self.currentUpdate()
			self.input()
		for i in range (0,len(couldOps)):															#Checks for all versions of "could"
			if (str(couldOps[i]) in self.statment or "what" in self.statment) and "your" in self.statment and ("name" in self.statment or "introduce" in self.statment):					# >> FIX ALL STATEMENT LOGIC <<
				self.introduce()
				self.input()
		if ("new" in self.statment or "make" in self.statment) and "event" in self.statment:
			self.newEvent()
		if "new" and "daily" in self.statment:
			self.newReminder()
		if ("remove" in self.statment or "delete" in self.statment) and ("event" in self.statment):
			self.delEvent()
		print("Restarting ")
		print("")
		self.checkAlarm()
		self.checkEvent()
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
		print("The current date and time "+timeUpdateOps[i]+":"+now.strftime("%d/%m/%Y %H:%M"))

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
		conn.execute("INSERT INTO ALARM (NAME, ALARMTIME, SETTING) \
			VALUES('"+self.alName+"','"+self.alTime+":00', 1)");
		conn.commit()

	def delAlarm(self):
		for i in range (0, len(self.alarmname)):
			if self.alarmname[i][0] in self.statment:
				self.delAl = self.alarmname[i][0]#input("Which alarm would you like to remove, sir? ")
				conn.execute("DELETE FROM ALARM WHERE NAME='"+self.delAl+"'");
				conn.commit()
				print("Done, sir")

	def delEvent(self):
		for i in range (0, len(self.allTodaysEvents)):
			if self.allTodaysEvents[i][0] in self.statment:
				self.delEv = self.allTodaysEvents[i][0]#input("Which event would you like to remove, sir? ")
				conn.execute("DELETE FROM EVENTS WHERE TITLE='"+self.delEv+"'");
				conn.commit()
				print("Done, sir")

	def selfDelEvent(self, event):
		now = datetime.datetime.now()
		conn.execute("DELETE FROM EVENTS WHERE TITLE='"+event+"' AND DATEPART='"+now.strtime("%d/%m/%Y")+"'");



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
		ALARMTIME 		TEXT 	NOT NULL,
		SETTING			INT);''')

c = Core()
""" TO-DO
>	Impliment speech recognition
>	Add notifaction for time in Events, if a time has been set
>	Add function to create dates to be informed of.
>	Output todays events and have the ability to ask for the description
>	Consider adding Bag-Of Words style word processing to allow for single stage commands
>	Add Daily description of events - Queries databse for all events on current day upon startup? - Puts events into variables for later use?
"""
conn.close()