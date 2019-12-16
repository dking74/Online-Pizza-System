#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: To define actors in system
#
#######################################################

from abc import ABC, abstractmethod
from enum import Enum

from orders import OrderStatus

class UsersInterface(ABC):
    """Interface for all users"""

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def updatePersonalInformation(self):
        pass

    @abstractmethod
    def isLoggedIn(self):
        pass

class AdminInterface(ABC):
    """Interface for admins"""

    @abstractmethod
    def isAdmin(self):
        pass

class Customer(UsersInterface):
    _UPDATE_FIELDS = [
        'first_name', "last_name", "phone_num", 
        "email_addr", "address", "paymentInfo"
    ]

    def __init__(self, first_name=None, last_name=None, phone_num=None, email_addr=None, paymentInfo=None):
        """Constructor for Customers

        @param: first_name: string
              : First name of customer
        @param: last_name: string
              : Last name of customer
        @param: phone_num: string
              : The phone number of customer
        @param: email_addr: string
              : The email address of customer
        @param: address: Address
              : The address of residence
        @param: paymentInfo: Payment
              : The payment info of user
        """
        self._first_name = first_name
        self._last_name = last_name
        self._phone_num = phone_num
        self._email_addr = email_addr
        #self._address = address

        self._payment = paymentInfo

        # Two instance variables determining if:
        # 1. user has clocked into system
        # 2. user has logged into system
        self._clockedin = False
        self._loggedin = False

    def __repr__(self):
        return (
            "\nCustomer(\n"
            "   first_name={0}\n"
            "   last_name={1}\n"
            "   phone_num={2}\n"
            "   email_address={3}\n"
            "   payment={4}\n" 
            ")"
            .format(
                self._first_name,
                self._last_name,
                self._phone_num,
                self._email_addr,
                self._payment)
        )

    def __str__(self):
            return (
            "\nCustomer(\n"
            "   first_name={0}\n"
            "   last_name={1}\n"
            "   phone_num={2}\n"
            "   email_address={3}\n"
            "   payment={4}\n" 
            ")"
            .format(
                self._first_name,
                self._last_name,
                self._phone_num,
                self._email_addr,
                self._payment)
        )

    @staticmethod
    def signup(username, password,
               first_name, last_name,
               phone_num, email_address,
               login_manager, customer_manager, payment=None):
        # Create the customer internally, then add the customer to the database
        new_customer = Customer(first_name, last_name, phone_num, email_address)
        new_login = UserLogin(username, password, "Customer")

        customer_created = customer_manager.get(new_customer)
        if customer_created:
            raise Exception("Your information already exists in our database.")
        user_created = login_manager.get(new_login)
        if user_created:
            raise Exception("Your login information is already taken.")
        
        # If we don't have the customer already available,
        # add the customer to database and return that customer.
        if (not customer_created and not user_created):
            id = customer_manager.add(new_customer)
            login_manager.add(new_login, id)
 
            return new_customer

    def login(self, username, password, login_viewer):
        login_var = UserLogin(username, password, "Customer")
        logins = login_viewer.getCustomer(login_var)

        if (logins):
            login_entry = logins[0]

            # Update all the properties of the current employee
            self._first_name = login_entry[0]
            self._last_name = login_entry[1]
            self._phone_num = login_entry[2]
            self._email_addr = login_entry[3]

            self._loggedin = True

        return self._loggedin

    def logout(self, login_viewer):
        self._loggedin = False

    def updatePersonalInformation(self, personal_info_dict):
        """Take in a dict of properties to changed.
        These are located in UPDATE_FIELDS
        """
        for key, value in personal_info_dict.items():
            if key in Customer._UPDATE_FIELDS:
                updated_key = "_" + key
                self.__dict__[updated_key] = value
            if key == "first_name":
                self.__dict__["_full_name"] = key + self._last_name
            if key == "last_name":
                self.__dict__["_full_name"] = self._first_name + key

    def getMenu(self, menu_viewer):
        return menu_viewer.getItems()

    def editItem(self, item, item_dict):
        for key, value in item_dict.items():
            if key in item._UPDATE_FIELDS:
                updated_key = "_" + key
                self.__dict__[updated_key] = value

    def editOrder(self, order, order_dict):
        for key, value in order_dict.items():
            if key in order._UPDATE_FIELDS:
                updated_key = "_" + key
                self.__dict__[updated_key] = value

    def submitOrder(self, order):
        return order.submit()

    def getOrderStatus(self, order):
        return order.getOrderStatus()

    def isLoggedIn(self):
        """Determine if user is logged into system"""
        return self._loggedin

    def getFirstName(self):
        return self._first_name

    def getLastName(self):
        return self._last_name

    def getFullName(self):
        name = (self._first_name + " " + self._last_name) if \
            (self._first_name is not None and self._last_name is not None) else \
            ""
        return name

    def getPhoneNumber(self):
        return self._phone_num

    def getEmailAddress(self):
        return self._email_addr

    def getPayment(self):
        return self._payment

class EmployeeType(Enum):
    ADMINISTRATOR = 1
    DRIVER        = 2
    BAKER         = 3
    DESKWORKER    = 4

class Employee(AdminInterface, UsersInterface):
    _UPDATE_FIELDS = [
        'FirstName', "LastName", "PhoneNumber",
        "EmailAddress", "Address", "Pay"
    ]

    def __init__(self, first_name=None, last_name=None, phone_num=None, email_addr=None, pay=None, employee_type=None):
        """Constructor for base class Employee

        @param: employee_type: EmployeeType
              : The type of employee user is
        @param: first_name: string
              : First name of employee
        @param: last_name: string
              : Last name of employee
        @param: phone_num: string
              : The phone number of employee
        @param: email_addr: string
              : The email address of employee
        @param: pay: float
              : What employee is paid
        """
        self._employee_type = employee_type or EmployeeType.DESKWORKER
        self._first_name = first_name
        self._last_name = last_name
        self._phone_num = phone_num
        self._email_addr = email_addr

        self._pay = pay

        # Two instance variables determining if:
        # 1. user has clocked into system
        # 2. user has logged into system
        self._clockedin = False
        self._loggedin = False

    def __str__(self):
        return (
            "Employee({0}, {1}, {2}, {3}, {4})"
            .format(str(self.getFirstName()),
                    str(self.getLastName()),
                    str(self.getEmployeeType()),
                    str(self.getPhoneNumber()),
                    str(self.getEmailAddress())))

    def login(self, username, password, login_manager):
        """Attempt to login through database.

        If there are results, change login of user, as well as other props.
        Then, return the logged in status
        """

        # Determine if login info exists for current employee loging in
        login_var = UserLogin(username, password, "Employee")
        logins = login_manager.getEmployee(login_var)

        # We can log the user in IF:
        # 1. The username/password combo exists
        # 2. The user is currently not already logged in
        if (logins and not self.isLoggedIn()):
            login_entry = logins[0]

            # Update all the properties of the current employee
            self.__class__ = Administrator

            self._first_name = login_entry[0]
            self._last_name = login_entry[1]
            self._phone_num = login_entry[2]
            self._email_addr = login_entry[3]
            self._pay = login_entry[4]
            self._employee_type = EmployeeType(login_entry[5])

            self._loggedin = True

            login_manager.edit(login_var, {"Status": 1})

        return self._loggedin

    def logout(self, username, login_manager):
        # If we are logged in, try to logout
        if (self.isLoggedIn()):
            self._loggedin = False

            # Get all the users currently logged in,
            # see if the username trying to logout is logged in,
            # and change status of that
            current_logins = login_manager.getCurrentLogins()
            for login in current_logins:
                if login.getUsername() == username:
                    login_manager.edit(login, {"Status": 0})

                    return True
        return False

    def clockin(self):
        self._clockedin = True

    def clockout(self):
        self._clockedin = False

    def updateOrderStatus(self, order, status):
        pass
        # order.orderStatus(status)

    def viewOrders(self, order_manager):
        """Print order charactistics out from order_manager"""

        return order_manager.getCurrentOrders()

    def updatePersonalInformation(self, personal_info_dict):
        """Take in a dict of properties to changed.
        These are located in UPDATE_FIELDS
        """
        for key, value in personal_info_dict.items():
            pass

    def isClockedIn(self):
        """Determine if user is clocked in"""
        return self._clockedin

    def isLoggedIn(self):
        """Determine if user is logged into system"""
        return self._loggedin

    def isAdmin(self):
        """If the employee type is admin, they are admin"""
        return (self._employee_type == EmployeeType.ADMINISTRATOR)

    def getFirstName(self):
        return self._first_name

    def getLastName(self):
        return self._last_name

    def getFullName(self):
        name = (self._first_name + " " + self._last_name) if \
            (self._first_name is not None and self._last_name is not None) else ""
        return name

    def getPhoneNumber(self):
        return self._phone_num

    def getEmailAddress(self):
        return self._email_addr

    def getPay(self):
        return self._pay

    def getEmployeeType(self):
        return self._employee_type.value

class Administrator(Employee):
    def __init__(self, first_name=None, last_name=None, phone_num=None, email_addr=None, address=None, pay=None):
        Employee.__init__(self, first_name=first_name, last_name=last_name, phone_num=phone_num, email_addr=email_addr, pay=pay, employee_type=EmployeeType.ADMINISTRATOR)

    def addMenu(self, menu):
        #return self._menu_manager.add(menu)
        pass

    def editMenu(self, menu, menu_dict):
        #return self._menu_manager.edit(menu, menu_dict)
        pass

    def removeMenu(self, menu):
        #return self._menu_manager.remove(menu)
        pass

    def addEmployee(self, employee):
        # self._employee_manager.add(employee)
        pass

    def editEmployee(self, employee, employee_dict):
        # self._employee_manager.edit(employee, employee_dict)
        pass
    
    def removeEmployee(self, employee):
        # self._employee_manager.remove(employee)
        pass

    def addOrder(self, order):
        # self._order_manager.add(order)
        pass

    def editOrder(self, order, order_dict):
        # self._employee_manager.edit(order, order_dict)
        pass
    
    def removeOrder(self, order):
        # self._order_manager.remove(order)
        pass

    def editTimeEntry(self, time, time_dict):
        # self._time_manager.edit(time, time_dict)
        pass

class DeliveryDriver(Employee):
    def __init__(self, first_name=None, last_name=None, phone_num=None, email_addr=None, address=None, pay=None):
        Employee.__init__(self, first_name=first_name, last_name=last_name, phone_num=phone_num, email_addr=email_addr, pay=pay, employee_type=EmployeeType.DRIVER)

    def pickupOrder(self, order):
        """Change order status to ready"""
        order.setOrderStatus(OrderStatus.READY)

    def driveOrder(self, order):
        """Change order status to on its way"""
        order.setOrderStatus(OrderStatus.ONITSWAY)

class Baker(Employee):
    def __init__(self, first_name=None, last_name=None, phone_num=None, email_addr=None, address=None, pay=None):
        Employee.__init__(self, first_name=first_name, last_name=last_name, phone_num=phone_num, email_addr=email_addr, pay=pay, employee_type=EmployeeType.BAKER)
    
    def prepareOrder(self, order):
        """Change order status to preparing"""
        order.setOrderStatus(OrderStatus.PREPARING)

    def finishOrder(self, order):
        """Change order status to completed"""
        order.setOrderStatus(OrderStatus.COMPLETED)

class DeskWorker(Employee):
    def __init__(self, first_name=None, last_name=None, phone_num=None, email_addr=None, pay=None):
        Employee.__init__(self, first_name=first_name, last_name=last_name, phone_num=phone_num, email_addr=email_addr, pay=pay, employee_type=EmployeeType.DESKWORKER)

    def acknowledgeOrder(self, order):
        """Change Order status to acknowledged"""

        order.setOrderStatus(OrderStatus.ACKNOWLEDGED)

    def acceptPayment(self, payment):
        pass

    def giveReceipt(self):
        pass

    def giveChange(self):
        pass

class EmployeeFactory(ABC):
    """Factory to create employees; main API"""

    @staticmethod
    def create(employee_type, **kwargs):
        """Create a specific Employee instance

        @param: name: string
              : The name of the employee
        @param: employee_type: EmployeeType Enum
              : The type of employee to create
        @param: **kwargs: dict
              : keyword arguments to provide; can be:
                - address: Address
                - email_addr: string
                - phone_num: string
                - pay: float
        @return: Employee
        """
        if employee_type == EmployeeType.ADMINISTRATOR:
            return Administrator(**kwargs)
        elif employee_type == EmployeeType.DRIVER:
            return DeliveryDriver(**kwargs)
        elif employee_type == EmployeeType.BAKER:
            return Baker(**kwargs)
        elif employee_type == EmployeeType.DESKWORKER:
            return DeskWorker(**kwargs)
        return None

class Address():
    """Model a real-life address"""

    def __init__(self, street, city, state, zip):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

class UserLogin():
    """Class to manage User logins"""

    _UPDATE_FIELDS = [
        "Username", "Password", "Status"
    ]

    def __init__(self, username, password, user_type):
        self._username = username
        self._password = password
        self._type = user_type

        self._login_status = False

    def __repr__(self):
        return (
            "\nUserLogin(\n"
            "   Username={0},\n"
            "   Password={1},\n"
            "   Type={2},\n"
            "   Status={3}\n"
            ")"
            .format(
                self._username, 
                self._password.replace(
                    self._password, "*" * len(self._password)),
                self._type, self._login_status))

    def __str__(self):
        return (
            "UserLogin({0}, {1}, {2}, {3})"
            .format(
                self._username, 
                self._password.replace(
                    self._password, "*" * len(self._password)),
                self._type, self._login_status))

    def getUsername(self):
        return self._username

    def getPassword(self):
        return self._password

    def getType(self):
        return self._type

    def getLoginStatus(self):
        return self._login_status

    def setLoginStatus(self, status):
        """Return self here so that we can chain"""
        self._login_status = status

        return self