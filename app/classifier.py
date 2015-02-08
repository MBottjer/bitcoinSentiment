import nltk
import json
import csv

class Classifier():

	def __init__(self):
		self.posDictionary = dict()
		self.neutDictionary = dict()
		self.negDictionary = dict()

		self.positive = 0.0
		self.neutral = 0.0
		self.negative = 0.0

	def handleWord(self, word, label):
		if label == "p":
			print '\t' + word + 'is POSITIVE'
			if self.posDictionary.has_key(word):
				self.posDictionary[word] = str(int(self.posDictionary[word]) + 1)
			else: 
				self.posDictionary[word] = str(1)
			
		elif label == "d":
			print '\t' + word + 'is NEUTRAL'
			if self.neutDictionary.has_key(word):
				self.neutDictionary[word] = str(int(self.neutDictionary[word]) + 1)
			else: 
				self.neutDictionary[word] = str(1)

		elif label == "n":
			print '\t' + word + 'is NEGATIVE'
			if self.negDictionary.has_key(word):
				self.negDictionary[word] = str(int(self.negDictionary[word]) + 1)
			else: 
				self.negDictionary[word] = str(1)

	def train(self, pathToTestFile):
		lines = open(pathToTestFile).read().splitlines()
		for line in lines:
			print line
			lineArray = line.split(',')
			label = lineArray[0]
			text = lineArray[1]

			words = line.split(' ')

			for word in words:
				self.handleWord(word, label)

	def runSingle(self, tweet):

		self.positive = 0.0
		self.neutral = 0.0
		self.negative = 0.0
		
		words = tweet.split(' ')
		print 'Tweet is ' + tweet
		size = len(words)
		print 'size is ' + str(size)
		

		for word in words:
			if self.posDictionary.has_key(word):
				# print 'Has positive'
				self.positive += int(self.posDictionary[word])	
				# print 'self.posDictionary[word] = ' + self.posDictionary[word]

			if self.neutDictionary.has_key(word):
				# print "Has neutral"
				self.neutral += int(self.neutDictionary[word]) 
				# print 'self.neutDictionary[word] = ' + self.neutDictionary[word]

			if self.negDictionary.has_key(word):
				# print 'Has negative'
				self.negative += int(self.negDictionary[word])
				# print 'self.negDictionary[word] = ' + self.negDictionary[word]
				
		self.positive /= size
		self.neutral /= size
		self.negative /= size

		print '\tpositive ' + str(self.positive)
		print '\tneutral ' + str(self.neutral)
		print '\tnegative ' + str(self.negative)

	def replaceTwoOrMore(s):
	    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	    return pattern.sub(r"\1\1", s)

	def getStopWordList(stopWordListFileName):
	    stopWords = []
	    stopWords.append('AT_USER')
	    stopWords.append('URL')

	    fp = open(stopWordListFileName, 'r')
	    line = fp.readline()
	    while line:
	        word = line.strip()
	        stopWords.append(word)
	        line = fp.readline()
	    fp.close()
	    return stopWords

	def runFromFile(self, pathToFile):
		listOfClassifiedTweets = list()

		lines = open(pathToFile).read().splitlines()
		for line in lines:
			if line == "":
				pass
			else:
				text = json.loads(line)['text']
				timeStamp = json.loads(line)['created_at']
				self.runSingle(text)
				print text
				listOfClassifiedTweets.append([timeStamp, text, self.positive, self.neutral, self.negative])

		return listOfClassifiedTweets

myClassifier = Classifier()
myClassifier.train('labelledTweets.csv')
tweets = myClassifier.runFromFile('twitDB.csv')
print json.dumps(tweets)