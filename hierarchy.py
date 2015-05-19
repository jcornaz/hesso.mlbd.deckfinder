import features
import dao
import numpy as np
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist

DISTANCE_METRIC = 'cosine'
LINKAGE_METHOD = 'centroid'

def learn(dataset):
	return hierarchy.linkage(pdist(dataset, DISTANCE_METRIC),LINKAGE_METHOD,DISTANCE_METRIC)

#DEBUG
with dao.Dao() as da:
	cards = da.cards
	decks = da.decks

dataset = np.array(features.exfe_decks(filter(lambda deck: deck.isValidConstructed, decks), cards))

hierarchy.dendrogram(learn(dataset))