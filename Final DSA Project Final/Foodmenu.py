# Purpose: This file contains the classes and methods for the menu and order menu linked lists.
# This class is used to create a node for the order menu linked list.
class OrderMenuitem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.next_item = None

# This class is used to create a node for the menu linked list.
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.next_item = None

# This class is used to create a linked list for the menu.
class MenuLinkedList:
    def __init__(self):
        self.head = None
    # This function is used to display the menu.
    def display_menu(self):
        current = self.head
        while current:
            print(f"Name: {current.name}, Price: ${current.price:.2f}")
            current = current.next_item
    # This function is used to add a food item to the menu.
    def add_item(self, name, price):
        try:
            new_item = MenuItem(name, price)
            new_item.next_item = self.head
            self.head = new_item
            print(name, "added to the menu.")
        except Exception as e:
            print(e)
            return
    # This function is used to get the food item from the menu by its index.
    def getobjectbyIndex(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current
            count += 1
            current = current.next_item
        return None
    # This function is used to get the length of the menu.
    def getLength(self):
        current = self.head
        length = 0

        while current:
            length += 1
            current = current.next_item

        return length
    # This function is used to find the food item from the menu by its name.
    def find_item(self, name):
        current = self.head
        while current:
            if current.name == name:
                return current
            current = current.next_item
        return None
    # This function is used to update the food item from the menu by its name.
    def update_item(self, name, new_price):
        item = self.find_item(name)
        if item:
            item.price = new_price
            print(name, "updated successfully.")
        else:
            print(name, "not found in the menu.")
    # This function is used to check if the food item is present in the menu by its name.
    def checkifAbsent(self, name):
        current = self.head
        while current:
            if current.name == name:
                return False
            current = current.next_item
        return True
    # This function is used to delete the food item from the menu by its name.
    def delete_item(self, name):
        current = self.head
        if current and current.name == name:
            self.head = current.next_item
            return
        prev = None
        while current and current.name != name:
            prev = current
            current = current.next_item
        if current is None:
            return
        prev.next_item = current.next_item
# This class is used to create a linked list for the order menu.
class OrderMenuLinkedList:
    def __init__(self):
        self.head = None
    # This function is used to display the order menu.
    def display_menu(self):
        current = self.head
        while current:
            print(f"Name: {current.name}, Price: ${current.price:.2f}, Quantity: {current.quantity}")
            current = current.next_item
    # This function is used to add a food item to the order menu.
    def add_item(self, name, price, quantity):
        new_item = OrderMenuitem(name, price, quantity)  # Fixed class name typo here
        new_item.next_item = self.head
        self.head = new_item
    # This function is used to find the food item from the order menu by its name.
    def find_item(self, name):
        current = self.head
        while current:
            if current.name == name:
                return current
            current = current.next_item
        return None
    # This function is used to update the food item from the order menu by its name.
    def update_item(self, name, new_price, new_quantity):
        item = self.find_item(name)
        if item:
            item.price = new_price
            item.quantity = new_quantity
            print(f"{name} updated successfully. New Price: ${new_price:.2f}, New Quantity: {new_quantity}")
        else:
            print(f"{name} not found in the menu.")
    # This function is used to delete the food item from the order menu by its name.
    def delete_item(self, name):
        current = self.head
        if current and current.name == name:
            self.head = current.next_item
            print(f"{name} deleted from the menu.")
            return
        prev = None
        while current and current.name != name:
            prev = current
            current = current.next_item
        if current is None:
            print(f"{name} not found in the menu.")
            return
        prev.next_item = current.next_item
        print(f"{name} deleted from the menu.")
    # This function is used to get the length of the order menu.
    def getlength(self):
        current = self.head
        length = 0
        while current:
            length += 1
            current = current.next_item
        return length
    # This function is used to get the food item from the order menu by its index.
    def getobjectbyIndex(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current
            count += 1
            current = current.next_item
        return None