import os
import json
from datetime import datetime
import tkinter as tk

# functionality
os.chdir("inbox")
directories = os.listdir()

name = input("Please input your name as on Facebook: (ex: Joe Smith)\n")
choice = input("Input 1 for total message count, 2 for individual breakdown of each person.\n")

yearAndMonth = {}
for each in directories:
	if each[0] == ".":
		continue
	os.chdir(each)
	temp = os.listdir()
	allFiles = [name for name in temp if name[-4:] == "json"]

	for eachFile in allFiles:
		file = open(eachFile, "r")
		data = json.loads(file.read())

		if len(data["participants"]) > 2:
			continue

		person = [x["name"] for x in data["participants"] if x["name"] != name]
		if len(person) > 0:
			person = person[0]
		else:
			continue
		for msg in data["messages"]:
			date = datetime.fromtimestamp(msg["timestamp_ms"]/1000)
			month = str(date.month) if len(str(date.month)) == 2 else "0" + str(date.month)
			monthYear = month + "/" + str(date.year)
			sender = msg["sender_name"]
			if monthYear not in list(yearAndMonth.keys()):
				yearAndMonth[monthYear] = {person: {"You": 1, "Them": 0}} if sender == name else {person: {"You": 0, "Them": 1}}
			elif person not in list(yearAndMonth[monthYear].keys()):
				yearAndMonth[monthYear][person] = {"You": 1, "Them": 0} if sender == name else {"You": 0, "Them": 1}
			elif sender == name:
				yearAndMonth[monthYear][person]["You"] += 1
			else:
				yearAndMonth[monthYear][person]["Them"] += 1

	os.chdir("..")

allMonths = sorted(list(yearAndMonth.keys()), key = lambda x: (int(x[-4:]), int(x[0:2])))
sumDict = yearAndMonth
for key in yearAndMonth.keys():
	for personKey in yearAndMonth[key].keys():
		sumDict[key][personKey] = yearAndMonth[key][personKey]["You"] + yearAndMonth[key][personKey]["Them"]

def totalMsg(month):
	sortPpl = {x:y for x,y in sorted(sumDict[month].items(), key=lambda item: item[1], reverse = True)}
	return sortPpl

def eachMsg(month):
	sortPpl = {x:y for x,y in sorted(yearAndMonth[month].items(), key=lambda item: item[1]["You"] + item[1]["Them"], reverse = True)}
	return sortPpl

# tkinter display setup
height, width = 500, 500

index, end = 0, len(allMonths) - 1

root = tk.Tk()
root.title("Facebook Message Analyzer")

canvas = tk.Canvas(root, height = height, width = width)
canvas.pack()

frame = tk.Frame(root, bg = '#CFFFF7')
frame.place(relwidth = 1, relheight = 1)

display = tk.Label(frame, text = "", bg = 'light blue', wraplength = 490)
display.place(relx = 0.01, rely = 0.01, relwidth = .98, relheight = 0.7)

def arrows(direction):
	global index, end
	if direction == "right" and index < end:
		index += 1
	elif direction == "left" and index > 0:
		index -= 1
	date = allMonths[index]
	info = str(totalMsg(date))
	update(info, date)

def update(info, date):
	currDate.config(text = date)
	display.config(text = info)

rightArrow = tk.Button(frame, text = ">", command = lambda: arrows("right"))
rightArrow.place(relx = 0.75, rely = 0.8, relwidth = 0.15, relheight = 0.1)

leftArrow = tk.Button(frame, text = "<", command = lambda: arrows("left"))
leftArrow.place(relx = 0.1, rely = 0.8, relwidth = 0.15, relheight = 0.1)

currDate = tk.Label(frame, text = "", bg = '#CFFFF7')
currDate.place(relx = 0.35, rely = 0.78, relwidth = .3, relheight = 0.15)

currDate.config(text = allMonths[0])
display.config(text = str(totalMsg(allMonths[0])))

root.mainloop()
