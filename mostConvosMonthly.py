import os
import json
from datetime import datetime

os.chdir("inbox")
directories = os.listdir()

name = input("Please input your name: (ex: Oscar Hu) \n")
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

def totalMsg():
	sumDict = yearAndMonth
	for key in yearAndMonth.keys():
		for personKey in yearAndMonth[key].keys():
			sumDict[key][personKey] = yearAndMonth[key][personKey]["You"] + yearAndMonth[key][personKey]["Them"]
	for month in allMonths:
		sortPpl = {x:y for x,y in sorted(sumDict[month].items(), key=lambda item: item[1], reverse = True)}
		print(month, sortPpl, "\n\n")

def eachMsg():
	for month in allMonths:
		sortPpl = {x:y for x,y in sorted(yearAndMonth[month].items(), key=lambda item: item[1]["You"] + item[1]["Them"], reverse = True)}
		print(month, sortPpl, "\n\n")

if int(choice) == 1:
	totalMsg()
else:
	eachMsg()

