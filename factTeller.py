import sqlite3
import random

def get_unread_facts(db, cursor):
	cursor.execute('''SELECT id, fact FROM facts WHERE used=0''')
	allfacts = cursor.fetchall()

	if allfacts == []:
		reset_read_ids(db, cursor)
		cursor.execute('''SELECT id, fact FROM facts WHERE used=0''')
		allfacts = cursor.fetchall()

	keys = []
	facts = []

	for i in allfacts:
		keys.append(i[0])
		facts.append(i[1])

	factlist = [keys, facts]

	return factlist


def update_read_fact(uid, db, cursor):
	cursor.execute('''UPDATE facts SET used = ? WHERE id = ?''', (1, uid))
	db.commit()

def reset_read_ids(db, cursor):
	cursor.execute('''UPDATE facts SET used=0''')
	db.commit()

def get_fact():
	db = sqlite3.connect('./Factsdb')
	cursor = db.cursor()

	factlist = get_unread_facts(db, cursor)
	random_id = random.choice(factlist[0])
	id_position = factlist[0].index(random_id)
	fact = factlist[1][id_position]
	update_read_fact(random_id, db, cursor)

	db.close()

	return fact


if __name__ == '__main__':
	fact = get_fact()
	print fact