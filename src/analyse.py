import features as f
import model as md
import numpy as np
import dao
import csv

def writeDeckListToCSV(filePath,deckList, deckClasses):
	with open(filePath+'.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, quotechar=';',quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['class','classeWoW','mana -3 -6 7+', 'health -3 -6 7+', 'attack -3 -6 7+', 'typeDistri-MSW']+["card #"+str(x) for x in range(1,31)])
		for deck,classe in zip(deckList,deckClasses):
			l = [c.name for c in deck.cardsList]
			typeDistri = " ".join("%.4f" % d for d in f.exfe_types(deck))
			rangeDistri = f.exfe_distri_range(deck)
			
			manaDistri = " ".join("%.4f" % d for d in rangeDistri[0:3])
			attackDistri = " ".join("%.4f" % d for d in rangeDistri[3:6])
			healthDistri = " ".join("%.4f" % d for d in rangeDistri[6:9])
			spamwriter.writerow([classe,md.Classes.NAMES[deck.klass],manaDistri,healthDistri, attackDistri,typeDistri]+l)
			
def writeDeckPrototypeToCSV(filePath, deckList, deckClasses):
	classSet = list(set(deckClasses))
	features = f.load_dataset(decks=deckList,withComp=True)
	nb_samples, nb_features = features.shape
	prototypes = np.zeros([nb_features,len(classSet)])
	winRates = {}
	matches = {}
	
	for i in range(len(classSet)):
		indexes = filter(lambda index: deckClasses[index] == classSet[i], range(nb_samples))
		for j in range(nb_features):
			prototypes[j,i] = np.mean(features[indexes,j])
			winRates[classSet[i]] = np.mean([deckList[k].constructedWinRate for k in indexes])
			matches[classSet[i]] = np.mean([deckList[k].nbConstructedMatches for k in indexes])
			
	with open(filePath + '.csv', 'wb' ) as csvfile:
		spamwriter = csv.writer(csvfile, quotechar=';',quoting=csv.QUOTE_MINIMAL)
		
		spamwriter.writerow(map(lambda c: winRates[c], classSet))
		spamwriter.writerow(map(lambda c: matches[c], classSet))
		
		for i in range(nb_features):
			spamwriter.writerow(prototypes[i,:])
		
	return prototypes, winRates, matches
	
if __name__ == '__main__':
	with dao.Dao() as da:
		decks = da.decks
		
	writeDeckListToCSV("classeTest",decks,range(len(decks)))