allcards = {}	# Dictionary of all the existing cards. The key is the id, and the value is the instance of the Card class

class Types:
  MINION = 1
  SPELL  = 2
  WEAPON = 3
    
class Mechanics:
	TAUNT = 1
	ONETURNEFFECT = 2
	MORPH = 3
	COMBO = 4
	SUMMON = 5
	SECRET = 6
	CHARGE = 7
	DEATHRATTLE = 8 
	FREEZE = 9
	AURA = 10
	POISONOUS = 11
	IMMUNETOSPELLPOWER = 12
	SPELLPOWER = 13
	BATTLECRY = 14
	ADJACENTBUFF = 15
	HEALTARGET = 16
	DIVINESHIELD = 17
	WINDFURY = 18 
	ENRAGE = 19
	AFFECTEDBYSPELLPOWER = 20
	STEALTH = 21
	SILENCE = 22
	#TODO complete it when the DATABASE is updated
	#ATTACKPLUS = 1
	#DEALDAMAGE = 4
	#DRAW = 6
	#RANDOM = 7
	#RETURN = 8

class Deck:
	"""
	Representation of a deck. It can be constructed or not, complete or not and valid or not
	Use the method addCard to define the content of the deck
	"""
	
	def __init__(self):
		"""
		Constructor
		"""
		
		self.__cards = {}
		self.__nbCards = 0
		self.__nboccMax = 0
		self.nbConstructedMatches = 0
		self.nbConstructedWins = 0
		self.nbArenaMatches = 0
		self.nbArenaWins = 0
		
	def addCard(self, card, nbocc=1):
		"""
		Add a card in the decks
		@param card [Card] Instance of the card to add
		@param nbocc [int] Number of occurences of the card to add
		"""
		
		self.__nbCards += nbocc
		
		if card in self.__cards:
			self.__cards[card] += nbocc
		else:
			self.__cards[card] = nbocc
			
		if self.__cards[card] > self.__nboccMax :
			self.__nboccMax = self.__cards[card]
			
	@property
	def cardsMap(self):
		return self.__cards
	
	@property
	def cardList(self):
		res = []
		for key in self.__cards:
			for i in range( self.__cards[key] ):
				res.append(key)
		return res

	@property
	def nbCards(self):
		return self.__nbCards
		
	@property
	def isComplete(self):
		return self.nbCards == 30
	
	@property
	def isValidConstructed(self):
		return self.isComplete and self.__nboccMax <= 2
	
	@property
	def isValidArena(self):
		return self.isComplete
		
	@property
	def constructedWinRate(self):
		if self.nbConstructedMatches > 0:
			return self.nbConstructedWins / self.nbConstructedMatches
		else:
			return float('nan')
	
	@property
	def arenaWinRate(self):
		if self.nbArenaMatches > 0:
			return self.nbArenaWins / self.nbArenaMatches
		else:
			return float('nan')
	
	def __hash__(self):
		return hash(self.cards)

	def __eq__(self, other):
		return len(set(self.cards.items()) ^ set(other.cards.items())) == 0
		
class Card:
	"""
	Representation of a card
	"""
	
	def __init__(self, id, name, type, manacost, attack=0, health=0, mechanics=[]):
		"""
		Constructor
		@param id [int] Unique ID of the card
		@param type [int] Type of the card
		@param manacost [int] Mana cost of the card
		@param attack [int] Attack (0 if not a minion)
		@param heal [int] Heal points (0 if not a minion)
		@param mechanics [int] List of mechanics ids (can be empty)
		"""
		
		self.id = id
		self.type = type
		self.manacost = manacost
		self.attack = attack
		self.health = health
		self.mechanics = mechanics
		self.name = name
	
	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		return self.id == other.id
