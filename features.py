#!/usr/bin/python
import model as md
import dao

reload(dao)
reload(md)

class Composition:
	def __init__(self, cards):
		self.keys = sorted(list(cards.keys()))
		self.nb = len(self.keys)
		
	def exfe(self, deck):
		res = [0] * self.nb
		cards = deck.cardsMap
		for card in cards.keys():
			try:
				res[self.keys.index(card.id)] = cards[card]
			except ValueError:
				print "ERROR: card " + str(card.id) + " not found in the list (" + ', '.join(map(str,self.keys)) + ")"
				
		return res
			
#TODO simplify this for loop and if (for all mec funcs)
def exfe_mec_general(deck,mechanic):
	val = 0
	for card in deck.cardsList:
		if mechanic in card.mechanics:
			val += 1
			
	return val
	
def exfe_mechanics(deck):
	result = []
	
	#TODO add more mechanics
	result.append(exfe_mec_general(deck,md.Mechanics.TAUNT))
	result.append(exfe_mec_general(deck,md.Mechanics.ONETURNEFFECT))
	result.append(exfe_mec_general(deck,md.Mechanics.MORPH))
	result.append(exfe_mec_general(deck,md.Mechanics.COMBO))
	result.append(exfe_mec_general(deck,md.Mechanics.SUMMON))
	result.append(exfe_mec_general(deck,md.Mechanics.SECRET))
	result.append(exfe_mec_general(deck,md.Mechanics.CHARGE))
	
	return result
	
def exfe_type(deck,type):
	val = 0
	for card in deck.cardsList:
		if type == card.type:
			val += 1
			
	return val
	
def exfe_types(deck):
	result = []
	
	result.append(exfe_type(deck,md.Types.MINION))
	result.append(exfe_type(deck,md.Types.SPELL))
	result.append(exfe_type(deck,md.Types.WEAPON))
	
	return result
	
	
def exfe_distri_general(deck,check,attribut,MAXMANA=7):
	result = []
	for i in range(MAXMANA+1):
		result.append(0)
		
	for card in deck.cardsList:
		if(check(card)):
			continue
		cost = attribut(card)
		if cost>MAXMANA:
			cost = MAXMANA
		result[cost] += 1
		
	return result

def exfe_distri(deck):
	result = []
	
	result.extend(exfe_distri_general(deck,lambda card: False,lambda card: card.manacost,7))
	result.extend(exfe_distri_general(deck,lambda card: card.type == md.Types.SPELL,lambda card: card.attack,7))
	result.extend(exfe_distri_general(deck,lambda card: card.type != md.Types.MINION,lambda card: card.health,7))
	
	return result
	 
def exfe_winrates(deck):
	result = []
	result.append(deck.constructedWinRate)
	#result.append(deck.arenaWinRate)
	return result

def exfe_decks(decks=[]):
	results = []
	
	for deck in decks:
		results.append(exfe_deck(deck))
		
	#return "matrix"
	return results
	
def exfe_deck(deck,comp):
	result = []
	
	result.extend(comp.exfe(deck))
	result.extend(exfe_mechanics(deck))
	result.extend(exfe_types(deck))
	result.extend(exfe_distri(deck))
	result.extend(exfe_winrates(deck))
	
	#return "list features"
	return result
	
#DEBUG
with dao.Dao() as da:
	cards = da.aquireCardList()
	decks = da.aquireDeckList()
	print exfe_deck(decks[42],Composition(cards))
