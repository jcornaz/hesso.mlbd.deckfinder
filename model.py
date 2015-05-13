class Deck:
	def __init__(self, isConstructed):
		self.__cards = {}
		self.__nbCards = 0
		self.isConstructed = isConstructed
	
	def addCard(self, card):
		nbCards += 1
		if card in self.__cards:
			self.__cards[card] += 1
		else:
			self.__cards[card] = 1

	@property
	def cardsMap(self):
		return self.__cards
	
	@property
	def cardList(self):
		res = self.__cards.keys()
		for key in self.__cards:
			if self.__cards[key] > 1:
				for i = range( 1, self.__cards[key] ):
					res.append(key)
		return res

	@property
	def nbCards(self):
		return self.__nbCards
		
	@property
	def isComplete(self):
		return self.nbCards == 30
	
	def __hash__(self):
		return hash(self.cards)

	def __eq__(self, other):
		return len(set(self.cards.items()) ^ set(other.cards.items())) == 0
		
class Card
	def __init__(self, id, type, manacost, attack, heal, mechanics):
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