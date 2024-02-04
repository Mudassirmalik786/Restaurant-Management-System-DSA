# Description: This file contains the MenuItem class which is used to create a linked list of menu items. Each menu item has a name, price, and quantity. The next_item variable is used to point to the next item in the linked list. The linked list is used to store the items that the user has ordered. This linked list is used to create the receipt for the user.
class MenuItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.next_item = None
