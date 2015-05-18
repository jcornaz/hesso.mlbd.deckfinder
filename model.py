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

class Classes:
	DRUID = 1
	HUNTER = 2
	MAGE = 3
	PALADIN = 4
	PRIEST = 5
	ROGUE = 6
	SHAMAN = 7
	WARLOCK = 8
	WARRIOR = 9

class Modes:
	ARENA = 1
	CASUAL = 2
	RANKED = 3
	FRIENDLY = 4
	PRACTICE = 5
	
class Deck:
	"""
	Representation of a deck. It can be constructed or not, complete or not and valid or not
	Use the method addCard to define the content of the deck
	"""
	
	def __init__(self,klass):
		"""
		Constructor
		@param klass Class of the deck
		"""
		
		self.__klass = klass
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
	
	def addCardsMap(self, cardsMap):
		"""
		Add a map of cards
		@param cardsMap [dict<card,int>] Map of cards to add. The keys must be the instance of the card and the key, the number of occurences
		"""
		
		for card in cardsMap.keys():
			self.addCard(card, cardsMap[card])
			
	@property
	def klass(self):
		return self.__klass
		
	@property
	def cardsMap(self):
		return self.__cards
	
	@property
	def cardsList(self):
		res = []
		for key in self.__cards.keys():
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
	
	def __init__(self, id, name, type, rarity, isClassCard, manacost, attack=0, health=0, mechanics=[]):
		"""
		Constructor
		@param id [int] Unique ID of the card
		@param name [string] Name of the card
		@param cardType [int] Type of the card
		@param rarity [int] Rarity of the card
		@param isClassCard [bool] If it's a card of class or not
		@param manacost [int] Mana cost of the card
		@param attack [int] Attack (0 if not a minion)
		@param heal [int] Heal points (0 if not a minion)
		@param mechanics [int] List of mechanics ids (can be empty)
		"""
		
		self.id = id
		self.name = name
		self.type = type
		self.rarity = rarity
		self.isClassCard = isClassCard
		self.manacost = manacost
		self.attack = attack
		self.health = health
		self.mechanics = mechanics
	
	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		return self.id == other.id
