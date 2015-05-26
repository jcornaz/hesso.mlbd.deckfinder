from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
import features
import numpy as np
import utils

def learn(dataset):
	db = DBSCAN(metric=cosine_distances).fit(dataset)
	labels = db.labels_
	core_samples_mask = np.zeros_like(labels, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	nblabels = len(set(labels)) - (1 if -1 in labels else 0)
	return labels, nblabels
	
def main():
	dataset = features.load_dataset()
	
	print "learning..."
	lerned, nblabels = learn(utils.random_subset(dataset,10000))
	
	print str(nblabels) + " clusters founds"
	
if __name__ == "__main__":
	main()