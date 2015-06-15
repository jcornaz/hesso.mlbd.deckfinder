import random as rnd
import numpy as np
from time import gmtime, strftime

def dictValues(dictionnary):
	return [dictionnary[k] for k in dictionnary.keys()]

def random_sublist( lst, n ):
	# Reservoir sampling algorithm

	res = []
	nbelt = len(lst)
	
	for i in range(n):
		res.append(lst[i])
	
	for i in range(n,nbelt):
		j = rnd.randint(0,i)
		if j < n:
			res[j] = lst[i]
	
	return res
	
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
			
			
def printTime(prefix):
	print (strftime("%H:%M:%S %d-%m-%Y", gmtime())+" "+prefix)
