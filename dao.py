import oursql
import json
import model
import random
from model import Deck
from model import Card
from model import Types

db_cred = None

def connect():
	global db_cred
	if db_cred is None :
		with open('db_credentials.json') as cred_file:    
		    db_cred = json.load(cred_file)
						
	return oursql.connect(host=db_cred['host'], user=db_cred['username'], passwd=db_cred['password'], db=db_cred['schema'], port=db_cred['port'])

def strCardTypeToEnum(strType):
	s = strType.lower()
	if s == 'Minion':
		return Types.MINION
	elif s == 'Spell':
		return Types.SPELL
	else:
		return Types.WEAPON
	
def aquireCardList():
	con = connect()
	
	with con:
		cur = con.cursor(oursql.DictCursor)
		
		print "aquiring cards..."
		cur.execute("SELECT * FROM cards WHERE collectible = 1 AND type_name != 'Hero'")
		cardsRows = cur.fetchall()
		
		print "aquiring mechanics..."
		cur.execute("SELECT * FROM card_mechanics WHERE card_id IN (SELECT id FROM cards WHERE collectible = 1)")
		mechRows = cur.fetchall()
				
		print "processing aquired mechanics..."
		mechanics = {}
		for row in mechRows:
			if row['card_id'] in row['card_id']:
				row['card_id'].append(row['mechanic_id'])
			else:
				row['card_id'] = [row['mechanic_id']]
				
		print "processing aquired cards..."
		model.allcards = {}
		for row in cardsRows:
			card = Card(row['id'],row['name'],strCardTypeToEnum(row['type_name']),row['rarity_id'],row['mana'],row['attack'],row['health'])
			if card.id in mechanics:
				card.mechanics = mechanics[card.id]
			model.allcards[card.id] = card
		
		return model.allcards
			
def aquireDeckList():
	res = []
	cards = aquireCardList()
	for i in range(100):
		deck = Deck()
		for j in range(30):
			deck.addCard(cards[random.choice(cards.keys())])
		res.append(deck)
	return res