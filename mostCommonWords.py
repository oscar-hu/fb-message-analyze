import os
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

os.chdir("inbox")
directories = os.listdir()

uniqueWord = {}
overallSentiment = 0
msgCount = 0
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
					overallSentiment += sentimentScores(msg["content"])
					msgCount += 1

					words = msg["content"].split()	
					for word in words:
						if word in uniqueWord:
							uniqueWord[word] += 1
						else:
							uniqueWord[word] = 1
				except:
					pass
	os.chdir("..")

if __name__ == "__main__":
	uniqueWord = {x:y for x,y in sorted(uniqueWord.items(), key = lambda item: item[1])}
	sentiment = overallSentiment / msgCount
	print("The average sentiment in all your messages tends to be " + scoreAnalysis(sentiment))
	print(uniqueWord)



def sentimentScores(sentence): 
    sent_obj = SentimentIntensityAnalyzer() 
    dictionary = sent_obj.polarity_scores(sentence) # dict has 'neg', 'pos', and 'neu'
    
    # print("Overall sentiment is : ", sent_dict)
    # print("Rating", end = " ")
    return dictionary['compound']

def scoreAnalysis(score):
  
    if score >= 0.05: 
        return "Positive"
    elif score <= - 0.05: 
        return "Negative"
    else: 
        return "Neutral"