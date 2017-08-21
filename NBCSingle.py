# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:16:24 2017

@author: mzent
"""

from textblob.classifiers import NaiveBayesClassifier

from textblob import TextBlob
import csv
import cPickle as pickle


train = []
test = []
full = []
classifiers = []
for prefix in ["ind","chi","fre","gre","mex","ita","tha"]:
	with open(prefix+'TrainData.csv', "rb") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			train.append((row[0] + ": " + row[2],row[3]))

	with open(prefix+'TestData.csv', "rb") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			test.append((row[0] + ": " + row[2],row[3]))

	print("Read data for " + prefix)

	cl = NaiveBayesClassifier(train)
	pickle.dump(cl,open(prefix+"Classifier.pkl","wb"))

	#Compute accuracy
	print "Model trained for " + prefix + ". Accuracy:" + str(cl.accuracy(test))

	print "Most informative features for " + prefix + ":"
	# Show 100 most informative features
	cl.show_informative_features(50)
	classifiers.append(cl)

with open('notTaggedData.csv', "rb") as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		full.append((row[0] + ": " + row[2],row[3]))

with open("CombinedOutput.csv","wb") as ofile:
	writer = csv.writer(ofile)
	for recipe in test:
		print recipe,
		classes = [recipe[0]]
		for cl in classifiers:
			classes.append(cl.prob_classify(recipe[0]).max())
		print recipe
		print "****    " + classes
		writer.writerow(classes)
"""
cl1 = pickle.load(open("serialNBCChinese.pickle","rb"))#read PICKLE file of model
cl2 = pickle.load(open("serialNBCFrench.pickle","rb"))
cl3 = pickle.load(open("serialNBCGreek.pickle","rb"))
cl4 = pickle.load(open("serialNBCIndian.pickle","rb"))
cl5 = pickle.load(open("serialNBCItalian.pickle","rb"))
cl6 = pickle.load(open("serialNBCMexican.pickle","rb"))
cl7 = pickle.load(open("serialNBCThai.pickle","rb"))
classifiers = [cl1,cl2,cl3,cl4,cl5,cl6,cl7]
print("created classifier")

ofile = open('chiClassified.csv', "w", encoding="latin-1", newline='')
writer = csv.writer(ofile)
count = 0
for recipe in full:
	classes = [recipe[0]]
	for cl in classifiers:
		classes.append(cl.prob_classify(recipe[0]).max())
	#print(classes)
	writer.writerow(classes)
	count+=1
	if(count%100 == 0):
		print(count)
	
ofile.close()
# Compute accuracy
#print("Accuracy: {0}".format(cl.accuracy(test)))

# Show 100 most informative features
##cl.show_informative_features(100)

#pickle.dump(cl,open( "serialNBCIndian.pickle", "wb" ))
"""