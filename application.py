from abc import ABC, abstractmethod

from users import *
from manager import *
from viewers import *
from orders import OrderBuilder, ShoppingCart

def ApplicationHandler(func):
    def Handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return Handler

class Application(ABC):
    @abstractmethod
    def initialize(self):
        pass

class CustomerApplication(Application):
    """Class to handle all customer operations"""

    def __init__(self, database):
        self._database = database
        self._customer = Customer()

        self._cart = ShoppingCart()

    def initialize(self):
        connected = self._database.connect()
        if (not connected):
            raise Exception("Unable to connect to database. Try again later.")

        self._login_manager = LoginManager(self._database)
        self._customer_manager = CustomerManager(self._database)
        self._order_manager = OrderManager(self._database)
        self._menu_viewer = MenuViewer(self._database)

        return self

    @ApplicationHandler
    def signupForApplication(self, username, password,
                    first_name, last_name, phone_num,
                    email_address, payment=None):  
        """Allow customer to signup in application.

        username, password are properties of UserLogin class.
        first_name, last_name, phone_num, email_address, and payment
        are all properties of Customer class.

        When this method is called, request goes to Customer class
        to create the customer. At the same time, the user login
        class is invoked to create username/password combo.
        """

        try:
            self._customer = Customer.signup(
                username, password,
                first_name, last_name,
                phone_num, email_address,
                self._login_manager, self._customer_manager,
                payment)
        except Exception as e:
            print(e)

        return self._customer

    @ApplicationHandler
    def loginToApplication(self, username, password):
        return self._customer.login(username, password, self._login_manager)

    @ApplicationHandler
    def logoutOfApplication(self):
        return self._customer.logout(self._login_manager)

    @ApplicationHandler
    def addToCart(self, item):
        """Add an item to the cart"""

        if self._customer.isLoggedIn():
            self._cart.add(item)
        else:
            print("You must be logged in first.")

    @ApplicationHandler
    def removeFromCart(self, item):
        """Remove an item from the cart"""

        if self._customer.isLoggedIn():
            self._cart.remove(item)
        else:
            print("You must be logged in first.")

    def getCart(self):
        """Get all the items in the cart"""

        if self._customer.isLoggedIn():
            return self._cart.getCart()
        else:
            print("You must be logged in first.")

    @ApplicationHandler
    def placeOrder(self, payment=None):
        """Build an order and add it to system"""

        if self._customer.isLoggedIn():
            if self._customer.getPayment() is None and \
                    payment is None:
                print("You must choose payment before submitting order.")
                return

            if len(self._cart.getCart()) == 0:
                print("You must add items before submitting order.")
                return
                    
            # Create a builder and build the order
            builder = OrderBuilder()
            builder.setCustomer(
                self._customer.getFullName(),
                self._customer.getEmailAddress())
            if payment:
                builder.setPayment(payment)
            builder.setItems(self._cart)
            order = builder.build()

            print(order)

            # Once the order has been built, submit and empty
            # cart if the order was placed correctly.
            placed_order = self._order_manager.add(order)

            if placed_order:
                self._cart.emptyCart()
        else:
            print("You must be logged in first.")

    @ApplicationHandler
    def getCurrentOrders(self):
        return self._order_manager.getCurrentOrders()

class EmployeeApplication(Application):
    """Class to handle all customer operations"""

    def __init__(self, database):
        self._database = database

        self._employee = Employee()

        self._menu_manager = None 
        self._order_manager = None
        self._item_manager = None
        self._employee_manager = None
        self._login_manager = None

    def initialize(self):
        connected = self._database.connect()
        if (not connected):
            raise Exception("Unable to connect to database. Try again later.")

        self._menu_manager = MenuManagerProxy(self._employee, database=self._database)
        self._order_manager = OrderManagerProxy(self._employee, database=self._database)
        self._item_manager = ItemManagerProxy(self._employee, database=self._database)
        self._employee_manager = EmployeeManagerProxy(self._employee, database=self._database)
        self._customer_manager = CustomerManagerProxy(self._employee, database=self._database)
        self._login_manager = LoginManagerProxy(self._employee, database=self._database)

        return self

    @ApplicationHandler
    def loginToApplication(self, username, password):
        logged_in = self._employee.login(username, password, self._login_manager)
        if (not logged_in):
            print("You are already logged in!")

    @ApplicationHandler
    def logoutOfApplication(self, username):
        logged_out = self._employee.logout(username, self._login_manager)
        if (not logged_out):
            print("You are not logged in!")

    @ApplicationHandler
    def getUsersLoggedIn(self):
        return self._login_manager.getCurrentLogins()

    @ApplicationHandler
    def viewOrders(self):
        return self._order_manager.getCurrentOrders()

    ##########################################
    # Order Management
    ##########################################
    @ApplicationHandler
    def addOrder(self):
        pass

    @ApplicationHandler
    def editOrder(self):
        pass

    @ApplicationHandler
    def removeOrder(self):
        pass

    @ApplicationHandler
    def getOrders(self):
        pass

    ##########################################
    # Employee Management
    ##########################################
    @ApplicationHandler
    def addEmployee(self):
        pass

    @ApplicationHandler
    def editEmployee(self):
        pass

    @ApplicationHandler
    def removeEmployee(self):
        pass

    @ApplicationHandler
    def getEmployees(self):
        pass

    ##########################################
    # Menu Management
    ##########################################
    @ApplicationHandler
    def addMenu(self):
        pass

    @ApplicationHandler
    def editMenu(self):
        pass

    @ApplicationHandler
    def removeMenu(self):
        pass

    @ApplicationHandler
    def getMenus(self):
        pass

    ##########################################
    # Item Management
    ##########################################
    @ApplicationHandler
    def addItem(self, item):
        return self._item_manager.add(item)

    @ApplicationHandler
    def editItem(self):
        pass

    @ApplicationHandler
    def removeItem(self, item):
        return self._item_manager.remove(item)

    @ApplicationHandler
    def getItems(self):
        return self._item_manager.getCurrentItems()