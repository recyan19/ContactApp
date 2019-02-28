#!/usr/bin/python3
import cmd
import os
from time import time
from multiprocessing import Queue, Process, Pool
from contacts import Book, ContactCard


class ContactApp(cmd.Cmd):
	intro = "\nContacts App\n"
	prompt = "> "
	cl = None
	def do_save(self, line):
		"""Saves new book in specified location"""
		if isinstance(self.cl, Book):
			self.cl.save_book(line)
			del self.cl
			print("\nYou saved your contacts in {} book.".format(line))
			print("To use this app you should create new book or open existing.\n")
			self.prompt = "> "
		else:
			print("To save book you must open or create it!")

	def do_open(self, line):
		"""Opens saved book from specified location"""
		try:
			self.cl = Book().open_book(line)
			if isinstance(self.cl, Book):
				self.prompt = '({})> '.format(line)
			self.can_be_closed = True
			self.bookfile = line
		except FileNotFoundError:
			print("There is no such file!")

	def do_close(self, line):
		"""Closes current book"""
		if isinstance(self.cl, Book) and self.can_be_closed:
			self.cl.save_book(self.bookfile)
			del self.cl
			self.prompt = "> "

	def do_createbook(self, line):
		"""Creates new contacts book. After adding new contacts to it, don't forget to save it"""
		self.cl = Book()
		print("New Contact Book initialized")

	def do_adduser(self, line):
		"""Adds contact to your current book"""
		if isinstance(self.cl, Book):
			self.cl.add_contact()
		else:
			print("To add contacts you need to open or create a book.")

	def do_deluser(self, line):
		"""Deletes contact from your current book (by id)."""
		if isinstance(self.cl, Book):
			try:
				self.cl.del_contact(line)
			except ValueError:
				print("Wrong syntax! Type 'help delete'")
		else:
			print("To delete contacts you need to open or create a book.")

	def do_fsearch(self, line):
		if isinstance(self.cl, Book):
			st = time()
			print("\nSearch results for: ",str(line))
			for i in self.cl.fsearch_contact(str(line)):
				print(i)

			print('Time elapsed: {:10f}'.format(time()-st))
		else:
			print("To search contacts you need to open or create a book.")

	def do_search(self, line):
		"""Searches contacts by any field using regular expressions (Case sensitive)."""
		# if isinstance(self.cl, Book):
		# 	st = time()
		# 	print("\nSearch results for: ",str(line))
		# 	for i in self.cl.search_contact(str(line)):
		# 		print(i)
		# 	print('Time elapsed: {:10f}'.format(time()-st))
		# else:
		# 	print("To search contacts you need to open or create a book.")
		if isinstance(self.cl, Book):
			st = time()
			print("\nSearch results for: ",str(line))
			w = []
			for i in range(0,len(self.cl.data),10000):
				w.append(self.cl.data[i:i+10000])
			workers = []
			for i in w:
				workers.append(Process(target=self.cl.search_contact, args=(i, str(line))))
			for worker in workers:
				worker.start()
			for worker in workers:
				worker.join()
			print('Time elapsed: {:10f}'.format(time()-st))
		else:
			print("To search contacts you need to open or create a book.")

	def do_multi_search(self, line):
		"""Searches contacts by any field using regular expressions (Case sensitive)."""
		if isinstance(self.cl, Book):
			print("\nSearch results for: ",str(line))
			t = time()
			self.cl.pool_str = str(line)
			pool = Pool(4)
			pool.imap_unordered(self.cl.multi_search_contact, self.cl.data, chunksize=50000)
			pool.close()
			pool.join()
			print("time elapsed: {:10f}".format(time()- t))
		else:
			print("To search contacts you need to open or create a book.")


	def do_show(self, line):
		"""Shows all available contacts in the current book."""
		if isinstance(self.cl, Book):
			print("Contacts in the current book\n")
			self.cl.list_contacts()
		else:
			print("To see contacts you need to open or create book")

	def do_update(self, line):
		"""Updates any field of specified contact (by id, field_name, value)\nList of available fields - [first_name,surname,company,address,telephone,email]"""
		if isinstance(self.cl, Book):
			try:
				self.cl.update_contact(*line.split())
				print("Updated Contact with id: {}. {}={}".format(*line.split()))
			except TypeError:
				print("Wrong syntax! Type 'help update'")
		else:
			print("To update contacts you need to open or create book")

	def do_list_availble_books(self, line):
		"""Shows all available books in current directory"""
		print('\nBooks in your current directory: \n')
		for i in os.listdir():
			if i.endswith('.bin'):
				print(i)
		print('\n')

	def do_add10000users(self, line):
		if isinstance(self.cl, Book):
			try:
				self.cl.add_10000contacts(str(line))
			except FileNotFoundError:
				print("There is no such file!")

	def do_len(self, line):
		print(len(self.cl.data))

	def do_EOF(self, line):
		return True

	def do_quit(self, line):
		return self.do_EOF(line)

	def do_postloop(self):
		print('Quit...')

if __name__ == '__main__':
	ContactApp().cmdloop()