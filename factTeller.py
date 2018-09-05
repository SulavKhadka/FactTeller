import sqlite3
import random


class FactTeller():

	def __init__(self):
		self.db = sqlite3.connect('./Databases/Factsdb')
		self.cursor = self.db.cursor()

		self.factlist = []

	def get_unread_facts(self):
		self.cursor.execute('''SELECT id, fact FROM facts WHERE used=0''')
		all_unread_facts = self.cursor.fetchall()

		if not all_unread_facts:
			self.reset_read_ids()
			self.cursor.execute('''SELECT id, fact FROM facts WHERE used=0''')
			all_unread_facts = self.cursor.fetchall()

		self.factlist = [(i[0], i[1]) for i in all_unread_facts]

	def update_read_fact(self, uid):
		self.cursor.execute('''UPDATE facts SET used = ? WHERE id = ?''', (1, uid))
		self.db.commit()

	def reset_read_ids(self):
		self.cursor.execute('''UPDATE facts SET used=0''')
		self.db.commit()

	def get_fact(self, number_of_facts):

		final_fact_list = []

		for _ in range(number_of_facts):
			self.get_unread_facts()
			random_fact_tuple = random.choice(self.factlist)
			self.update_read_fact(random_fact_tuple[0])
			final_fact_list.append(random_fact_tuple[1])

		self.db.close()
		return final_fact_list


if __name__ == '__main__':
	f = FactTeller()
	random_fact = f.get_fact(1)
	[print(i) for i in random_fact]