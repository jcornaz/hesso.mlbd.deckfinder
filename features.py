#!/usr/bin/python
import model as md

toto = md.Card(1,2,3)

print()

def exfe_composition_deck(deck,all_cards):
	result = {}
	
	for key in all_cards:
		result[key] = 0
	
	for v in deck.cardList():
		result[v.id] += 1 
	
	#return dictionary of all cards, key=cardID value=count
	return result
	
#TODO simplify this for loop and if (for all mec funcs)
def exfe_mec_general(deck,mechanic):
	val = 0
	for card in deck.cardList():
		if mechanic in card.mechanics:
			val += 1
			
	return val
	
def exfe_mec(deck):
	result = []
	
	result.append(exfe_mec_general(deck,M_ATTACKPLUS))
	result.append(exfe_mec_general(deck,BATTLECRY))
	result.append(exfe_mec_general(deck,CHARGE))
	result.append(exfe_mec_general(deck,DEALDAMAGE))
	result.append(exfe_mec_general(deck,DEATHRATTLE))
	result.append(exfe_mec_general(deck,DRAW))
	result.append(exfe_mec_general(deck,RANDOM))
	result.append(exfe_mec_general(deck,RETURN))
	result.append(exfe_mec_general(deck,SECRET))
	result.append(exfe_mec_general(deck,SILENCE))
	result.append(exfe_mec_general(deck,SUMMON))
	
	return result
	
def exfe_type(deck,type):
	val = 0
	for card in deck.cardList():
		if type in card.type:
			val += 1
			
	return val
	
def exfe_types(deck):
	result = []
	
	result.append(exfe_type(deck,MINION))
	result.append(exfe_type(deck,SPELL))
	result.append(exfe_type(deck,WEAPON))
	
	return result
	
def exfe_distri_mana(deck):
	pass
	
def exfe_distri_attack(deck):
	pass
	
def exfe_distri_health(deck):
	pass

def exfe_winrates(deck):
	pass

def exfe_decks(decks=[]):
	return "matrix"
	
def exfe_deck(deck):
	return "list features"
	
