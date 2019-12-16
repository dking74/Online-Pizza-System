#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: To define managers for POS of pizza system
#        : This is the most important module in the project
#        : because it defines all the database manipulation
#        : and appropriate actions to take.
#
#######################################################

from abc import ABC, abstractmethod

from sqlalchemy.exc import *

from database import Database, DatabaseType
from menu import Menu
from users import Customer, Employee, UserLogin
from payment import Payment, PaymentType, PaymentLocation
from items import *
from orders import Order, OrderStatus

class Manager(ABC):
    """Interface for all manager classes"""

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def get(self):
        pass

    def getCustom(self, *columns, **filter):
        pass

class ManagerProxy(ABC):
    """Base class for Manager proxies that allows
    for setting a new employee so a new instance does
    not have to be created.
    """

    def setCurrentEmployee(self, employee):
        self._user = employee

    def isUserAdmin(self):
        """All proxies should be able to tell if current user is admin"""
        return self._user.isAdmin()

class MenuManager(Manager):
    """Manage all menus"""

    def __init__(self, database=None):
        """Initialize a database if needed and place instances of methods"""

        self.database = database or Database()

    def add(self, menu):
        """Add menu if it does not already exist"""
        self.database.execute(
            "INSERT INTO Menus (MenuName, Description) "
            "VALUES"
            "   ('{}', '{}')".format(menu.getMenuName(), menu.getDescription()))

    def edit(self, menu, menu_dict):
        """Edit specific menu with entered properties"""
        update_string_array = []
        for key, value in menu_dict.items():
            if key in menu._UPDATE_FIELDS:
                update_string = ("{} = '{}'".format(key, value))
                update_string_array.append(update_string)
        update_command = ",".join(update_string_array)

        # Now update all menus with properties set if current
        # command enterered by user is valid.
        if update_command:
            self.database.execute(
                "UPDATE Menus "
                "SET {0} "
                "WHERE MenuName='{1}' AND Description='{2}'"
                .format(update_command, menu.getMenuName(), menu.getDescription()))

    def remove(self, menu):
        """Remove specific menu from database"""
        self.database.execute(
            "DELETE FROM Menus "
            "WHERE MenuName='{0}' AND Description='{1}'"
            .format(menu.getMenuName(), menu.getDescription()))

    def get(self, menu):
        """Get the menu to see if already one available"""
        return self.database.execute(
            "SELECT * FROM Menus WHERE MenuName='{0}' AND Description='{1}'".format(
                    menu.getMenuName(), menu.getDescription()))

    def getCurrentMenus(self):
        """Get all the current menus, in oop form"""
        self._updateCurrentMenus()
        return self._current_menus

    def _updateCurrentMenus(self):
        """Keep track of the current menus in system"""
        results = self.database.execute("SELECT MenuName, Description FROM Menus")
        self._current_menus = [Menu(*row) for row in results]

class MenuManagerProxy(Manager, ManagerProxy):
    """Manage all menus with proxy in middle"""

    def __init__(self, user, menu_manager=None, database=None):
        """Create MenuManager that depends on specific user for access.
        @param: user: Employee
              : The user utilizing manager
        @param: menu_manager: MenuManager: optional
              : The menu manager responsible for database communication
        @param: database: Database: optional
              : The database to connect to

        @note: User can provide either menu_manager or database.
             : If menu_manager is provided, database wont matter.
             : If database is provided without manager, manager 
             : will be created with database as parameter.
        """
        self._user = user
        self._manager = menu_manager or MenuManager(database)
    
    def add(self, menu):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.add(menu)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def edit(self, menu, menu_dict):
        # If the user is an admin, call the manager edit function
        if (self.isUserAdmin()):
            self._manager.edit(menu, menu_dict)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def remove(self, menu):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.remove(menu)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def get(self, menu):
        return self._manager.get(menu)

    def getCurrentMenus(self):
        return self._manager.getCurrentMenus()

class EmployeeManager(Manager):
    """Manage all employees"""

    def __init__(self, database=None):
        """Initialize a database if needed and place instances of methods"""

        self.database = database or Database()

    def add(self, employee):
        """Add employee if it does not already exist"""
        self.database.execute(
            "INSERT INTO Employees ("
            "   FirstName, LastName, PhoneNumber, EmailAddress, Pay, EmployeeType"
            ") VALUES "
            " ('{0}','{1}','{2}','{3}','{4}','{5}')".format(
                employee.getFirstName(), employee.getLastName(),
                employee.getPhoneNumber(), employee.getEmailAddress(),
                employee.getPay(), employee.getEmployeeType()
            ))

    def edit(self, employee, employee_dict):
        """Edit specific employee with entered properties"""
        update_string_array = []
        for key, value in employee_dict.items():
            if key in employee._UPDATE_FIELDS:
                update_string = ("{} = '{}'".format(key, value))
                update_string_array.append(update_string)
        update_command = ",".join(update_string_array)

        # Now update all menus with properties set if current
        # command enterered by user is valid.
        if update_command:
            self.database.execute(
                "UPDATE Employees "
                "SET {0} "
                "WHERE FirstName='{1}' AND LastName='{2}' "
                .format(update_command,
                    employee.getFirstName(),
                    employee.getLastName()))

    def remove(self, employee):
        """Remove specific menu from database"""
        self.database.execute(
            "DELETE FROM Employees "
            "WHERE FirstName='{0}' AND LastName='{1}' "
            .format(employee.getFirstName(),
                    employee.getLastName()))

    def get(self, employee):
        """Get the menu to see if already one available"""
        return self.database.execute(
            "SELECT * FROM Employees WHERE FirstName='{1}' AND LastName='{2}' "
            .format(employee.getFirstName(),
                    employee.getLastName()))

    def getCurrentEmployees(self):
        """Get all the current employees, in oop form"""
        self.__updateCurrentEmployees()
        return self._current_employees

    def _updateCurrentEmployees(self):
        """Keep track of the current employees in system"""
        results = self.database.execute(
            "SELECT FirstName, LastName "
            "FROM Employees")
        self._current_employees = [Employee(*row) for row in results]

class EmployeeManagerProxy(Manager, ManagerProxy):
    """Manage all employees with proxy in middle"""

    def __init__(self, user, employee_manager=None, database=None):
        self._user = user
        self._manager = employee_manager or EmployeeManager(database)
    
    def add(self, employee):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.add(employee)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def edit(self, employee, employee_dict):
        # If the user is an admin, call the manager edit function
        if (self.isUserAdmin()):
            self._manager.edit(employee, employee_dict)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def remove(self, employee):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.remove(employee)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def get(self, employee):
        if (self.isUserAdmin()):
            return self._manager.get(employee)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def getCurrentEmployees(self):
        if (self.isUserAdmin()):
            return self._manager.getCurrentEmployees()
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

class LoginManager(Manager):
    """Manage all menus"""

    def __init__(self, database=None):
        """Initialize a database if needed and place instances of methods"""

        self.database = database or Database()

    def add(self, userlogin, id):
        """Add userlogin if it does not already exist"""

        self.database.execute(
            "INSERT INTO UserLogin ("
            "   Username, Password, UserType, Status, {0}"
            ") VALUES"
            "   ('{1}','{2}','{3}',0,{4})".format(
                'EmployeeId' if (userlogin.getType() == 'Employee') else 'CustomerId',
                userlogin.getUsername(), 
                userlogin.getPassword(),
                userlogin.getType(),
                id))

    def edit(self, userlogin, login_dict):
        """Edit specific menu with entered properties"""

        update_string_array = []
        for key, value in login_dict.items():
            if key in userlogin._UPDATE_FIELDS:
                update_string = ("{} = '{}'".format(key, value))
                update_string_array.append(update_string)
        update_command = ",".join(update_string_array)

        # Now update all userlogins with properties set if current
        # command enterered by user is valid.
        if update_command:
            self.database.execute(
                "UPDATE UserLogin "
                "SET {0} "
                "WHERE Username='{1}'"
                .format(update_command, 
                    userlogin.getUsername()))

    def remove(self, userlogin):
        """Remove specific userlogin from database"""

        self.database.execute(
            "DELETE FROM UserLogin "
            "WHERE Username='{0}'"
            .format(userlogin.getUsername()))

    def getCustomer(self, userlogin):
        return self.database.execute(
            "SELECT c.FirstName, c.LastName, c.PhoneNumber, "
            "c.EmailAddress "
            "FROM UserLogin u "
            "LEFT JOIN Customers c "
            "ON u.CustomerId=c.CustomerId "
            "WHERE u.Username='{0}'".format(
                userlogin.getUsername()))

    def getEmployee(self, userlogin):
        return self.database.execute(
            "SELECT e.FirstName, e.LastName, e.PhoneNumber, "
            "e.EmailAddress, e.Pay, e.EmployeeType "
            "FROM UserLogin u "
            "INNER JOIN Employees e "
            "ON u.EmployeeId=e.EmployeeId "
            "WHERE u.Username='{0}'".format(
                    userlogin.getUsername()))

    def get(self, userlogin):
        """Get the userlogin to see if already one available"""

        return self.database.execute(
            "SELECT * "
            "FROM UserLogin t "
            "LEFT JOIN Employees e "
            "ON t.EmployeeId=e.EmployeeId "
            "LEFT JOIN Customers c "
            "ON t.CustomerId=c.CustomerId "
            "WHERE t.Username='{0}'".format(
                    userlogin.getUsername()))

    def getCurrentLogins(self):
        """Get all the current menus, in oop form"""
        self._updateCurrentLogins()
        return self._current_logins

    def _updateCurrentLogins(self):
        """Keep track of the current menus in system"""

        results = self.database.execute(
            "SELECT Username, Password, UserType, Status "
            "FROM UserLogin WHERE Status=1")

        # Get the current logins
        self._current_logins = []
        if results is not None:
            self._current_logins = [
                UserLogin(row[0], row[1], row[2])
                .setLoginStatus(row[3])
                for row in results]

class LoginManagerProxy(Manager, ManagerProxy):
    """Manage all menus with proxy in middle"""

    def __init__(self, user, login_manager=None, database=None):
        self._user = user
        self._manager = login_manager or LoginManager(database)
    
    def add(self, userlogin, id):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.add(userlogin, id)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def edit(self, userlogin, login_dict):
        # If the user is an admin, call the manager edit function
        if (self.isUserAdmin()):
            self._manager.edit(userlogin, login_dict)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def remove(self, userlogin):
        # If the user is an admin, call the userlogin add function
        if (self.isUserAdmin()):
            self._manager.remove(userlogin)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def getEmployee(self, userlogin):
        return self._manager.getEmployee(userlogin)

    def getCustomer(self, userlogin):
        return self._manager.getCustomer(userlogin)

    def get(self, userlogin):
        return self._manager.get(userlogin)

    def getCurrentLogins(self):
        if (self.isUserAdmin()):
            return self._manager.getCurrentLogins()
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

class CustomerManager(Manager):
    """Manage all customers"""

    def __init__(self, database=None):
        """Initialize a database if needed and place instances of methods"""

        self.database = database or Database()

    def add(self, customer):
        """Add customer if it does not already exist"""

        result = self.database.execute(
            "INSERT INTO Customers ("
            "   FirstName, LastName, PhoneNumber, EmailAddress"
            ") VALUES "
            " ('{0}','{1}','{2}','{3}')".format(
                customer.getFirstName(), customer.getLastName(),
                customer.getPhoneNumber(), customer.getEmailAddress()
            ))

        try:
            id = self.get(customer)[0][0]
        except Exception as e:
            id = None
        return id

    def edit(self, customer, customer_dict):
        """Edit specific employee with entered properties"""
        update_string_array = []
        for key, value in customer_dict.items():
            if key in customer._UPDATE_FIELDS:
                update_string = ("{} = '{}'".format(key, value))
                update_string_array.append(update_string)
        update_command = ",".join(update_string_array)

        # Now update all menus with properties set if current
        # command enterered by user is valid.
        if update_command:
            self.database.execute(
                "UPDATE Customers "
                "SET {0} "
                "WHERE FirstName='{1}' AND LastName='{2}'"
                "AND EmailAddress='{3}'"
                .format(update_command,
                    customer.getFirstName(),
                    customer.getLastName(),
                    customer.getEmailAddress()))

    def remove(self, customer):
        """Remove specific customer from database"""
        self.database.execute(
            "DELETE FROM Customers "
            "WHERE FirstName='{0}' AND LastName='{1}'"
            "AND EmailAddress='{2}'"
            .format(customer.getFirstName(),
                    customer.getLastName(),
                    customer.getEmailAddress()))

    def get(self, customer):
        """Get the customer to see if already one available"""
        
        return self.database.execute(
            "SELECT * FROM Customers "
            "WHERE FirstName='{0}' AND LastName='{1}' AND EmailAddress='{2}'"
            .format(customer.getFirstName(),
                    customer.getLastName(),
                    customer.getEmailAddress()))

    def getCurrentCustomers(self):
        """Get all the current customers, in oop form"""
        self._updateCurrentCustomers()
        return self._current_customers

    def _updateCurrentCustomers(self):
        """Keep track of the current employees in system"""
        results = self.database.execute(
            "SELECT FirstName, LastName, PhoneNumber, EmailAddress "
            "FROM Customers")
        self._current_customers = [Customer(*row) for row in results]

class CustomerManagerProxy(Manager, ManagerProxy):
    """Manage all customers with proxy in middle"""

    def __init__(self, user, customer_manager=None, database=None):
        self._user = user
        self._manager = customer_manager or CustomerManager(database)
    
    def add(self, customer):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.add(customer)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def edit(self, customer, customer_dict):
        # If the user is an admin, call the manager edit function
        if (self.isUserAdmin()):
            self._manager.edit(customer, customer_dict)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def remove(self, customer):
        # If the user is an admin, call the customer add function
        if (self.isUserAdmin()):
            self._manager.remove(customer)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def get(self, customer):
        if (self.isUserAdmin()):
            return self._manager.get(customer)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def getCurrentCustomers(self):
        if (self.isUserAdmin()):
            return self._manager.getCurrentCustomers()
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

class OrderManager(Manager):
    """Manage all orders"""

    def __init__(self, database=None):
        """Initialize a database if needed and place instances of methods"""

        self.database = database or Database()

    def add(self, order):
        """Add order if it does not already exist"""

        # Submit order internally and then to database
        order.submit()

        payment_id = self._addPayment(order.getPayment())
        unique_order = self.database.execute(
            "INSERT INTO Orders ("
            "   OrderNumber, Status, "
            "   CustomerName, CustomerEmail, "
            "   PaymentId"
            ") VALUES"
            "   ({0},{1},'{2}','{3}',{4})".format(
                order.getOrderNumber(),
                order.getOrderStatus().value,
                order.getCustomerName(),
                order.getCustomerEmail(),
                payment_id))

        # Add entries for order -> item linking table
        # Only do this if a unique order was created.
        if not isinstance(unique_order, IntegrityError):
            self._addOrderItems(order)

    def _addPayment(self, payment):
        """Internal function to add the payment to database"""

        card_info = payment.getCardInfo()
        self.database.execute(
            "INSERT INTO Payments ("
            "   PaymentNumber, UserName, PaymentType,"
            "   PaymentLocation, CardNumber, ExpDate, CSV"
            ") VALUES "
            "   ({0},'{1}',{2},{3},'{4}','{5}',{6})"
            .format(
                payment.getPaymentNumber(),
                payment.getUserName(),
                payment.getType().value,
                payment.getPaymentLocation().value,
                card_info.get("Card Number", "NULL"),
                card_info.get("Expiration Date", "NULL"),
                card_info.get("CSV", "NULL")))

        return self._getPaymentId(payment)

    def _addOrderItems(self, order):
        """Internal function to map order id
        to item ids in database
        """

        # Get the items associated with the order and their
        # respective ids in the database.
        items = order.getItems()
        query_string = " OR ".join([
            "(Name='" + item.getName() +"')" \
            for item in items
        ])
        item_ids = self.database.execute(
            "SELECT ItemId "
            "FROM Items "
            "WHERE {0}".format(query_string))

        # Get the order id that we are currently working on
        order_id = self.database.execute(
            "SELECT OrderId "
            "FROM Orders "
            "WHERE OrderNumber={0}".format(order.getOrderNumber()))

        # Add the orderid/itemid combo to database
        for item in item_ids:
            execution = self.database.execute(
                "INSERT INTO OrderItems ("
                "   OrderId, ItemId "
                ") VALUES "
                "    ({0},{1})".format(order_id[0][0], item[0]))   

    def _getPayment(self, order):
        """Internal function to get the payment id
        after the order has been submitted.
        """

        try:
            return self.database.execute(
                "SELECT CustomerId, PaymentId "
                "FROM Orders "
                "WHERE OrderNumber={0}"
                .format(
                    order.getOrderNumber()))[0]
        except:
            return (None, None)

    def _getPaymentId(self, payment):
        """Internal function to get the payment id
        after the payment has been put in database
        but order has not been submitted yet
        """

        try:
            return self.database.execute(
                "SELECT PaymentId "
                "FROM Payments "
                "WHERE PaymentNumber={0}"
                .format(payment.getPaymentNumber()))[0][0]
        except:
            return None

    def edit(self, order, order_dict):
        """Edit specific order with entered properties"""

        update_string_array = []
        for key, value in order_dict.items():
            if key in order._UPDATE_FIELDS:
                update_string = ("{} = '{}'".format(key, value))
                update_string_array.append(update_string)
        update_command = ",".join(update_string_array)

        # Now update all orders with properties set if current
        # command enterered by user is valid.
        if update_command:
            self.database.execute(
                "UPDATE Order "
                "SET {0} "
                "WHERE Username='{1}'"
                .format(update_command, 
                    order.getUsername()))

    def remove(self, order):
        """Remove specific userlogin from database"""

        self.database.execute(
            "DELETE FROM Orders o "
            "INNER JOIN Customer c "
            "ON o.CustomerId=c.CustomerId "
            "WHERE c.FirstName='{0}' AND c.LastName='{1}'"
            .format(
                order.getCustomer().getFirstName(),
                order.getCustomer().getLastName()))

    def get(self, order):
        """Get the order to see if already one available"""

        return self.database.execute(
            "SELECT o.OrderStatus, "
            "".format())

    def getCurrentOrders(self):
        """Get all the current orders, in oop form"""
        self._updateCurrentOrders()
        return self._current_orders

    def _updateCurrentOrders(self):
        """Keep track of the current menus in system"""

        base_orders = self.database.execute(
            "SELECT o.OrderId, o.OrderNumber, o.CustomerName, o.CustomerEmail, o.Status, "
            "p.PaymentNumber, p.UserName, p.PaymentType, p.PaymentLocation, "
            "p.CardNumber, p.ExpDate, p.CSV "
            "FROM Orders o "
            "LEFT JOIN Payments p "
            "ON o.PaymentId=p.PaymentId "
            "WHERE o.Status < 5")

        orders = []
        for order in base_orders:
            items = self.database.execute(
                "SELECT "
                "   i.Name, i.ItemType, i.Description, i.Price, "
                "   p.Crust, p.Shape, p.State, "
                "   d.Ounces, "
                "   b.Count, b.Sauce "
                "FROM Items i "
                "LEFT JOIN Pizzas p ON i.ItemId=p.ItemId "
                "LEFT JOIN Drinks d ON i.ItemId=d.ItemId "
                "LEFT JOIN Breadsticks b ON i.ItemId=b.ItemId "
                "INNER JOIN OrderItems oi ON i.ItemId=oi.ItemId "
                "INNER JOIN Orders o ON oi.OrderId=o.OrderId "
                "WHERE o.OrderId={0}".format(order[0]))

            new_items = []
            for item in items:
                if item[1] == "Pizza":
                    new_item = Pizza(
                        item[0], item[3],
                        shape=PizzaShape(item[5]),
                        crust=PizzaCrust(item[4]),
                        state=PizzaState(item[6]),
                        description=item[2])
                elif item[1] == "Drink":
                    new_item = Drink(
                        item[0], item[3],
                        item[7], description=item[2])
                else:
                    new_item = Breadstick(
                        item[0], item[8], item[3],
                        sauce=item[9],
                        description=item[2])
                new_items.append(new_item)

            # Add the order to master list
            orders.append(
                Order(
                    customer_name=order[2],
                    customer_email=order[3],
                    order_num=order[1],
                    payment=Payment(
                        order[6],
                        PaymentType(order[7]),
                        PaymentLocation(order[8]),
                        card_information=({
                            "Card Number": order[9],
                            "Expiration Date": order[10],
                            "CSV": order[11]
                        } if order[11] else None),
                        payment_num=order[5]),
                    items=new_items,
                    order_status=OrderStatus(order[4])))

        self._current_orders = orders

class OrderManagerProxy(Manager, ManagerProxy):
    """Manage all menus with proxy in middle"""

    def __init__(self, user, order_manager=None, database=None):
        self._user = user
        self._manager = order_manager or OrderManager(database)
    
    def add(self, order):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.add(order, id)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def edit(self, order, order_dict):
        # If the user is an admin, call the manager edit function
        if (self.isUserAdmin()):
            self._manager.edit(order, order_dict)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def remove(self, order):
        # If the user is an admin, call the order add function
        if (self.isUserAdmin()):
            self._manager.remove(order)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def get(self, order):
        return self._manager.get(order)

    def getCurrentOrders(self):
        return self._manager.getCurrentOrders()

class PaymentManager(Manager):
    """Manage all payments"""

    def __init__(self, database=None):
        """Initialize a database if needed and place instances of methods"""

        self.database = database or Database()

    def add(self, payment):
        """Add payment if it does not already exist"""

        card_payment = payment.getCardInfo()
        if card_payment is not None:
            self.database.execute(
                "INSERT INTO Payments ("
                "   UserName, PaymentType, PaymentLocation, CardNumber, "
                "   ExpDate, CSV "
                ") VALUES"
                "   ('{0}',{1},{2},'{3}','{4}',{5})".format(
                    payment.getUserName(),
                    payment.getType().value,
                    payment.getPaymentLocation(),
                    card_payment["Card Number"],
                    card_payment["Expiration Date"],
                    card_payment["CSV"]))
        else:
            self.database.execute(
                "INSERT INTO Payments ("
                "   UserName, PaymentType, PaymentLocation "
                ") VALUES"
                "   ('{0}',{1},{2})".format(
                    payment.getUserName(),
                    payment.getType().value,
                    payment.getPaymentLocation()))

    def edit(self, payment, payment_dict):
        """Edit specific order with entered properties.
        Payment should not be edited without help from customer.
        """

        update_string_array = []
        for key, value in payment_dict.items():
            if key in payment._UPDATE_FIELDS:
                update_string = ("{} = '{}'".format(key, value))
                update_string_array.append(update_string)
        update_command = ",".join(update_string_array)

        # Now update all payments with properties set if current
        # command enterered by user is valid.
        if update_command:
            self.database.execute(
                "UPDATE Payments "
                "SET {0} "
                "WHERE UserName='{1}' AND PaymentLocation={2}"
                .format(update_command, 
                    payment.getUserName(),
                    payment.getPaymentLocation()))

    def remove(self, payment):
        """Remove specific payment from database"""

        self.database.execute(
            "DELETE FROM Payments p "
            "WHERE p.UserName='{0}' AND p.PaymentLocation={1}"
            .format(
                payment.getUserName(),
                payment.getPaymentLocation()))

    def get(self, payment):
        """Get the payment to see if already one available"""

        return self.database.execute(
            "SELECT *"
            "FROM Payments p "
            "WHERE p.UserName='{0}' AND p.PaymentType='{1}' "
            .format(
                payment.getUserName(),
                payment.getPaymentType()))

    def getCurrentPayments(self):
        """Get all the current payments, in oop form"""
        self._updateCurrentPayments()
        return self._current_payments

    def _updateCurrentPayments(self):
        """Keep track of the current payments in system"""

        results = self.database.execute(
            "SELECT UserName, PaymentType, "
            "PaymentLocation ,CardNumber, ExpDate, CSV "
            "FROM Payments")
        
        self._current_payments = [Payment(*row) for row in results]

class PaymentManagerProxy(Manager, ManagerProxy):
    """Manage all payments with proxy in middle"""

    def __init__(self, user, payment_manager=None, database=None):
        self._user = user
        self._manager = payment_manager or PaymentManager(database)
    
    def add(self, payment):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.add(payment)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def edit(self, payment, payment_dict):
        # If the user is an admin, call the manager edit function
        if (self.isUserAdmin()):
            self._manager.edit(payment, payment_dict)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def remove(self, payment):
        # If the user is an admin, call the payment add function
        if (self.isUserAdmin()):
            self._manager.remove(payment)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def get(self, payment):
        if (self.isUserAdmin()):
            return self._manager.get(payment)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def getCurrentPayments(self):
        if (self.isUserAdmin()):
            return self._manager.getCurrentPayments()
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

class ItemManager(Manager):
    """Manage all items"""

    def __init__(self, database=None):
        """Initialize a database if needed and place instances of methods"""

        self.database = database or Database()

    def add(self, item):
        """Add item if it does not already exist"""

        # Make sure that the item is a derived type,
        # rather than base type so that item can be
        # properly placed into database.
        if not isinstance(item, Pizza) and \
              not isinstance(item, Breadstick) and \
              not isinstance(item, Drink):
            return

        # The generic item information needs to be
        # added into database first. Then, specific
        # item type comes second.
        executed = self.database.execute(
            "INSERT INTO Items ("
            "   Name, ItemType, Description, Price"
            ") VALUES"
            "   ('{0}','{1}','{2}',{3})".format(
                item.getName(), item.getItemType(), 
                item.getDescription(), item.getPrice()))

        # If an IntegrityError is raised, that means we
        # were unable to create due to UNIQUE constraints.
        # If executed isnt this, add the item in other tables.
        if not isinstance(executed, IntegrityError):
            # We created a new item and need to retrieve id now
            new_item_id = self.getItemId(item)[0][0]
            database_string = self._getItemTableString(item, new_item_id)
            item_table = self.database.execute(database_string)

            if (item.getItemType() == "Pizza"):
                pizza_id = self.database.execute(
                    "SELECT p.PizzaId "
                    "FROM Pizzas p "
                    "INNER JOIN Items i "
                    "ON p.ItemId = i.ItemId "
                    "WHERE i.Name='{0}' AND i.Description='{1}' "
                    "AND i.Price={2}".format(
                       item.getName(), item.getDescription(),
                       item.getPrice()))[0][0]

                # If we found the pizza, add toppings.
                for topping in item.getToppings():
                    topping_id = self.database.execute(
                        "SELECT ToppingId "
                        "FROM Toppings "
                        "WHERE ToppingName='{0}' AND ToppingPrice={1}"
                        .format(
                            topping.getName(),
                            topping.getPrice()))[0][0]
                    self.database.execute(
                        "INSERT INTO PizzaToppings ("
                        "   PizzaId, ToppingId "
                        ") VALUES "
                        "   ({0},{1})".format(
                            pizza_id, topping_id))
            return new_item_id

    def edit(self, item, item_dict):
        """Edit specific order with entered properties"""

        update_string_array = []
        for key, value in item_dict.items():
            if key in item._UPDATE_FIELDS:
                update_string = ("{} = '{}'".format(key, value))
                update_string_array.append(update_string)
        update_command = ",".join(update_string_array)

        # Now update all orders with properties set if current
        # command enterered by user is valid.
        if update_command:
            self.database.execute(
                "UPDATE Order "
                "SET {0} "
                "WHERE Username='{1}'"
                .format(update_command, 
                    item.getName()))

    def remove(self, item):
        """Remove specific item from database"""

        # Due to foreign key constraint, remove 
        # base item to remove all associated entries.
        self.database.execute(
            "DELETE FROM Items "
            "WHERE Name='{0}'"
            .format(
                item.getName()))

    def _getItemTableString(self, item, item_id):
        """Internal function to determine where
        the sub-item should go into.

        Returns the proper insert string.
        """

        if (item.getItemType() == "Pizza"):
            return (
                "INSERT INTO Pizzas ("
                "   ItemId, Crust, Shape"
                ") VALUES "
                "   ({0},{1},{2})".format(
                    item_id, item.getCrust().value, item.getShape().value)
            )
        elif (item.getItemType() == "Breadstick"):
            return (
                "INSERT INTO Breadsticks ("
                "   ItemId, Count, Sauce"
                ") VALUES "
                "   ({0},{1},{2})".format(
                    item_id, item.getBreadstickCount(),
                    item.getSauce() or "NULL")
            )
        else:
            return (
                "INSERT INTO Drinks ("
                "   ItemId, Ounces"
                ") VALUES "
                "   ({0},{1})"
                .format(
                    item_id, item.getOunces())
            )

    def getItemId(self, item):
        """Get the specific item by id"""

        return self.database.execute(
            "SELECT ItemId "
            "FROM Items "
            "WHERE Name='{0}' AND ItemType='{1}' AND "
            "Description='{2}' AND Price={3}"
            .format(
                item.getName(), item.getItemType(),
                item.getDescription(), item.getPrice()))

    def get(self, item):
        """Get the item to see if already one available"""

        # Hacky way of doing this, but the type is one
        # of: Pizza, Breadstick, or Drink. The table names
        # are the item plus an 's'.
        return self.database.execute(
            "SELECT * "
            "FROM Items i "
            "INNER JOIN {0} t "
            "ON i.ItemId=t.ItemId "
            "WHERE i.Name='{1}'".format(
                item.getItemType() + "s", 
                item.getName()))

    def getCurrentItems(self):
        """Get all the current items, in oop form"""
        
        return self._updateCurrentItems()

    def _updateCurrentItems(self):
        """Keep track of the current items in system"""

        results = self.database.execute(
            "SELECT i.Name, i.ItemType, i.Description, i.Price, "
            "p.Crust, p.Shape, p.State, p.PizzaId, "
            "d.Ounces, "
            "b.Count, b.Sauce "
            "FROM Items i "
            "LEFT JOIN Pizzas p "
            "ON i.ItemId=p.ItemId "
            "LEFT JOIN Drinks d "
            "ON i.ItemId=d.ItemId "
            "LEFT JOIN Breadsticks b "
            "ON i.ItemId=b.ItemId")

        # Go through each result, determine type, and add to items list
        items = []
        for row in results:
            item_type = row[1]

            if (item_type == "Pizza"):
                item = Pizza(
                        row[0], row[3],
                        crust=PizzaCrust(row[4]), shape=PizzaShape(row[5]),
                        state=PizzaState(row[6]), description=row[2])

                toppings = self.database.execute(
                   "SELECT t.ToppingName, t.ToppingPrice "
                   "FROM Toppings t "
                   "INNER JOIN PizzaToppings pt "
                   "ON t.ToppingId=pt.ToppingId "
                   "WHERE pt.PizzaId={0}".format(row[7]))

                # Add each topping found into the item created
                for topping in toppings:
                    item.add_toppings(Topping(*topping))
            elif (item_type == "Drink"):
                item = Drink(row[0], row[3], row[8], description=row[2])
            else:
                item = Breadstick(row[0], row[9], row[3],
                            sauce=row[10], description=row[2])
            items.append(item)

        return items

class ItemManagerProxy(Manager, ManagerProxy):
    """Manage all menus with proxy in middle"""

    def __init__(self, user, item_manager=None, database=None):
        self._user = user
        self._manager = item_manager or ItemManager(database)
    
    def add(self, item):
        # If the user is an admin, call the manager add function
        if (self.isUserAdmin()):
            self._manager.add(item)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def edit(self, item, item_dict):
        # If the user is an admin, call the manager edit function
        if (self.isUserAdmin()):
            self._manager.edit(item, item_dict)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def remove(self, item):
        # If the user is an admin, call the order add function
        if (self.isUserAdmin()):
            self._manager.remove(item)
        else:
            raise Exception("Employee ('{0}') does not have access!".format(self._user.getFullName()))

    def get(self, item):
        return self._manager.get(item)

    def getCurrentItems(self):
        return self._manager.getCurrentItems()