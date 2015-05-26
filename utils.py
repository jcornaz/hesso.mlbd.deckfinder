import random as rnd
import numpy as np

def dictValues(dictionnary):
	return [dictionnary[k] for k in dictionnary.keys()]
	
def random_subset( matrix, n ):
	indexes = []
	l,c = matrix.shape
	res = np.zeros([n,c])
	j = rnd.randint(0,l)
	for i in range(n):
		while j in indexes:
			j = rnd.randint(0,l)
		res[i,:] = matrix[j,:]
	return res