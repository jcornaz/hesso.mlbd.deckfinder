import oursql
import json
import string
import os.path
import pickle
from model import Deck
from model import Card
from model import Types
from model import Modes

FILENAME_DB_CREDENTIALS = 'db_credentials.json'
FILENAME_CARDS_LIST = 'cards_list.dat'
FILENAME_DECKS_LIST = 'decks_list.dat'

class Dao:
	def __init__(self):
		self.cards = None
		self.decks = None
		self.__con = None
	
	def __enter__(self):
		with open(FILENAME_DB_CREDENTIALS) as cred_file:    
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
			
	def parseCardstring(self,cardstring):
		if not self.cards:
			self.aquireCardList()
			
		res = {}
		for strv in string.split(cardstring,','):
			v = string.split(strv,'_')
			cardid = int(v[0])
			nbocc = int(v[1])
			if cardid in self.cards:
				res[self.cards[cardid]] = nbocc
		
		return res
				
	def aquireMechanics(self):
		print "aquiring mechanics from database..."
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
		if os.path.isfile(FILENAME_CARDS_LIST):
			print "loading cards from file..."
			with open(FILENAME_CARDS_LIST) as file:
				self.cards = pickle.load(file)
		else:
			mechanics = self.aquireMechanics()
			
			print "aquiring cards from database..."
			rows = self.execute("SELECT * FROM cards WHERE collectible = 1 AND type_name != 'Hero' AND mana IS NOT NULL")
			
			print "processing aquired cards..."
			self.cards = {}
			for row in rows:
				card = Card(id=row['id'],name=row['name'],type=Dao.strCardTypeToEnum(row['type_name']),isClassCard=not row['klass_id'] is None,rarity=row['rarity_id'],manacost=row['mana'],attack=row['attack'],health=row['health'])
				if card.id in mechanics:
					card.mechanics = mechanics[card.id]
				self.cards[card.id] = card
			
			print "dumping cards to file..."
			with open(FILENAME_CARDS_LIST,'w') as file:
				pickle.dump(self.cards, file)
		
		return self.cards
	
	def aquireResults(self,modes=[Modes.RANKED, Modes.CASUAL]):
		print "aquiring matches victories counts from database..."
		rows = self.execute( "SELECT d.cardstring, m.mode_id, count(m.id) FROM matches m, match_decks md, decks d WHERE m.id = md.match_id AND d.id = md.deck_id AND d.unique_deck_id IS NOT NULL AND m.mode_id in (" + ','.join(map(str,modes)) + ") AND m.result_id = 1 AND d.cardstring REGEXP '^([0-9]+_[1-9],)*([0-9]+_[1-9])$' GROUP BY d.cardstring, m.mode_id" )
		
		print "processing aquired results..."
		arenaWins = {}
		constructedWins = {}
		for row in rows:
			if row['mode_id'] == Modes.ARENA :
				arenaWins[row['cardstring']] = row['count(m.id)']
			else:
				constructedWins[row['cardstring']] = row['count(m.id)']
		
		return arenaWins, constructedWins
			
	def aquireDeckList(self,modes=[Modes.RANKED, Modes.CASUAL]):
		if not self.cards:
			self.aquireCardList()

		if os.path.isfile(FILENAME_DECKS_LIST):
			print "loading decks from file..."
			with open(FILENAME_DECKS_LIST) as file:
				self.decks = pickle.load(file)
		else:
			arenaWins, constructedsWins = self.aquireResults(modes)
			
			print "aquiring decks from database..."
			rows = self.execute("SELECT d.cardstring, d.klass_id, m.mode_id, count(m.id) FROM matches m, match_decks md, decks d WHERE m.id = md.match_id AND d.id = md.deck_id AND d.unique_deck_id IS NOT NULL AND m.mode_id in (" + ','.join(map(str,modes)) + ") AND d.cardstring REGEXP '^([0-9]+_[1-9],)*([0-9]+_[1-9])$' GROUP BY d.cardstring, m.mode_id")
			
			print "processing aquired decks..."
			self.decks = {}
			for row in rows:
				if row['cardstring'] in self.decks:
					deck = self.decks[row['cardstring']]
				else:
					deck = Deck(row['klass_id'])
					deck.addAllCards(self.parseCardstring(row['cardstring']))
					self.decks[row['cardstring']] = deck
					
				if row['mode_id'] == Modes.ARENA :
					deck.nbArenaMatches += row['count(m.id)']
					if row['cardstring'] in arenaWins:
						deck.nbArenaWins += arenaWins[row['cardstring']]
				else:
					deck.nbConstructedMatches += row['count(m.id)']
					if row['cardstring'] in constructedsWins:
						deck.nbConstructedWins += constructedsWins[row['cardstring']]
			
			print "dumping decks to file..."
			with open(FILENAME_DECKS_LIST,'w') as file:
				pickle.dump(self.decks, file)
				
		return [self.decks[k] for k in self.decks.keys()]