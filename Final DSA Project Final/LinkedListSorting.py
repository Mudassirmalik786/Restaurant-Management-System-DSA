# Description: This file contains the sorting algorithms for the linked list
from Foodmenu import MenuLinkedList

# This function is used to sort the food information of the menu in ascending order of price using bubble sort.
def bubble_sort_on_MenuLinkedList(menuFood, key):
    if menuFood.head is None or menuFood.head.next_item is None:
        return menuFood

    for i in range(menuFood.getLength() - 1):
        current = menuFood.head
        prev = None

        for j in range(menuFood.getLength() - i - 1):
            next_node = current.next_item

            if key == 'price':
                if current.price > next_node.price:
                    if prev:
                        prev.next_item = next_node
                    else:
                        menuFood.head = next_node

                    current.next_item = next_node.next_item
                    next_node.next_item = current

                    current, next_node = next_node, current
            elif key == 'name':
                if current.name > next_node.name:
                    if prev:
                        prev.next_item = next_node
                    else:
                        menuFood.head = next_node

                    current.next_item = next_node.next_item
                    next_node.next_item = current

                    current, next_node = next_node, current

            prev = current
            current = current.next_item

    return menuFood

# This function is used to sort the food information of the menu in ascending order of price using selection sort.
def insertion_sort_on_MenuLinkedList(menuFood, key):
    if menuFood.head is None or menuFood.head.next_item is None:
        return menuFood

    sorted_head = None

    current = menuFood.head
    while current:
        next_node = current.next_item
        if key == 'price':
            if sorted_head is None or sorted_head.price > current.price:
                current.next_item = sorted_head
                sorted_head = current
            else:
                search = sorted_head
                while search.next_item and search.next_item.price < current.price:
                    search = search.next_item
                current.next_item = search.next_item
                search.next_item = current
        elif key == 'name':
            if sorted_head is None or sorted_head.name.casefold() > current.name.casefold():
                current.next_item = sorted_head
                sorted_head = current
            else:
                search = sorted_head
                while search.next_item and search.next_item.name.casefold() < current.name.casefold():
                    search = search.next_item
                if search.next_item and search.next_item.name.casefold() == current.name.casefold():
                    if search.next_item.name < current.name:
                        current.next_item = search.next_item
                        search.next_item = current
                    else:
                        current.next_item = search.next_item.next_item
                        search.next_item.next_item = current
                else:
                    current.next_item = search.next_item
                    search.next_item = current
        current = next_node
    menuFood.head = sorted_head
    return menuFood
