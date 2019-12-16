#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: To define orders interactions in system
# Pattern: Builder on Order to assist creating complex object
#
#######################################################

from enum import Enum
from abc import ABC, abstractmethod

class OrderStatus(Enum):
    NOT_SUBMITTED = 0
    PENDING       = 1
    SUBMITTED     = 2
    ACKNOWLEDGED  = 3
    PREPARING     = 4
    COMPLETED     = 5
    READY         = 6
    ONITSWAY      = 7

class ShoppingCart():
    """Class to manage items in cart"""
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def remove(self, item):
        self._items.remove(item)

    def emptyCart(self):
        self._items = []

    def getCart(self):
        return self._items

class OBuilder(ABC):
    """OBuilder is interface to assist in creating of Orders"""

    @abstractmethod
    def setCustomer(self):
        pass

    @abstractmethod
    def setPayment(self):
        pass

    @abstractmethod
    def setItems(self):
        pass

class OrderBuilder(OBuilder):
    """OrderBuilder instance gets created before Order.
    This class helps build an Order easily.
    """

    def __init__(self):
        self._customer_name = ""
        self._customer_email = ""
        self._payment = None
        self._items = []

    def setCustomer(self, customer_name, customer_email):
        self._customer_name = customer_name
        self._customer_email = customer_email

        return self

    def setPayment(self, payment):
        self._payment = payment

        return self

    def setItems(self, cart):
        """Cart is a ShoppingCart this is being utilized"""
        self._items = cart.getCart().copy()

        return self

    def build(self):
        """Build is a simple API to create Order for you"""

        if not self._customer_name or not self._customer_email:
            raise Exception("Please call 'setCustomer' first before building.")
        if not self._payment:
            raise Exception("Please call 'setPayment' first before building.")
        if not self._items:
            raise Exception("Please call 'setItems' first before building.")

        return Order(
                self._customer_name,
                self._customer_email,
                self._payment, self._items)

class Order():
    _UPDATE_FIELDS = [
        "OrderNumber", "OrderStatus",
        "Customer", "Payment"
    ]

    ORDER_NUM = 1

    def __init__(self, customer_name=None, customer_email=None, payment=None, items=None, order_status=None, order_num=None):
        """Initialize an Order instance

        @param: customer_name: string: optional
              : The customer placing order
        @param: customer_email: string: options
              : The email address of customer
        @param: payment: Payment: optionl
              : The payment to be used with order
        """
        self._customer_name = customer_name
        self._customer_email = customer_email
        self._payment  = payment
        self._items    = items or []

        self._status = order_status or OrderStatus.NOT_SUBMITTED
        self._subtotal = 0

        # Set the initial total with toppings
        self._setTotal()

        # The order needs a number associated when created.
        # If user does not provide it, put it at Order.OrderNum
        self._order_number = order_num or Order.ORDER_NUM

    def __repr__(self):
        return (
            "\nOrder(\n"
            "   OrderNum={0},\n"
            "   CustomerName={1},\n"
            "   CustomerEmail={2}\n"
            "   Payment={3},\n"
            "   Items={4},\n"
            "   Status={5},\n"
            "   Total={6}\n"
            ")".format(
                self._order_number,
                self._customer_name,
                self._customer_email,
                self._payment,
                self._items,
                self._status,
                self._subtotal
            ))

    def __str__(self):
        return (
            "\nOrder(\n"
            "   OrderNum={0},\n"
            "   CustomerName={1},\n"
            "   CustomerEmail={2}\n"
            "   Payment={3},\n"
            "   Items={4},\n"
            "   Status={5},\n"
            "   Total={6}\n"
            ")".format(
                self._order_number,
                self._customer_name,
                self._customer_email,
                self._payment,
                self._items,
                self._status,
                self._subtotal
            ))

    #################################################
    # Public getters for:
    #   Customer, Payment, Items, NumItems,
    #   OrderStatus, Cost
    #################################################
    def getCustomerName(self):
        return self._customer_name

    def getCustomerEmail(self):
        return self._customer_email

    def getPayment(self):
        return self._payment

    def getItems(self):
        return self._items

    def getNumItems(self):
        return len(self._items)

    def getOrderStatus(self):
        return self._status

    def getSubtotal(self):
        return self._subtotal

    def getOrderNumber(self):
        return self._order_number

    #################################################
    # Public setters for: Customer and Payment and Status
    #################################################
    def setCustomerName(self, customer_name):
        self._customer_name = customer_name

    def setCustomerEmail(self, customer_email):
        self._customer_email = customer_email

    def setPayment(self, payment):
        self._payment = payment

    def setOrderStatus(self, status):
        """Change the order status for updates"""
        if isinstance(status, OrderStatus):
            self._status = status

    #################################################
    # Public API methods
    #################################################
    def addItem(self, item):
        self._items.add(item)

    def addItems(self, *items):
        for item in items:
            self.addItem(item)

    def _setTotal(self):
        """Go through items and set the total of order"""

        subtotal = 0

        cart = self._items
        for item in cart:
            subtotal += item.purchase()

        self._subtotal = subtotal

        return self

    def submit(self):
        """Submit the order to inject into sales system
        and return the order number created.
        """

        # Set what the total of the purchase is
        # and the status of the order.
        self._setTotal()
        self.setOrderStatus(OrderStatus.SUBMITTED)

        Order.ORDER_NUM += 1

        return self._order_number
