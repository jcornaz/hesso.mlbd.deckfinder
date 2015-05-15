import oursql
import json
import string
from model import Deck
from model import Card
from model import Types

class Dao:
	def __init__(self):
		self.cards = None
		self.decks = None
		self.__con = None
	
	def __enter__(self):
		with open('db_credentials.json') as cred_file:    
		    db_cred = json.load(cred_file)
						
		self.__con = oursql.connect(host=db_cred['host'], user=db_cred['username'], passwd=db_cred['password'], db=db_cred['schema'], port=db_cred['port'])
		self.__cur = self.__con.cursor(oursql.DictCursor)
		
		return self
		
	def __exit__(self, type, value, traceback):
		if self.__con :
			self.__con.close()
			self.__con = None
	
	def execute(self, query):
		self.__cur.execute(query)
		return self.__cur.fetchall()
	
	@staticmethod
	def strCardTypeToEnum(strType):
		s = strType.lower()
		if s == 'minion':
			return Types.MINION
		elif s == 'spell':
			return Types.SPELL
		else:
			return Types.WEAPON
			
			
	def aquireMechanics(self):
		print "aquiring mechanics..."
		rows = self.execute("SELECT * FROM card_mechanics WHERE card_id IN (SELECT id FROM cards WHERE collectible = 1)")
				
		print "processing aquired mechanics..."
		mechanics = {}
		for row in rows:
			if row['card_id'] in row['card_id']:
				row['card_id'].append(row['mechanic_id'])
			else:
				row['card_id'] = [row['mechanic_id']]
				
		return mechanics
			
	def aquireCardList(self):
		mechanics = self.aquireMechanics()
		
		print "aquiring cards..."
		rows = self.execute("SELECT * FROM cards WHERE collectible = 1 AND type_name != 'Hero' AND mana IS NOT NULL")
		
		print "processing aquired cards..."
		self.cards = {}
		for row in rows:
			card = Card(id=row['id'],name=row['name'],type=Dao.strCardTypeToEnum(row['type_name']),isClassCard=not row['klass_id'] is None,rarity=row['rarity_id'],manacost=row['mana'],attack=row['attack'],health=row['health'])
			if card.id in mechanics:
				card.mechanics = mechanics[card.id]
			self.cards[card.id] = card
		
		return self.cards
				
	def aquireDeckList(self,modes):
		if not self.cards:
			self.aquireCardList()

		print "aquiring decks..."
		rows = self.execute("SELECT klass_id, cardstring, user_num_matches, user_num_wins FROM decks WHERE id IN (SELECT deck_id FROM constructeds) AND cardstring REGEXP '([0-9]+_[1-2],)*([0-9]+_[1-2])'")
		
		print "processing aquired decks..."
		self.decks = {}
		res = []
		for row in rows:
			if row['cardstring'] in self.decks.keys():
				deck = self.decks[row['cardstring']]
			else:
				deck = Deck(row['klass_id'],True)
				for strv in string.split(row['cardstring'],','):
					v = string.split(strv,'_')
					cardid = int(v[0])
					nbocc = int(v[1])
					if cardid in self.cards.keys():
						deck.addCard( self.cards[cardid], nbocc )
				self.decks[row['cardstring']] = deck
				res.append(deck)
			deck.nbConstructedMatches += row['user_num_matches']
			deck.nbConstructedWins += row['user_num_wins']
		
		return res