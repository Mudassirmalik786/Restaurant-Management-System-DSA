# Description: This file contains the functions that are used to load the data from the csv files and save the data to the csv files.
import Foodmenu
import LoginPythonFile
import csv
import os

CustomerHash = LoginPythonFile.HashTable()
menuLinkedList = Foodmenu.MenuLinkedList()
# This function is used to save all the login information of the user in the hash table to the csv file.
def save_all_data_of_Customer(CustomerHash):
    file_path = "CustomerLogin.csv"
    arr = CustomerHash.access_all_elements()
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(arr)):
            data = [arr[i].userName, arr[i].password, arr[i].Bill]
            writer.writerow(data)

# This function is used to load data of customer from the csv file to the hash table.
def read_Customer(file_path):
    if not os.path.exists(file_path):
        createFile(file_path)
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            userName = row[0]
            passcode = int(row[1])
            CustomerHash.insert(userName, passcode)
    return CustomerHash

# This function is used to create a csv file.
def createFile(file_path):
    with open(file_path, 'w', newline='') as file:
        pass

# This function is used to load the food information of the menu from the csv file.
def read_foodMenu():
    file_path = "FoodMenuFile.csv"
    if not os.path.exists(file_path):
        createFile(file_path)
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            FoodName = row[0]
            Price = int(row[1])
            menuLinkedList.add_item(FoodName, Price)
    return menuLinkedList

# This function is used to save the food information of the menu to the csv file.
def write_foodMenu(menuFood):
    file_path = "FoodMenuFile.csv"
    print("In Food Menu Written")
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(menuFood.getLength()):
            foodItem = menuFood.getobjectbyIndex(i)
            writer.writerow([foodItem.name, foodItem.price])

# This function is used to save the food information of the menu to the csv file.
def write_foodItem_to_csv(name, price):
    file_path = "FoodMenuFile.csv"
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, str(price)])

