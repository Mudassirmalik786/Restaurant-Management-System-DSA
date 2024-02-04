# Libraries of python used in this application.
import sys
import csv
import time
import re
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem, QTableWidget, \
    QPushButton, QLineEdit, QTextEdit, QListWidget, QListWidgetItem
from bst import BST
import LinkedListSorting
import Foodmenu
import LoginPythonFile
import loadHelper

# Global Variables
AdminName = "AAMZ"
PasswordName = 30
file_path = "CustomerLogin.csv"
menuFood = loadHelper.read_foodMenu()
CustomerHash = loadHelper.read_Customer(file_path)
OrderList = Foodmenu.OrderMenuLinkedList()
employee_data=BST()

# Function to show congratulations message
def show_congratulations():
    QMessageBox.information(None, "Congratulations", "Operation completed successfully!")

# function to save one entry in the csv file
def saveoneEntry(userName, passcode, file_path):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        data = [userName, passcode, 0]
        writer.writerow(data)

# Class to add reviews
class AddReview(QDialog):
    # Constructor
    def __init__(self):
        super(AddReview, self).__init__()
        loadUi("AddReviews.ui", self)
        self.setFixedSize(self.size())
        self.initUI()
    # Function to initialize UI
    def initUI(self):
        try:
            self.review_textbox = self.findChild(QTextEdit, 'AddReviewBox')
            self.myCust = None
            self.send_button = self.findChild(QPushButton, 'AddReviewSaveButton')
            self.send_button.clicked.connect(self.save_review)
        #self.AddReviewBackButton = self.findChild(QPushButton, 'AddReviewBackButton')
            self.AddReviewBackButton.clicked.connect(self.close_window)
            self.reviews_list = []
        except Exception as e:
            print(e)
    # Function to save review
    def save_review(self):
        review_text = self.review_textbox.toPlainText()

        if not review_text.strip():
            QMessageBox.warning(self, "Warning", "Please write a review before saving.")
            return

        self.reviews_list.append(review_text)
        self.save_reviews_to_file()

        self.review_textbox.clear()
        QMessageBox.information(self, "Success", "Review added successfully!")
    # Function to close window
    def save_reviews_to_file(self):
        with open('reviews.txt', 'a') as file:
            for review in self.reviews_list:
                file.write(review + '\n')
    # Function to close window
    def close_window(self):
        if not self.myCust:
            self.myCust = CustomerMenu()
        self.myCust.show()
        self.close()

# Class to delete employees
class DeleteEmployees(QDialog):
    # Constructor
    def __init__(self):
        super(DeleteEmployees, self).__init__()
        try:
            loadUi("DeleteEmployee.ui", self)
            self.setFixedSize(self.size())
            self.ViewEmployeeBackButton.clicked.connect(self.close_window)
        # self.ViewEmployeeBackButton = self.findChild(QPushButton,'ViewEmployeeBackButton')
        # self.ViewEmployeeBackButton.clicked.connect(self.close_window)
            self.IDTXT = self.findChild(QLineEdit, 'IDTXT')
            self.deleteEmployeeButton = self.findChild(QPushButton, 'deleteEmployeeBtn')
            self.deleteEmployeeButton.clicked.connect(self.delete_employee)
            self.tableWidget = self.findChild(QTableWidget, 'tableWidget')
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Name"])
            self.myAdmin = None
            self.load_data_from_csv()
            self.populate_table_widget()
        except Exception as e:
            print(e)
    # Function to close window
    def close_window(self):
        if not self.myAdmin:
            self.myAdmin = AdminMenu()
        self.myAdmin.show()
        self.close()
    # Function to delete employee
    def delete_employee(self):
        try:
            ID = self.IDTXT.text().strip()
            if not ID:
                self.show_warning_message("Please enter an ID.")
                self.IDTXT.clear()
                return
            try:
                id=int(ID)
            except:
                self.show_warning_message("Please enter an Integer.")
                self.IDTXT.clear()
                return
            current=employee_data.search(id)
            if not current:
                self.show_warning_message("Employee Not Found")
                self.IDTXT.clear()
                return
            else:
                employee_data.delete(id)
            self.populate_table_widget()
            self.save_data_to_csv()
            self.IDTXT.clear()
        except Exception as e:
            print(e)
    # Function to show warning message
    def show_warning_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Warning")
        msg_box.exec_()
    # Function to populate table widget
    def populate_table_widget(self):
        self.tableWidget.setRowCount(0)
        for row, (employee_id, name) in enumerate(employee_data.in_order_traversal()):
            self.tableWidget.insertRow(row)
            item_id = QTableWidgetItem(str(employee_id))
            item_name = QTableWidgetItem(name)
            self.tableWidget.setItem(row, 0, item_id)
            self.tableWidget.setItem(row, 1, item_name)
    # Function to load data from csv
    def load_data_from_csv(self):
        try:
            with open('employees.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    employee_id = int(row["ID"])
                    name = row["Name"]
                    employee_data.insert(employee_id, name)
        except FileNotFoundError:
            pass
    # Function to save data to csv
    def save_data_to_csv(self):
        with open('employees.csv', 'w', newline='') as file:
            fieldnames = ["ID", "Name"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for employee_id, name in employee_data.in_order_traversal():
                writer.writerow({"ID": employee_id, "Name": name})
# Class to add employees
class AlphabetValidator(QRegularExpressionValidator):
    def __init__(self):
        super().__init__(QRegularExpression("[a-zA-Z\s]+"))

    def validate(self, input_str, pos):
        state, input_str, pos = super().validate(input_str, pos)
        if state == QRegularExpressionValidator.Acceptable:
            return state, input_str, pos
        elif input_str == '':
            return QRegularExpressionValidator.Intermediate, input_str, pos
        else:
            return QRegularExpressionValidator.Invalid, input_str, pos

class AddEmployees(QDialog):
    # Class variable to keep track of the last assigned employee ID
    last_employee_id = 0

    # Constructor
    def __init__(self):
        super(AddEmployees, self).__init__()
        loadUi("AddEmployee.ui", self)
        self.setFixedSize(self.size())
        try:
            self.ViewEmployeeBackButton.clicked.connect(self.close_window)
            self.nameTXT = self.findChild(QLineEdit, 'nameTXT')
            self.nameTXT.setValidator(AlphabetValidator())  # Set custom validator
            self.addEmployeeButton = self.findChild(QPushButton, 'addEmployeeBtn')
            self.addEmployeeButton.clicked.connect(self.add_employee)
            self.tableWidget = self.findChild(QTableWidget, 'tableWidget')
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Name"])
            self.myAdmin = None
            self.load_data_from_csv()
            self.populate_table_widget()
        except Exception as e:
            print(e)

    # Function to close window
    def close_window(self):
        if not self.myAdmin:
            self.myAdmin = AdminMenu()
        self.myAdmin.show()
        self.close()

    # Function to add employee
    def add_employee(self):
        name = self.nameTXT.text().strip()

        if not name:
            self.show_warning_message("Please enter a name.")
            self.nameTXT.clear()
            return

        # Increment the last assigned employee ID to generate a new unique ID
        AddEmployees.last_employee_id += 1
        employee_id = AddEmployees.last_employee_id

        employee_data.insert(employee_id, name)

        self.populate_table_widget()
        self.save_data_to_csv()
        self.nameTXT.clear()

    # Function to load data from csv
    def load_data_from_csv(self):
        try:
            with open('employees.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    employee_id = int(row["ID"])
                    name = row["Name"]
                    employee_data.insert(employee_id, name)
                    # Update the last assigned employee ID if necessary
                    if employee_id > AddEmployees.last_employee_id:
                        AddEmployees.last_employee_id = employee_id
        except FileNotFoundError:
            pass

    # Function to save data to csv
    def save_data_to_csv(self):
        with open('employees.csv', 'a', newline='') as file:  # Open in append mode
            fieldnames = ["ID", "Name"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Only write header if the file is empty
            if file.tell() == 0:
                writer.writeheader()

            for employee_id, name in employee_data.in_order_traversal():
                writer.writerow({"ID": employee_id, "Name": name})

    # Function to show warning message
    def show_warning_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Warning")
        msg_box.exec_()

    # Function to populate table widget
    def populate_table_widget(self):
        self.tableWidget.setRowCount(0)
        for row, (employee_id, name) in enumerate(employee_data.in_order_traversal()):
            self.tableWidget.insertRow(row)
            item_id = QTableWidgetItem(str(employee_id))
            item_name = QTableWidgetItem(name)
            self.tableWidget.setItem(row, 0, item_id)
            self.tableWidget.setItem(row, 1, item_name)

 #-------

# Class to show another window
class AnotherWindow(QMainWindow):
    def __init__(self):
        super(AnotherWindow, self).__init__()
        loadUi("adminMenu.ui", self)
        self.setFixedSize(self.size())

# Class to show final order
class OrderFormClass(QMainWindow):
    def __init__(self):
        super(OrderFormClass, self).__init__()
        loadUi("View Final Order.ui", self)
        self.setFixedSize(self.size())
        loadOrderData(self)
        self.myCust = None
        self.backBTN.clicked.connect(self.close_Window)
    # Function to close window
    def close_Window(self):
        if not self.myCust:
            self.myCust = CustomerMenu()
        self.myCust.show()
        self.close()

# Class to show customer menu
class CustomerMenu(QMainWindow):
    # Constructor
    def __init__(self, cust=None):
        self.cust = cust
        super(CustomerMenu, self).__init__()
        loadUi("customerMenu.ui", self)
        self.setFixedSize(self.size())
        try:
            self.backBTN.clicked.connect(self.close_window)
            self.myMenu = None
            self.ViewFoodMenu.clicked.connect(self.show_Menu)
            self.myFinalOrder = None
            self.viewFinalOrder.clicked.connect(self.showFinalOrder)
            self.myReview=None
            self.GiveReviews.clicked.connect(self.add_Reviews)
        except Exception as e:
            print(e)
    # Function to add reviews
    def add_Reviews(self):
        try:
            if not self.myReview:
                self.myReview = AddReview()
            self.hide()
            self.myReview.show()
        except Exception as e:
            print(e)
    # Function to close window
    def showFinalOrder(self):

        if not self.myFinalOrder:
            self.myFinalOrder = OrderFormClass()
            print("in If")
        self.myFinalOrder.show()
        print("Outside If")
        self.close()
    # function to show menu
    def show_Menu(self):
        if not self.myMenu:
            self.myMenu = viewMenuUI()
        self.myMenu.show()
        self.close()
    # Function to close window
    def close_window(self):
        self.close()
        main_window.show()

# Class to show customer menu
class viewMenuUI(QMainWindow):
    # Constructor
    def __init__(self):
        super(viewMenuUI, self).__init__()
        loadUi("View Food Menu.ui", self)
        self.setFixedSize(self.size())
        loadDataofFoodMenu(self)
        self.orderButton.clicked.connect(self.addtoOrder)
        self.deleteOrder.clicked.connect(self.deleteOrderItem)
        self.myCust = None
        self.backBTN.clicked.connect(self.close_Window)
    # Function to close window
    def close_Window(self):
        if not self.myCust:
            self.myCust = CustomerMenu()
        self.myCust.show()
        self.close()
    # Function to delete order item
    def deleteOrderItem(self):
        try:
            foodName = self.itemNameTXT.text()
            user_input = self.quantityTXT.text()
            if not foodName or not user_input:
                QMessageBox.critical(self, "Error", "Kindly Enter name and Quantity")
                return
            foodName = foodName.lower().strip()
            user_input = user_input.strip()
            current = OrderList.find_item(foodName)
            if current:
                try:
                    quantity = int(user_input)
                except:
                    QMessageBox.critical(self, "Error", "Kindly Enter Quantity in Numbers")
                    return
                if quantity == current.quantity:
                    OrderList.delete_item(foodName)
                    loadDataofFoodMenu(self)
                    self.quantityTXT.setText("")
                    self.itemNameTXT.setText("")
                    QMessageBox.critical(self, "Congratulations", "Item Removed From Order")
                    return
                elif quantity < current.quantity:
                    current.quantity = current.quantity - quantity
                    loadDataofFoodMenu(self)
                    self.quantityTXT.setText("")
                    self.itemNameTXT.setText("")
                    QMessageBox.critical(self, "Congratulations", "Item Decreased From Order")
                    return
                else:
                    QMessageBox.critical(self, "Error", "You are entering Quantity greater than Your Order")
                    return
            else:
                QMessageBox.critical(self, "Error", "Not Found")
                return
        except Exception as e:
            print(e)
    # Function to add to order
    def addtoOrder(self):
        try:
            foodName = self.itemNameTXT.text()
            user_input = self.quantityTXT.text()
            if not foodName or not user_input:
                QMessageBox.critical(self, "Error", "Kindly Enter name and Quantity")
                return
            foodName = foodName.lower().strip()
            user_input = user_input.strip()
            current = None
            current = menuFood.find_item(foodName)
            if current:
                try:
                    quantity = int(user_input)
                except:
                    QMessageBox.critical(self, "Error", "Kindly Enter Quantity in Numbers")
                    return
                OrderList.add_item(foodName, current.price, quantity)
                loadDataofFoodMenu(self)
                self.quantityTXT.setText("")
                self.itemNameTXT.setText("")
                show_congratulations()
            else:
                QMessageBox.critical(self, "Error", "Kindly Enter from the Shown Menu")
                return
        except Exception as e:
            print(e)

# Class to show customer menu
class ChangeMenu(QMainWindow):
    def __init__(self):
        super(ChangeMenu, self).__init__()
        loadUi("EditFoodMenu.ui", self)
        self.setFixedSize(self.size())
        loadData(self)
        self.addFood.clicked.connect(self.addFoodItem)
        self.deleteCustomer.clicked.connect(self.deleteFoodItem)
        self.myMenu = None
        self.backButton.clicked.connect(self.close_window)
        self.priceBtn.clicked.connect(self.SortOnPrice)
        self.nameBtn.clicked.connect(self.SortOnName)
    # funcion to sort the price
    def SortOnPrice(self):
        try:
            sortBase = self.SortBox.currentText()
            if sortBase=="Sort by Using:":
                QMessageBox.critical(self,"Error","Please Select any Sort")
                return
            elif sortBase == "Bubble Sort":
                LinkedListSorting.bubble_sort_on_MenuLinkedList(menuFood,"price")
            elif sortBase == "Insertion Sort":
                LinkedListSorting.insertion_sort_on_MenuLinkedList(menuFood, "price")
            loadData(self)
            self.SortBox.setCurrentText("Sort by Using:")
        except Exception as e:
            print(e)
    # Function to sort by name
    def SortOnName(self):
        try:
            sortBase = self.SortBox.currentText()
            if sortBase=="Sort by Using:":
                QMessageBox.critical(self,"Error","Please Select any Sort")
                return
            elif sortBase == "Bubble Sort":
                LinkedListSorting.bubble_sort_on_MenuLinkedList(menuFood,"name")
            elif sortBase == "Insertion Sort":
                LinkedListSorting.insertion_sort_on_MenuLinkedList(menuFood, "name")
            loadData(self)
            self.SortBox.setCurrentText("Sort by Using:")
        except Exception as e:
            print(e)
    # Function to close window
    def close_window(self):
        if not self.myMenu:
            self.myMenu = AdminMenu()
        self.myMenu.show()
        self.close()
    # Function to delete food item
    def deleteFoodItem(self):
        nameFood = self.foodNameTxt.text()
        self.priceTxt.setText("")
        if not nameFood:
            QMessageBox.critical(self, "Error", "Kindly Enter Food Name")
            return
        nameFood = nameFood.strip().lower()
        current = None
        current = menuFood.find_item(nameFood)
        try:
            if current:
                print("In Delete Food 1")
                menuFood.delete_item(nameFood)
                print("In Delete Food 2")
                loadHelper.write_foodMenu(menuFood)
                loadData(self)
                self.foodNameTxt.setText("")
                self.priceTxt.setText("")
            else:
                QMessageBox.critical(self, "Error", "Item not Found")
                return
        except Exception as e:
            print(e)
            return
    # Function to add food item
    def addFoodItem(self):
        try:
            nameFood = self.foodNameTxt.text()
            priceFood = self.priceTxt.text()
            if not nameFood or not priceFood:
                QMessageBox.critical(self, "Error", "Kindly Enter both Food Name and Price")
                return
            try:
                nameFood = nameFood.strip().lower()
                priceFood = priceFood.strip().lower()
                price = int(priceFood)
            except ValueError:
                QMessageBox.critical(self, "Error", "Price should be Numbers")
                return
            if price > 0:
                if menuFood.checkifAbsent(nameFood):
                    try:
                        menuFood.add_item(nameFood, price)
                        loadHelper.write_foodItem_to_csv(nameFood, price)
                        loadData(self)
                        self.foodNameTxt.setText("")
                        self.priceTxt.setText("")
                    except Exception as e:
                        print(e)
                        return
                else:
                    QMessageBox.critical(self, "Error", "Item already Exists")
            else:
                QMessageBox.critical(self, "Error", "Price should be Greater than 0")
        except Exception as e:
            print(e)


# Class to show customer menu
class showCustomer(QMainWindow):
    def __init__(self):
        super(showCustomer, self).__init__()
        loadUi("View Customer.ui", self)
        self.setFixedSize(self.size())
        loadCustomerData(self)
        try:
            # pass
            self.myMenu = None
            self.updateButton.clicked.connect(self.updateCustomer)
            self.deleteButton.clicked.connect(self.deleteCustomer)
            self.backBTN.clicked.connect(self.close_Window)
        except Exception as e:
            print(e)
    # Function to close window
    def close_Window(self):
        self.myMenu = AdminMenu()
        self.myMenu.show()
        self.close()
    # Function to update customer
    def updateCustomer(self):
        try:
            name = self.userNameTxt.text()
            user_input = self.passwordTXT.text()
            price = self.BillTXT.text()
            print("1")
            if not name or not user_input:
                QMessageBox.critical(self, "Error", "Kindly Enter Username and Password")
                return
            try:
                password = int(user_input)
            except ValueError:
                QMessageBox.critical(self, "Error", "Password should be Numbers")
                return
            current = CustomerHash.search(name, password)
            print("2")
            if current:
                try:
                    print("3")
                    print(current.userName)
                    Bill = int(price)
                    print("4")
                except:
                    QMessageBox.critical(self, "Error", "Kindly Enter Price greater than 0")
                    return
                current.Bill = Bill
                print("5")
                loadCustomerData(self)
                QMessageBox.critical(self, "Congratulations! ", "Bill Changed")
                self.userNameTxt.setText("")
                self.passwordTXT.setText("")
                self.BillTXT.setText("")
            else:
                QMessageBox.critical(self, "Error", "Customer not Found")
                return
            loadHelper.save_all_data_of_Customer(CustomerHash)

            print("6")
        except Exception as e:
            print(e)
    # Function to delete customer
    def deleteCustomer(self):
        try:
            name = self.userNameTxt.text()
            user_input = self.passwordTXT.text()
            self.BillTXT.setText("")  # Corrected line to clear the text field
            if not name or not user_input:
                QMessageBox.critical(self, "Error", "Kindly Enter Username and Password")
                return
            try:
                password = int(user_input)
            except ValueError:
                QMessageBox.critical(self, "Error", "Password should be Numbers")
                return
            current = CustomerHash.search(str(name), password)
            if current:
                CustomerHash.delete_from_hash_table(name, password)
                loadCustomerData(self)
                self.userNameTxt.setText("")
                self.passwordTXT.setText("")
                self.BillTXT.setText("")
                QMessageBox.critical(self, "Congratulations", "Customer Deleted")
            else:
                QMessageBox.critical(self, "Error", "Customer not Found")
                return
            loadHelper.save_all_data_of_Customer(CustomerHash)
        except Exception as e:
            print(e)

# Class to show reviews
class ViewReviews(QDialog):
    try:
        # Constructor
        def __init__(self):
            super(ViewReviews, self).__init__()
            loadUi("ViewReviews.ui", self)
            self.setFixedSize(self.size())
            self.review_list_widget = self.findChild(QListWidget, 'listWidget')
            self.myAdmin = None
            self.ViewReviewsBackButton.clicked.connect(self.close_window)
            self.view_reviews()  # Load reviews from file
    except Exception as e:
        print(e)
    # Function to view reviews
    def view_reviews(self):
        self.reviews_list = []
        try:
            with open('reviews.txt', 'r') as file:
                self.reviews_list = file.readlines()
        except FileNotFoundError:
            pass
        self.update_review_list_widget()
    # Function to update review list widget
    def update_review_list_widget(self):
        self.review_list_widget.clear()
        for review in self.reviews_list:
            item = QListWidgetItem(review.strip())
            self.review_list_widget.addItem(item)
    # Function to close window
    def close_window(self):
        if not self.myAdmin:
            self.myAdmin=AdminMenu()
        self.myAdmin.show()
        self.close()

# Class to show admin menu
class AdminMenu(QMainWindow):
    # Constructor
    def __init__(self):
        super(AdminMenu, self).__init__()
        loadUi("adminMenu.ui", self)
        self.setFixedSize(self.size())
        self.setFixedSize(self.size())
        self.BackBTN.clicked.connect(self.close_window)
        self.myMenu = None
        self.ChangePricesOFFood.clicked.connect(self.show_Menu)
        self.viewCust = None
        self.ViewCusotmers.clicked.connect(self.show_Customers)
        self.cust_Bill = None
        # self.ViewFoodMenu.clicked.connect()
        self.newEmployee = None
        self.EditEmployees.clicked.connect(self.show_Employee_Form)
        self.deleteEmployee.clicked.connect(self.show_delete_Employee)
        self.myReview = None
        self.ViewReviews.clicked.connect(self.show_Reviews)

    # Function to show delete employee menu
    def show_delete_Employee(self):
        if not self.newEmployee:
            self.newEmployee = DeleteEmployees()
        self.newEmployee.show()
        self.close()
    # Function to show reviews
    def show_Reviews(self):
        try:
            if not self.myReview:
                self.myReview = ViewReviews()
            self.myReview.show()
            self.close()
        except Exception as e:
            print(e)
    # Function to show menu
    def show_Menu(self):
        if not self.myMenu:
            self.myMenu = ChangeMenu()
        self.myMenu.show()
        self.close()
    # Function to show customers
    def show_Customers(self):
        if not self.viewCust:
            self.viewCust = showCustomer()
        self.viewCust.show()
        self.close()
    # Function to show employee form
    def show_Employee_Form(self):
        if not self.newEmployee:
            self.newEmployee = AddEmployees()
        self.newEmployee.show()
        self.close()
    # Function to close window
    def close_window(self):
        self.close()
        main_window.show()

# Class to show login form
class LoginForm(QMainWindow):
    # Constructor
    def __init__(self):
        super(LoginForm, self).__init__()
        self.customerMenu = None
        self.adminMenu = None
        loadUi("ResturantLogin.ui", self)
        self.setFixedSize(self.size())
        self.setFixedSize(self.size())
        self.SignUpButton.clicked.connect(self.newloginfunction)
        self.SigninButton.clicked.connect(self.loginfunction)
        self.BackBTN.clicked.connect(self.close_Window)
    
    # Function to close window
    def close_Window(self):
        self.close()
    # Function of new login either customer or admin
    def newloginfunction(self):
        try:
            user_input = 0
            userName = self.userNameTXT.text()
            password = self.passwordTXT.text()
            Role = self.RoleBox.currentText()
            if not password or not userName:
                QMessageBox.critical(self, "Error", "Please fill in both email and password fields ")
                return
            if Role == "Select your Role":
                QMessageBox.critical(self, "Error", " Select your Role.")
                return
            try:
                user_input = int(password)
            except ValueError:
                QMessageBox.critical(self, "Error", "Password should be Numbers ")
                return
            if Role == "Admin":
                QMessageBox.critical(self, "Error", "Admin can't Signup")
                return
            elif Role == "Customer":
                if not CustomerHash.search(userName, user_input):
                    CustomerHash.insert(userName, user_input, 0)
                    saveoneEntry(userName, user_input, file_path);
                    if not self.customerMenu:
                        self.customerMenu = CustomerMenu()
                    self.hide()
                    self.customerMenu.show()
                    self.RoleBox.setCurrentText()
                    self.userNameTXT.setText("")
                    self.passwordTXT.setText("")
                else:
                    QMessageBox.critical(self, "Error", "Customer Exist")
                    return
        except Exception as e:
            print(e)
    # Function to login either customer or admin
    def loginfunction(self):
        user_input = 0
        userName = self.userNameTXT.text()
        password = self.passwordTXT.text()
        Role = self.RoleBox.currentText()
        if not password or not userName:
            QMessageBox.critical(self, "Error", "Please fill in both email and password fields ")
            return
        if Role == "Select your Role":
            QMessageBox.critical(self, "Error", " Select your Role.")
            return
        try:
            user_input = int(password)
        except ValueError:
            QMessageBox.critical(self, "Error", "Password should be Numbers ")
            return

        if Role == "Admin":
            try:
                if userName == AdminName and user_input == PasswordName:
                    if not self.adminMenu:
                        self.adminMenu = AdminMenu()
                    self.hide()
                    self.adminMenu.show()
                    self.RoleBox.setCurrentText()
                    self.userNameTXT.setText("")
                    self.passwordTXT.setText("")
                else:
                    QMessageBox.critical(self, "Error", "Incorrect Username for Admin")
                    return
            except Exception as e:
                print(e)
        elif Role == "Customer":
            try:
                if CustomerHash.search(userName, user_input):
                    cust = CustomerHash.search(userName, user_input)
                    if not self.customerMenu:
                        self.customerMenu = CustomerMenu(cust)
                    self.hide()
                    self.customerMenu.show()
                    self.RoleBox.setCurrentText()
                    self.userNameTXT.setText("")
                    self.passwordTXT.setText("")
                else:
                    QMessageBox.critical(self, "Error", "Incorrect Username or Password")
                    return
            except Exception as e:
                print(e)

# Function to show another form
def show_another_form(self):
    if not self.another_window:  # Check if the form instance exists
        self.another_window = AnotherWindow()  # Create instance if not exists
    self.hide()  # Hide the current window
    self.another_window.show()  # Show the other window  # time.sleep(10)

# Function to show another form
def loadData(self):
    print("Length", menuFood.getLength())
    try:
        self.foodTable.setColumnCount(2)
        self.foodTable.setRowCount(menuFood.getLength())
        row = 0
        for i in range(menuFood.getLength()):
            foodItem = menuFood.getobjectbyIndex(i)
            self.foodTable.setItem(row, 0, QTableWidgetItem(str(foodItem.name)))
            self.foodTable.setItem(row, 1, QTableWidgetItem(str(foodItem.price)))
            row += 1
    except Exception as e:
        print("An error occurred:", str(e))

# Function to load customer data
def loadCustomerData(self):
    try:
        myArray = []
        myArray = CustomerHash.access_all_elements()
        self.customerTable.setColumnCount(3)
        self.customerTable.setRowCount(len(myArray))
        row = 0
        for i in range(0, len(myArray)):
            singleCust = myArray[i]
            self.customerTable.setItem(row, 0, QTableWidgetItem(str(singleCust.userName)))
            print(singleCust.password)
            self.customerTable.setItem(row, 1, QTableWidgetItem(str(singleCust.password)))
            self.customerTable.setItem(row, 2, QTableWidgetItem(str(singleCust.Bill)))
            row += 1
    except Exception as e:
        print("An error occurred:", str(e))

# Function to load food menu data
def loadDataofFoodMenu(self):
    try:
        self.foodMenuTable.setColumnCount(2)
        self.foodMenuTable.setRowCount(menuFood.getLength())
        row = 0
        for i in range(menuFood.getLength()):
            foodItem = menuFood.getobjectbyIndex(i)
            self.foodMenuTable.setItem(row, 0, QTableWidgetItem(str(foodItem.name)))
            self.foodMenuTable.setItem(row, 1, QTableWidgetItem(str(foodItem.price)))
            row = row + 1
    except Exception as e:
        print("An error occurred:", str(e))

# Function to load order data
def loadOrderData(self):
    try:
        TotalBill = 0
        self.orderTable.setColumnCount(4)
        self.orderTable.setRowCount(OrderList.getlength())
        row = 0
        for i in range(OrderList.getlength()):
            foodItem = OrderList.getobjectbyIndex(i)
            self.orderTable.setItem(row, 0, QTableWidgetItem(str(foodItem.name)))
            self.orderTable.setItem(row, 1, QTableWidgetItem(str(foodItem.price)))
            self.orderTable.setItem(row, 2, QTableWidgetItem(str(foodItem.quantity)))
            self.orderTable.setItem(row, 3, QTableWidgetItem(str(foodItem.price * foodItem.quantity)))
            Bill = foodItem.price * foodItem.quantity
            TotalBill = TotalBill + Bill
            row = row + 1
        self.totalBill.setText(str(TotalBill))
    except Exception as e:
        print("An error occurred:", str(e))

# Main function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = LoginForm()
    main_window.show()
    sys.exit(app.exec_())
