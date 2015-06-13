from minisom import MiniSom
import features    
import sys

def main(args=[]):
	som = MiniSom(5,5,4,sigma=0.3,learning_rate=0.5) # initialization of 6x6 SOM
	print "Training..."
	som.train_random(features.load_dataset(),100) # trains the SOM with 100 iterations
	print "...ready!"

if __name__ == '__main__':
	main(sys.argv[1:])