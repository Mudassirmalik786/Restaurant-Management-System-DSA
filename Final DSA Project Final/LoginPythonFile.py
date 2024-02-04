# Purpose: This file is used to create a hash table for the login information of the user.
import csv

# This class is used to contain the login information of the user.
class Customer:
    def __init__(self, userName, password,Bill):
        self.userName = userName
        self.password = password
        self.Bill = Bill
        self.next = None
# This class is used to create a hash table for the login information of the user.
class HashTable:
    def __init__(self):
        self.size = 10
        self.HashTable = {}
        for i in range(self.size):
            self.HashTable[i] = None
    # This function is used to hash the password of the user.
    def hash(self, key):
        return key % self.size
    # This function is used to insert the login information of the user into the hash table.
    def insert(self, userName, password,Bill=0):
        hash_table_index = self.hash(password)
        new_Customer = Customer(userName, password,Bill)
        if self.HashTable[hash_table_index] is None:
            self.HashTable[hash_table_index] = new_Customer
        else:
            head = self.HashTable[hash_table_index]
            current = head
            while current.next is not None:
                current = current.next
            current.next = new_Customer
    # This function is used to check if the login information of the user is present in the hash table.
    def isPresent(self, userName, password):
        hash_table_index = self.hash(password)
        head = self.HashTable[hash_table_index]
        current = head
        while current != None:
            if current.userName == userName:
                return True
            current = current.next
        return False
    # This function is used to search the login information of the user in the hash table.
    def search(self, userName, password):
        hash_table_index = self.hash(password)
        head = self.HashTable[hash_table_index]
        current = head
        while current != None:
            if current.password == password and current.userName == userName:
                return current
            current = current.next
        return None
    # This function is used to access all the login information of the user in the hash table.
    def access_all_elements(self):
        all_elements = []
        for i in range(self.size):
            current = self.HashTable[i]
            while current:
                all_elements.append(current)
                current = current.next
        return all_elements
    # This function is used to get the length of the hash table.
    def getlength(self):
        count = 0
        for i in range(self.size):
            current = self.HashTable[i]
            while current:
                count += 1
                current = current.next
        return count
    # This function is used to delete the login information of the user from the hash table.
    def delete_from_hash_table(self, userName, password):
        hash_table_index = self.hash(password)
        head = self.HashTable[hash_table_index]
        if head is None:
            return None
        if head.userName == userName and head.password == password:
            self.HashTable[hash_table_index] = head.next
            return
        prev = None
        current = head
        while current is not None and (current.userName != userName and current.password != password):
            prev = current
            current = current.next
        if current is None:
            return None
        prev.next = current.next
    # This function is used to print the login information of the user from the hash table.
    def print_hash_table(self):
        for i in range(self.size):
            print("index:", i)
            temp = self.HashTable[i]
            while temp:
                print(temp.userName, temp.password)
                temp = temp.next

# This function is made to test the working of login information of the user.
'''
if __name__ == "__main__":
    h1 = HashTable()
    option = 0
    while option != 3:
        print("1. signup")
        option = int(input())
        if option == 1:
            email = input("Email :")
            first_name = input("first name :")
            last_name = input("last Name :")
            password = int(input("password :"))
            h1.insert(first_name, last_name, email, password)
    email = input()
    password = int(input())
    print(h1.search(password, email))
    h1.print_hash_table()
'''
