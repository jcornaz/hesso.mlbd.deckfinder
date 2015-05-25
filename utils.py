import random

def dictValues(dictionnary):
	return [dictionnary[k] for k in dictionnary.keys()]
	
def random_subset( iterator, n ):
	indexes = []
	res = []
	