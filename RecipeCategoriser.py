# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:16:24 2017

@author: mzent
"""

from textblob.classifiers import NaiveBayesClassifier

from textblob import TextBlob
import csv
import cPickle as pickle

classifiers = []
for prefix in ["ind","chi","fre","gre","mex","ita","tha"]:
	train = []
	test = []
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

print "Trained all classifiers, loading untagged data."

full = []
with open('notTaggedData.csv', "rb") as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		full.append((row[0] + ": " + row[2],row[3]))

print "Data loaded, predicting classes for whole dataset."

with open("CombinedOutput.csv","wb") as ofile:
	writer = csv.writer(ofile)
	for recipe in full:
		print recipe,
		classes = [recipe[0]]
		for cl in classifiers:
			classes.append(cl.prob_classify(recipe[0]).max())
		print recipe
		print "****    " + classes
		writer.writerow(classes)