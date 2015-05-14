import oursql
import json
import model
from model import Deck
from model import Card

with open('db_credentials.json') as cred_file:    
    db_cred = json.load(cred_file)

def connect():
	return oursql.connect(host=db_cred['host'], user=db_cred['username'], passwd=db_cred['password'], db=db_cred['schema'], port=db_cred['port'])
									
def aquireCardList():
	con = connect()
	
	with con:
		cur = con.cursor(oursql.DictCursor)
		
		print "aquiring cards..."
		cur.execute("SELECT * FROM cards WHERE collectible = 1")
		cardsRows = cur.fetchall()
		
		print "aquiring mechanics..."
		cur.execute("SELECT * FROM card_mechanics WHERE card_id IN (SELECT id FROM cards WHERE collectible = 1)")
		mechRows = cur.fetchall()
		
		mechanics = {}
		
		print "processing aquired mechanics..."
		for row in mechRows:
			if row['card_id'] in row['card_id']:
				row['card_id'].append(row['mechanic_id'])
			else:
				row['card_id'] = [row['mechanic_id']]
				
		print "processing aquired cards..."
		for row in cardsRows:
			card = Card(row['id'],row['name'],row['mana'],row['attack'],row['health'])
			if card.id in mechanics:
				card.mechanics = mechanics[card.id]
			model.allcards[card.id] = card
			
def aquireDeckList():
	pass
