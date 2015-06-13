from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
import features
import numpy as np
import utils
import sys
import pickle

def learn(dataset,epsvalue):
	db = DBSCAN(eps=epsvalue,min_samples=10,metric=cosine_distances,algorithm='ball_tree').fit(dataset)
	labels = db.labels_
	core_samples_mask = np.zeros_like(labels, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	return set(labels), core_samples_mask

def read_args(args=[]):
	epsvalue = 1
	subset_size = sys.maxint
	file_name = 'dbscan_result.dat'
	
	try:
		if len(args) > 0:
			epsvalue = int(args[0])
			if len(args) > 1:
				if args[1] != "all":					
					subset_size = int(args[1])
				if len(args) > 2:
					file_name = args[2]
	except Exception:
		pass
	
	return epsvalue, subset_size, file_name
	
def main(args=[]):
	"""
	Run the dbscan algorithm
	@param args [startEpsValue=1, randomSubsetSize=all, fileName=dbscan_result.dat]
	"""
	epsvalue, subset_size, file_name = read_args(args)
	
	dataset = features.load_dataset();
	if subset_size < sys.maxint:
		dataset = utils.random_subset(dataset,subset_size)

	print 'learning with eps=' + str(epsvalue) + '...'
	labels, mask = learn(dataset, epsvalue)
	while len(labels) <= 1:
		epsvalue /= 2.0
		print 'learning with eps=' + str(epsvalue) + '...'
		labels, mask = learn(dataset, epsvalue)
	
	print str(len(labels)) + " clusters founds"
	print "dumping result in " + file_name
	with open(file_name,'w') as file:
		pickle.dump([labels, mask], file, pickle.HIGHEST_PROTOCOL)
	
if __name__ == "__main__":
	main(sys.argv[1:])