#!/usr/bin/python3
import random
import re
import os
import pickle
import getpass
import random
from time import time
from hashlib import sha256
from collections import UserList, OrderedDict


class Book(UserList):
    
    def __init__(self):
        self.password = ''
        super().__init__()

    def add_contact(self):
        print("Adding new contact...\nEnter credentials:")
        creds = ['first_name', 'surname', 'company', 'address', 'telephone', 'email']
        cred_dict = OrderedDict()
        for i in creds:
            cred_dict[i] = input(i+': ')
        self.data.append(ContactCard(**cred_dict))
        return "Successfully added contact"

    def add_10000contacts(self, users):
        with open(users, 'rt') as f:
            file_obj = f.read()
            file_obj = file_obj.split()
        print("Adding 10000 contacts...\n")
        creds = ['first_name', 'surname', 'company', 'address', 'telephone', 'email']
        for i in range(10000):
            cred_dict = OrderedDict()
            for i in creds:
                cred_dict[i] = random.choice(file_obj)
            self.data.append(ContactCard(**cred_dict))
        return "Successfully added 10000 contacts"

    def del_contact(self, uid):
        for i in self.data:
            if i.uid == int(uid):
                print("Deleting Contact with id: {}".format(i.uid))
                self.data.remove(i)
        return

    def search_contact(self, m_d, reg_str):
        res = []
        for i in m_d:
            if any(re.search(reg_str, str(x)) for x in i.d):
                res.append(i)
        for i in res:
            print(i)

    def fsearch_contact(self, reg_str):
        res = []
        for i in self.data:
            if any(re.search(reg_str, str(x)) for x in i.d):
                res.append(i)
        return res

    def multi_search_contact(self, obj):
        if any(re.search(self.pool_str, str(x)) for x in obj.d):
            res = obj
            print(res)
        else:
        	pass

    def list_contacts(self):
        for i in self.data:
            print(i)

        return

    def update_contact(self, uid, field, value):
        for i in self.data:
            if i.uid == int(uid):
                i.__dict__[field] = value
        return self.data

    def save_book(self, file):
        if not os.path.exists(file):
            self.password = sha256(getpass.getpass("Create a password: ").encode('utf_8')).hexdigest()
        with open(file, 'wb') as f:
            pickle.dump(self, f)

    def open_book(self, file):
        with open(file, 'rb') as f:
            obj = pickle.load(f)
            passw = sha256(getpass.getpass("Enter a password: ").encode('utf_8')).hexdigest()
            if passw == obj.password:
                print("\nYou have opened {} book.\n".format(file))
                return obj
            else:
                print("Wrong password! Try again")    


class ContactCard:

    rand_list = list(set(random.randint(0,100000) for i in range(100000)))

    def __init__(self, first_name, surname=None, company=None, address=None, telephone=None, email=None):
        self.first_name = first_name
        self.surname = surname
        self.company = company
        self.address = address
        self.telephone = telephone
        self.email = email
        self.uid = hash(first_name) + self.rand_gen()

    @property
    def d(self):
        return [self.uid, self.first_name, self.surname, self.company, self.address, self.telephone, self.email]

    def rand_gen(self):
        r = random.choice(ContactCard.rand_list)
        ContactCard.rand_list.remove(r)
        return r

    def __str__(self):
        return "\nContact {0}:\nFirstname: {1}\nSurname: {2}\nCompany: {3}\nAddress: {4}\nTelephone: {5}\nEmail: {6}\n".format(
            self.uid, self.first_name, self.surname, self.company, self.address, self.telephone, self.email
        )

    # def __repr__(self):
    #     return "\nContact {0}:\nFirstname: {1}\nSurname: {2}\nCompany: {3}\nAddress: {4}\nTelephone: {5}\nEmail: {6}\n".format(
    #         self.uid, self.first_name, self.surname, self.company, self.address, self.telephone, self.email
    #     )
