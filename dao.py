import oursql
import json
import model
from model import Deck
from model import Card

with open('db_credentials.json') as cred_file:    
    db_cred = json.load(cred_file)

def aquire(query):
	con = oursql.connect(host=db_cred['host'], user=db_cred['username'], passwd=db_cred['password'], db=db_cred['schema'], port=db_cred['port'])
	with con:
		cur = con.cursor(oursql.DictCursor)
		cur.execute(query)
		return cur.fetchall()
									
def aquireCardList():
	rows = aquire("SELECT * FROM cards WHERE collectible = 1")
	for row in rows:
		print str(row['id']) + " " + row['name'] + " " + str(row['attack'])

def aquireDeckList():
	pass
