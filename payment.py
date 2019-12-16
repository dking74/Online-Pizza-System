#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: To define payment options in project
# Patterns: Builder and Abstract Factory
#
#######################################################

from abc import ABC, abstractmethod
from enum import Enum

class PaymentType(Enum):
    """Enum for the types of payments valid"""
    CREDIT = 1
    DEBIT  = 2
    CASH   = 3
    CHECK  = 4

class PaymentLocation(Enum):
    """Enum for types of locations for payment"""
    STORE = 1
    ONLINE = 2

class PaymentInterface(ABC):
    @abstractmethod
    def setPaymentUser(self):
        pass

    @abstractmethod
    def setPaymentType(self):
        pass

    @abstractmethod
    def setPaymentLocation(self):
        pass

    @abstractmethod
    def setPaymentInformation(self):
        pass

class PaymentBuilder(PaymentInterface):
    """Builder to assist in creating payment"""
    def __init__(self):
        self._user = None
        self._type = None
        self._information = None
        self._location = None

    def setPaymentUser(self, customer):
        self._user = customer

        return self

    def setPaymentType(self, payment_type):
        # Set the type if it is an Enum value
        # and if the user has already been set.
        if isinstance(payment_type, PaymentType) and \
           self._user is not None:
            self._type = payment_type

        return self
    
    def setPaymentInformation(self, card_number, expiration_date, csv):
        """Only set payment information if type is debit or credit"""
        if self._type == PaymentType.DEBIT or self._type == PaymentType.CREDIT:
            self._information = {
                "Card Number": card_number,
                "Expiration Date": expiration_date,
                "CSV": csv
            }

        return self

    def setPaymentLocation(self, location):
        """Set where payment will take place,
        credit/debit, can be completed in either location.
        Check/cash can only be done in store.
        """
        # Kind of complicated here...We set the location
        # If the payment type has already been set.
        # If payment type is cash or check, we must pickup in store.
        if (
            isinstance(location, PaymentLocation) and
            (
                (
                  (self._type == PaymentType.CASH or self._type == PaymentType.CHECK) and
                  self._location == PaymentLocation.STORE
                ) or
                (self._type == PaymentType.CREDIT or self._type == PaymentType.DEBIT)
            )
        ):
            self._location = location

        return self

    def build(self):
        """Build the payment if it is valid. We return null if not valid"""
        if self._validPayment():

            return PaymentFactory.create(
                self._type,
                self._user,
                self._location,
                self._information
            )
        return None

    def _validPayment(self):
        """Valid payment is determined by following:
        - user, type, location has been set
        - if type is cash/credit, information has been provided

        @return bool
        """
        return (
            self._user is not None and
            self._type is not None and
            self._location is not None and 
            (
                (self._type == PaymentType.CASH or self._type == PaymentType.CHECK) or
                (
                    (self._type == PaymentType.DEBIT or self._type == PaymentType.CREDIT) and
                     self._information is not None
                )
            )
        )

class PaymentFactory(ABC):
    """Factory to create payments
    This is the main interface that should be used
    for payment creation.
    """

    @staticmethod
    def create(payment_type, user, location, information=None):
        """Factory method to return proper kinds of payment"""

        if (payment_type == PaymentType.CREDIT):
            return CreditPayment(user, location, information)
        elif (payment_type == PaymentType.DEBIT):
            return DebitPayment(user, location, information)
        elif (payment_type == PaymentType.CASH):
            return CashPayment(user)
        elif (payment_type == PaymentType.CHECK):
            return CheckPayment(user)
        raise Exception("Invalid payment type selected.")

class Payment():
    """Base class for payment"""

    _UPDATE_FIELDS = [
        "PaymentNumber",
        "UserName", "PaymentType", "PaymentLocation",
        "CardNumber", "ExpDate", "CSV"
    ]

    PAYMENT_NUM = 1

    def __init__(self, user_name, payment_type, payment_location, card_information=None, payment_num=None):
        self._user = user_name
        self._type = payment_type
        self._location = payment_location
        self._card_info = card_information or {}

        # Set the payment number either through constructor
        # or through set payment_num. We only want to increase
        # default payment number if one was not provided.
        self._payment_num = payment_num or Payment.PAYMENT_NUM
        if not payment_num:
            Payment.PAYMENT_NUM += 1

    def __repr__(self):
        return (
            "\nPayment(\n"
            "   Customer={0}\n"
            "   Type={1}\n"
            "   Location={2}\n"
            ")".format(self._user,
                self._type,
                self._location))

    def __str__(self):
        return (
            "\nPayment(\n"
            "   Customer={0}\n"
            "   Type={1}\n"
            "   Location={2}\n"
            ")".format(self._user,
                self._type,
                self._location))

    def pay(self):
        pass

    def getType(self):
        return self._type

    def getUserName(self):
        return self._user

    def getPaymentLocation(self):
        return self._location

    def getCardInfo(self):
        return self._card_info

    def getPaymentNumber(self):
        return self._payment_num

class CreditPayment(Payment):
    """Credit payment has card info associated"""
    def __init__(self, user_name, payment_location, card_information):
        Payment.__init__(self, user_name, payment_location, PaymentType.CREDIT, card_information)

    def pay(self, amount):
        pass

class DebitPayment(Payment):
    """Debit payment has card info associated"""
    def __init__(self, user_information, payment_location, card_information):
         Payment.__init__(self, user_information, payment_location, PaymentType.DEBIT, card_information)

    def pay(self, amount): 
        pass

class CashPayment(Payment):
    """Payment by cash to be done in store"""

    def __init__(self, user_information):
        Payment.__init__(self, user_information, PaymentType.CASH, PaymentLocation.STORE)

        self._user = user_information
        self._location = PaymentLocation.STORE
        self._card_info = None

    def pay(self, amount):
        return amount

class CheckPayment(Payment):
    """Payment by Check to be done in store"""
    def __init__(self, user_information):
        Payment.__init__(self, user_information, PaymentType.CHECK, PaymentLocation.STORE)

    def pay(self, amount):
        return 0