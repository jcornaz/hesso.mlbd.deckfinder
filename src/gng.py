#!/usr/bin/python
import model
import dao
from model import Mechanics
import random
import features as feat
from time import gmtime, strftime

import mdp
import bimdp

#with dao.Dao() as da:
#	cards = da.cards
#	decks = da.decks

def printTime(prefix):
	print (strftime("%H:%M:%S %d-%m-%Y", gmtime())+" "+prefix)
	
def writeDeckListToCSVPoints(filePath,deckList, deckClass):
	with open(filePath+'.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, quotechar=';',quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['class','x','y'])
		for deck,classe in zip(deckList,deckClass):
			spamwriter.writerow([classe,deck[0],deck[1]])

import numpy as np
np.random.seed(0)
mdp.numx_rand.seed(1266090063)

random.seed(0)
def rand_points(number, a, b):
	x = []
	y = []
	for i in range(number):
		x.append([random.uniform(a, b)])
		y.append([random.uniform(a, b)])
	return mdp.numx.concatenate((x,y), axis=1)

raw1 = rand_points(10, 1, 2)
raw2 = rand_points(100, 4, 5)
features = mdp.numx.concatenate([raw1,raw2], axis=0)
features = mdp.numx.take(features,mdp.numx_rand.permutation(features.shape[0]), axis=0)

features = feat.load_dataset_gng()[:]#10'000 met 10 secondes pour write class

printTime("Start GNG")


gng = mdp.nodes.GrowingNeuralGasNode(	max_nodes=2000)
MAX = 10
for i in range(MAX):
	gng.train(features)
	printTime(str(float(i+1)*100.0/MAX)+"%")

gng.stop_training()
	


classes = []

printTime("write classe")
lenConnectGraph = len(gng.graph.connected_components())

print("number of nodes "+str(len(gng.graph.connected_components())))
connect_comp = gng.graph.connected_components()

nearest_neigh = gng.nearest_neighbor(features)[0]

printTime("Start for loop")
for n in nearest_neigh: #TODO c'est quoi la distance dans le [1] ??
	idx = 0
	for val in connect_comp:
		if n in val:
			classes.append(idx)
			break
		elif idx+1==lenConnectGraph:
			raise "no class finded for an input..."
		idx += 1
	
#feat.writeDeckListToCSVPoints("points",features,classes)

with dao.Dao() as da: # TODO pas opti car on le fait deux fois avec load_dataset()
		cards = da.cards
		decks = da.decks
		
decks = filter(lambda deck: deck.isValidConstructed, decks)
printTime("Start write csv")
feat.writeDeckListToCSV("fileNameTest",decks,classes)
