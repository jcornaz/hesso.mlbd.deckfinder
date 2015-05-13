allcards = {}	# Dictionary of all the existing cards. The key is the id, and the value is the instance of the Card class

class Deck:
	"""
	Representation of a deck. It can be constructed or not, complete or not and valid or not
	Use the method addCard to define the content of the deck
	"""
	
	def __init__(self, isConstructed=True):
		"""
		Constructor
		@param isConstructed [bool] If the deck is an constructed one or not
		"""
		self.isConstructed = isConstructed
		self.__cards = {}
		self.__nbCards = 0
		self.__nboccMax = 0
		
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
	def isValid(self):
		return self.isComplete and (not self.isConstructed or self.__nboccMax <= 2)
	
	def __hash__(self):
		return hash(self.cards)

	def __eq__(self, other):
		return len(set(self.cards.items()) ^ set(other.cards.items())) == 0
		
class Card:
	"""
	Representation of a card
	"""
	
	def __init__(self, id, type, manacost, attack=0, heal=0, mechanics=[]):
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
		self.heal = heal
		self.mechanics = mechanics
	
	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		return self.id == other.id