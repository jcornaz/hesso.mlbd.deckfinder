from minisom import MiniSom
import features    
import sys
import pickle
import pylab as py

def learn(dataset,sigma=0.3,learning_rate=0.5,nb_iter=10000):
	nb_sample, nb_features = dataset.shape
	som = MiniSom(6,6,nb_features,sigma=sigma,learning_rate=learning_rate)
	som.train_random(dataset,nb_iter)
	return som

def plotsom(som, features, tostrfct=lambda i: str(i)):
	py.bone()
	py.pcolor(som.distance_map().T)
	py.colorbar()
	
	nb_samples,_ = features.shape
	
	lastPos = {}
	for i in range(nb_samples):
		w = som.winner(features[i,:])
		if w in lastPos:
			pos = lastPos[w]
			pos[0] += 0.2
			if pos[0] >= 1.0:
				pos[0] = 0
				pos[1] += 0.2
		else:
			pos = [0.0, 0.0];
		
		lastPos[w] = pos
		
		if( pos[1] < 1.0):
			py.text(w[0]+pos[0], w[1]+(0.8-pos[1]),tostrfct(i))
	
def main(args=[]):
	file_name = 'som_result.dat'
	
	dataset = features.load_dataset(withComp=True)
	som = learn(dataset)
	print "dumping result in " + file_name
	with open(file_name,'w') as file:
		pickle.dump(som, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	main(sys.argv[1:])