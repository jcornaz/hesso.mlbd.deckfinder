#!/usr/bin/python
import model
import dao
from model import Mechanics
import random

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

raw1 = rand_points(100, 1, 2)
raw2 = rand_points(100, 110, 100)
features = mdp.numx.concatenate([raw1,raw2], axis=0)
features = mdp.numx.take(features,mdp.numx_rand.permutation(features.shape[0]), axis=0)

for v in features:
	print v
gng = mdp.nodes.GrowingNeuralGasNode(max_nodes=100000)
gng.train(features)
gng.stop_training()

n_obj = len(gng.graph.connected_components())
print n_obj
	

