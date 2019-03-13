#!/usr/bin/python3
import cmd
import pprint
import getpass
import random
from time import time
from pymongo import MongoClient
from bson.objectid import ObjectId

class ContactApp(cmd.Cmd):
	intro = "\nContacts App\n"
	prompt = '> '
	client = MongoClient('localhost', 27017)
	db = None

	#works
	def do_create(self, line):
		"""For creating new database. Usage: create [name]"""
		dblist = self.client.list_database_names()
		if self.db is None:
			if line not in dblist:
				self.db = self.client[line]
				self.client.db.add_user(input("create username: "), getpass.getpass("Create password: "), roles=[{'role':'readWrite','db':line}])
				self.prompt = '({}) > '.format(line)
			else:
				print("This name is already taken.")
		else:
			print("Firstly close current database")

	#works
	def do_open(self, line):
		"""Opens existing database with specified name"""
		if self.db is None:
			if line in self.client.list_database_names():
				username = input("Enter username: ")
				password = getpass.getpass("Enter password: ")
				try:
					self.db = self.client[line]
					db = self.db
					self.client.db.authenticate(username, password)
					del db
					self.prompt = '({}) > '.format(line)
				except Exception:
				 	print("authentication failed")
				 	self.db = None
			else:
				print("Database doesn't exist")
		else:
			print("Firstly close current database")

	#works
	def do_close(self, line):
		"""Closes current database"""
		if not(self.db is None):
			self.db.logout()
			self.db = None
			self.prompt = '> '
		else:
			print("Invalid input\n")

	# Works
	def do_addContact(self, line):
		"""Adds new contact to your current database"""
		if not(self.db is None):
			cont = self.db.contact
			contact_info = {
				'first_name': input("First name: "),
				'surname': input("Surname: "),
				'company': input("Company: "),
				'address': input("Address: "),
				'telephone': input("Telephone: "),
				'email': input("Email: ")
			}
			cont.insert_one(contact_info)
		else:
			print("You must open the existing database or create new one.")

	def do_add_100000(self, line):
		if not(self.db is None):
			cont = self.db.contact
			with open('users.txt', 'rt') as file:
				names = file.read()
				names = names.split()
				print("Adding 10000 contacts...\n")
				contacts = [{'first_name': random.choice(names),
							 'surname': random.choice(names),
							 'company': random.choice(names),
							 'address': random.choice(names),
							 'telephone': random.choice(names),
							 'email': random.choice(names)
							} for i in range(100000)]
				cont.insert_many(contacts)



	#works
	def do_delContact(self, line):
		"""Deletes contact with specified _id"""
		if not(self.db is None):
			try:
				self.db.contact.delete_one({'_id': ObjectId(line)})
			except Exception:
				print("This id doesn't exist!")
		else:
			print("You must open the existing database or create new one.")

	#works
	def do_show(self, line):
		"""Shows all available contacts in the current database."""
		if not(self.db is None):
			for contact in self.db.contact.find():
				pprint.pprint(contact)
		else:
			print("You must open the existing database or create new one.")

	#works
	def do_list(self, line):
		"""Shows all available databases"""
		x = [i for i in self.client.list_databases() if i['name'] not in ['admin','config','line','local','mongoengine_test','pymongo_test']]
		for db in x:
			print(db['name'])

	def do_search(self, line):
		"""Searches contacts by any field using regular expressions (Case sensitive)."""
		if not(self.db is None):
			start = time()
			result = self.db.contact.find({'$or':[
					{'first_name': {'$regex':line, '$options':'i'}},
					{'surname': {'$regex':line, '$options':'i'}},
					{'company': {'$regex':line, '$options':'i'}},
					{'address': {'$regex':line, '$options':'i'}},
					{'telephone': {'$regex':line, '$options':'i'}},
					{'email': {'$regex':line, '$options':'i'}},
					{'id_': {'$regex':line, '$options':'i'}}
				]})
			for i in result:
				pprint.pprint(i)
			print("Time elapsed: {}".format(time()-start))
		else:
			print("You must open the existing database or create new one.")

	#works
	def do_update(self, line):
		"""Updates contact with specified _id"""
		if not(self.db is None):
			try:
				field = input("Field to update: ")
				value = input("Value: ")
				query = {'_id': ObjectId(line)}
				new_vals = {"$set": {field: value}}
				self.db.contact.update_one(query, new_vals)
			except Exception:
				print("Wrong _id! Try again.")

	#works
	def do_len(self, line):
		"""Returns number of users in current book"""
		if not(self.db is None):
			print(self.db.contact.count_documents({}))
		else:
			print("You must open the existing database or create new one.")




	def do_EOF(self, line):
		"""Don't touch this!"""
		return True

	def do_quit(self, line):
		"""Quits the program"""
		if not(self.db is None):
			self.db.logout()
			self.db = None
		return self.do_EOF(line)

	def do_postloop(self):
		"""Does nothing"""
		print('Quit...')


if __name__ == '__main__':
	ContactApp().cmdloop()
