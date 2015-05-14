#!/usr/bin/python
import model as md
import dao as da

def exfe_composition_deck(deck,all_cards):
	result = {}
	
	for key in all_cards:
		result[key] = 0
		
	for v in deck.cardList:
		result[v.id] += 1 
	
	#return dictionary of all cards, key=cardID value=count
	return result
	
#TODO simplify this for loop and if (for all mec funcs)
def exfe_mec_general(deck,mechanic):
	val = 0
	for card in deck.cardList:
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
	for card in deck.cardList:
		if type in card.type:
			val += 1
			
	return val
	
def exfe_types(deck):
	result = []
	
	result.append(exfe_type(deck,md.Types.MINION))
	result.append(exfe_type(deck,md.Types.SPELL))
	result.append(exfe_type(deck,md.Types.WEAPON))
	
	return result
	
#TODO lambda ??
def exfe_distri(deck):
	 exfe_distri_general(deck,lambda card: true,lambda card: card.manacost,7)
	 exfe_distri_general(deck,lambda card: card.type == md.Types.SPELL,lambda card: card.attack,7)
	 exfe_distri_general(deck,lambda card: card.type != md.Types.MINION,lambda card: card.health,7)
	 
	 
def exfe_distri_general(deck,check,attribut,MAXMANA=7):
	result = []
	for i in range(MAXMANA):
		result.append(0)
		
	for card in deck.cardList:
		if(check(card)):
			pass
		cost = attribut(card)
		if cost>MAXMANA:
			cost = MAXMANA
		result[card] += 1
		
	return result
	
def exfe_distri_mana(deck,MAXMANA=7):
	result = []
	for i in range(MAXMANA):
		result.append(0)
		
	for card in deck.cardList:
	
		cost = card.manacost
		if cost>MAXMANA:
			cost = MAXMANA
		result[card] += 1
		
	return result
	
	
def exfe_distri_attack(deck,MAXATTACK=7):
	result = []
	for i in range(MAXATTACK):
		result.append(0)
		
		
	for card in deck.cardList:
		if card.type == md.Types.SPELL:
			pass
		cost = card.attack
		if cost>MAXATTACK:
			cost = MAXATTACK
		result[card] += 1
		
	return result
	
def exfe_distri_health(deck,MAXHEALTH=7):
	result = []
	for i in range(MAXHEALTH):
		result.append(0)
		
	for card in deck.cardList:
		if card.type != md.Types.MINION:
			pass
		cost = card.health
		if cost>MAXHEALTH:
			cost = MAXHEALTH
		result[card] += 1
		
	return result

def exfe_winrates(deck):
	result = []
	result.append(deck.constructedWinRate())
	#result.append(deck.arenaWinRate())
	return result

def exfe_decks(decks=[]):
	results = []
	
	for deck in decks:
		results.append(exfe_deck(deck))
		
	#return "matrix"
	return results
	
def exfe_deck(deck):
	result = []
	
	result.extend(exfe_composition_deck(deck,da.aquireCardList()))
	result.extend(exfe_mechanics(deck))
	result.extend(exfe_types(deck))
	result.extend(exfe_distri_mana(deck))#TODO use generalize ?
	result.extend(exfe_distri_attack(deck))#TODO use generalize ?
	result.extend(exfe_distri_health(deck))#TODO use generalize ?
	result.extend(exfe_winrates(deck))
	
	#return "list features"
	return result
	
#DEBUG
decks = da.aquireDeckList()
exfe_decks(decks)

	
