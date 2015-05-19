#!/usr/bin/python
import model
import dao
from model import Mechanics

import mdp
import bimdp

with dao.Dao() as da:
	cards = da.cards
	decks = da.decks
	

