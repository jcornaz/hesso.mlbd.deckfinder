from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
import features
import numpy as np
import utils

def learn(dataset,epsvalue):
	db = DBSCAN(eps=epsvalue,metric=cosine_distances).fit(dataset)
	labels = db.labels_
	core_samples_mask = np.zeros_like(labels, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	nblabels = len(set(labels)) - (1 if -1 in labels else 0)
	return labels, nblabels, core_samples_mask
	
def main():
	dataset = utils.random_subset(features.load_dataset(),1000)

	epsvalue = 0.1
	print 'learning with eps=' + str(epsvalue) + '...'
	_, nblabels, _ = learn(dataset, epsvalue)
	while nblabels <= 1:
		epsvalue /= 2
		print 'learning with eps=' + str(epsvalue) + '...'
		_, nblabels, _ = learn(dataset, epsvalue)
	
	print str(nblabels) + " clusters founds"
	
if __name__ == "__main__":
	main()