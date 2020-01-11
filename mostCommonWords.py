import os
import json

os.chdir("inbox")
directories = os.listdir()

uniqueWord = {}
for each in directories:
	if each[0] == ".":
		continue
	os.chdir(each)
	temp = os.listdir()
	allFiles = [name for name in temp if name[-4:] == "json"]

	for eachFile in allFiles:
		file = open(eachFile, "r")
		data = json.loads(file.read())

		for msg in data["messages"]:
			if msg["sender_name"] == "Oscar Hu":
				words = []
				try:
					words = msg["content"].split()	
					for word in words:
						if word in uniqueWord:
							uniqueWord[word] += 1
						else:
							uniqueWord[word] = 1
				except:
					pass
	os.chdir("..")

uniqueWord = {x:y for x,y in sorted(uniqueWord.items(), key=lambda item: item[1])}
print(uniqueWord)