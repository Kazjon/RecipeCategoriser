# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:21:44 2017

@author: mzent
"""
import csv

ofile = open('strippedData.csv', "w", encoding="utf8", newline='')
writer = csv.writer(ofile)

data = []
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_',' ']
i = 0
with open('OutputRecipes.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        recipe = []
        recipe.append(row[2][7:])
        recipe.append(row[1][11:])
        string = ""
        for c in row[4]:
            if c in alphabet:
                string = string + c
        ingredients = ""
        for s in string.split():
            if(len(s) > 2):
                ingredients = ingredients + s + " "
        recipe.append(ingredients[:-1])
        writer.writerow(recipe)
        i+=1
        if(i%1000 == 0): 
            print(i)
        
ofile.close()