from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
import features
import numpy as np
import utils
import sys
import pickle

class Operation:
	LEARN = 0
	ANALYSE = 1

def clusters(db):
	labels = db.labels_
	core_samples_mask = np.zeros_like(labels, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	return set(labels), core_samples_mask
	
def learn(dataset,epsvalue,min_samples=10):
	return DBSCAN(eps=epsvalue,min_samples=min_samples,metric=cosine_distances,algorithm='ball_tree').fit(dataset)

def read_args(args=[]):
	operation = Operation.LEARN
	file_name = 'dbscan_result.dat'
	epsvalue = 0.5
	subset_size = sys.maxint
	
	if len(args) > 0:
		if args[0].lower() == 'analyse':
			operation = Operation.ANALYSE
		elif args[0].lower() == 'learn':
			operation = Operation.LEARN
		else:
			raise ValueError("unknown operation : " + args[0])
			
		if len(args) > 1:
			file_name = args[1]
			if len(args) > 2:
				epsvalue = float(args[2])
				if len(args) > 3:
					if args[3].lower() != "all":					
						subset_size = int(args[3])
	
	return operation, file_name, epsvalue, subset_size
	
def main(args=[]):
	"""
	Run the dbscan algorithm
	@param args [operation=(learn|analyse), file_name=../data/dbscan_result.dat, startEpsValue=0.5, randomSubsetSize=all]
	"""
	operation, file_name, epsvalue, subset_size = read_args(args)
	
	if operation == Operation.LEARN:
		dataset = features.load_dataset();
		if subset_size < sys.maxint:
			dataset = utils.random_subset(dataset,subset_size)
	
		print 'learning with eps=' + str(epsvalue) + '...'
		db = learn(dataset, epsvalue)
		labels, _ = clusters(db)
		while len(labels) <= 2:
			epsvalue /= 2.0
			print 'learning with eps=' + str(epsvalue) + '...'
			db = learn(dataset, epsvalue)
			labels, _ = clusters(db)
		
		print str(len(labels)) + " clusters founds"
		print "dumping result in " + file_name
		with open(file_name,'w') as file:
			pickle.dump(db, file, pickle.HIGHEST_PROTOCOL)
	else:
		print "loading result from " + file_name
		with open(file_name, 'r') as file:
			db = pickle.load(file)
		
		labels, mask = clusters(db)
		print "mask : " + str(mask)
		print "labels : " + str(labels)
		print str(len(labels)) + " cluster founds"
		
if __name__ == "__main__":
	main(sys.argv[1:])