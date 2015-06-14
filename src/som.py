from minisom import MiniSom
import features    
import sys
import pickle

def learn(dataset,sigma=0.3,learning_rate=0.5,nb_iter=10000):
	som = MiniSom(5,5,4,sigma=sigma,learning_rate=learning_rate)
	som.train_random(dataset,nb_iter)
	return som
	
def main(args=[]):
	file_name = 'som_result.dat'
	
	dataset = features.load_dataset(withComp=True)
	som = learn(dataset)
	print "dumping result in " + file_name
	with open(file_name,'w') as file:
		pickle.dump(som, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	main(sys.argv[1:])