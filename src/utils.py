import random as rnd
import numpy as np

def dictValues(dictionnary):
	return [dictionnary[k] for k in dictionnary.keys()]
	
def random_subset( matrix, n ):
	# Reservoir sampling algorithm

	nbrow,nbcol = matrix.shape
	res = np.empty([n,nbcol])
	
	for i in range(n):
		res[i,:] = matrix[i,:]
	
	for i in range(n,nbrow):
		j = rnd.randint(0,i)
		if j < n:
			res[j,:] = matrix[i,:]
	
	return res
			