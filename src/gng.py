#!/usr/bin/python
import model
import dao
from model import Mechanics
import random
import features as feat

import mdp
import bimdp

#with dao.Dao() as da:
#	cards = da.cards
#	decks = da.decks

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
raw2 = rand_points(100, -110, -100)
features = mdp.numx.concatenate([raw1,raw2], axis=0)
features = mdp.numx.take(features,mdp.numx_rand.permutation(features.shape[0]), axis=0)

features = feat.load_dataset()

gng = mdp.nodes.GrowingNeuralGasNode(max_nodes=1000)
gng.train(features)

classes = []

for n in gng.nearest_neighbor(features)[0]: #TODO c'est quoi la distance dans le [1] ??
	for idx, val in enumerate(gng.graph.connected_components()):
		if n in val:
			classes.append(idx)
			break
		elif idx+1==len(gng.graph.connected_components()):
			raise "no class finded for an input..."
			
n_obj = len(gng.graph.connected_components())
print n_obj

with dao.Dao() as da: # TODO pas opti car on le fait deux fois avec load_dataset()
		cards = da.cards
		decks = da.decks
feat.writeDeckListToCSV("fileNameTest",decks,classes)

