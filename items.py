#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: Create Items classes for items to buy
# Note: This was developed previously
#
#######################################################

from enum import Enum
from aenum import NoAlias, Enum as AdvancedEnum

class Item():
    """Base class for all purchaseable items at Pizza store"""

    _UPDATE_FIELDS = [
        "Name", "ItemType", "Description", "Price"
    ]

    def __init__(self, name, item_type, description, price):
        """Base class for all items

        @param: name: string
              : The name of the item
        @param: item_type: string (one of 'Pizza', 'Dessert', 'Breadstick', or 'Drink')
              : The grouping of item
        @param: description: string
              : The descriptive help of item
        @param: price: float
              : The price of item
        """
        self._name = name
        self._type = item_type
        self._price = price
        self._description = description

        self._num_purchased = 0

    def __str__(self):
        """String repr. of Item class"""

        return (
            "Item(\n"
            "   Name: {0}\n"
            "   Description: {1}\n"
            "   Price: {2}\n"
            ")"
        ).format(self._name, self._description, self._price)

    ################################################
    # Public methods for buying/removing Item
    ################################################
    def purchase(self, num_items=None):
        """Method to allow user to purchase item

        @param: num_items: int: optional
              : The number of specific item the user wishes
              : to purchase. If no value entered, default will be 1
    
        @return: The total cost items times num_items will cost user
        """

        num_items = self._checkNumItems(num_items)
        self._num_purchased += num_items

        return (self._price * num_items)

    def remove(self, num_items=None):
        """Method to allow user to remove from buying

        @param: num_items: int: optional
              : The number of specific item the user wishes
              : to remove. If no value entered, default will be 1
    
        @return: The total cost items times num_items will be awarded to user
        """

        # Make sure user has selected these items before removing
        num_items = self._checkNumItems(num_items)
        if (num_items <= self._num_purchased):
            self._num_purchased -= num_items

            return (self._price * num_items)

        return 0

    ################################################
    # Public setters for Name and Price and Description
    ################################################
    def setName(self, name):
        self._name = name

    def setPrice(self, new_price):
        self._price = new_price

    def setDescription(self, new_description):
        self._description = new_description

    ##############################################################
    # Public getters for Name,Price, Description, and NumPurchased
    ##############################################################
    def getName(self):
        return self._name

    def getItemType(self):
        return self._type

    def getPrice(self):
        return self._price

    def getDescription(self):
        return self._description

    def getNumPurchasedOrder(self):
        return self._num_purchased

    ################################################
    # Private methods internal to Item class
    ################################################
    def _checkNumItems(self, num_items):
        """Internal function to check the value of num_items
        If the value is None, return 1. Otherwise, return num_items.
        """

        if (num_items is None):
            return 1
        return num_items

class Drink(Item):
    """Drink class represents any kind of drink
    that a user can purchase from a Pizza store online
    """

    _UPDATE_FIELDS = ["Ounces"] + Item._UPDATE_FIELDS

    def __init__(self, drink_type, price, ounces, description=""):
        """Handle drinks to be bought

        @param: drink_type: DrinkType
              : The type of drink to purchase
        @param: price: float
              : The price of drink
        @param: ounces: float
              : The size of the drink
        @param: description: string
              : The description of the drink
        """

        Item.__init__(self, drink_type, 'Drink', description, price)

        self._ounces = ounces
        self._ounces_left = ounces
        self._drank = False

    def __repr__(self):
        return (
            "\nDrink(\n"
            "   Name={0}\n"
            "   Price={1}\n"
            "   Ounces={2}\n"
            "   Description={3}\n"
            ")".format(
                self.getName(),
                self.getPrice(),
                self.getOunces(),
                self.getDescription())
        )

    def __str__(self):
        return (
            "\nDrink(\n"
            "   Name={0}\n"
            "   Price={1}\n"
            "   Ounces={2}\n"
            "   Description={3}\n"
            ")".format(
                self.getName(),
                self.getPrice(),
                self.getOunces(),
                self.getDescription())
        )

    ################################################
    # Public methods that allow user to drink/refill drink
    ################################################
    def drink(self, ounces_drink=None):
        """Drink a certain amount of the drink

        @param: ounces_drink: int: optional
              : The amount to drink; If nothing
              : provided, drink all

        @return: None
        """

        # If the user does not enter a drink amount
        # make the drink empty. Otherwise, drink the amount
        # that is entered.
        if (ounces_drink is None):
            self._ounces_left = 0
        else:
            self._ounces_left -= ounces_drink
        
        # If the drink amount is less than/equal to 0,
        # set exactly to 0 and set drank to true.
        if (self._ounces_left <= 0):
            self._ounces_left = 0
            self._drank = True

    def refill(self, amount=None):
        """Method to refill the drink

        @param: amount: int: optional
              : The amount to refill in drink;
              : If nothing provided, refill to top
        
        @return: None
        """

        if (amount is not None) and \
             (amount + self._ounces_left <= self._ounces):
            self._ounces_left += amount
            self._ounces_left = self._ounces
        else:
            self._ounces_left = self._ounces

        self._drank = False

    def isDrank(self):
        """Determine if user has finished drink"""
        return self._drank

    def getOunces(self):
        return self._ounces

    def getDrinkType(self):
        """Get the type of drink being used"""
        return self.getName()

    def getOuncesLeft(self):
        """Get the number of ounces left in drink"""
        return self._ounces_left

class Breadstick(Item):
    """Breadstick class represents an order of breadsticks served
    by a Pizza store.
    """

    _UPDATE_FIELDS = ["Count", "Sauce"] + Item._UPDATE_FIELDS

    def __init__(self, bread_type, count, price, sauce=None, description=""):
        Item.__init__(self, bread_type, "Breadstick", description, price)

        self._stick_count = count
        self._sauce = sauce

    def __repr__(self):
        return ("\nBreadstick(name={0},"
                    "count={1}, "
                    "sauce={2}, "
                    "description={3})".format(
                        self._name,
                        self._stick_count,
                        str(self._sauce),
                        self._description))
    def __str__(self):
        return ("\nBreadstick(name={0},"
                    "count={1}, "
                    "sauce={2}, "
                    "description={3})".format(
                        self._name,
                        self._stick_count,
                        str(self._sauce),
                        self._description))

    def addBreadstick(self, num_sticks=None):
        """Add a breadstick to the stick count.
        If None, add 1. Otherwise, add user entered amount
        """

        if (num_sticks is None):
            self._stick_count += 1
        else:
            self._stick_count += num_sticks

    def eatBreadstick(self, num_sticks=None):
        """Eat a user entered amount of breadsticks"""

        if (num_sticks is None and self._stick_count > 0):
            self._stick_count -= 1
        elif (num_sticks is not None and num_sticks <= self._stick_count):
            self._stick_count -= num_sticks

    def getBreadstickCount(self):
        return self._stick_count

    def addSauce(self, sauce_type):
        """sauce_type must be of type 'Sauce'"""

        self._sauce = sauce_type

    def getSauce(self):
        return self._sauce

    def removeSauce(self):
        self._sauce = None

    def isSauceAdded(self):
        return (self._sauce is not None)

class Pizza(Item):
    """Pizza class represents a Pizza that a Pizza store can hold"""

    _UPDATE_FIELDS = [
        "Shape", "Crust", "State", "Toppings"
    ] + Item._UPDATE_FIELDS

    def __init__(self, pizza_type, price, shape=None, crust=None, state=None, additional_toppings=None, description=""):
        """Instantiate a pizza instance variable

        @param: pizza_type: string
              : The type of pizza as defined by PizzaType class
        @param: price: float
              : The base price of the pizza at defined
        @param: shape: PizzaShape
              : The shape that the pizza is in
        @param: crust: PizzaCrust
              : The style of the crust of pizza
        @param: state: PizzaState
              : The state of the pizza
        @param: additional_toppings: list
              : The additional toppings to place on pizza
        @param: description: string
              : The description of the pizza
        """

        Item.__init__(self, pizza_type, 'Pizza', description, price)

        self._shape = shape or PizzaShape.CIRCULAR
        self._crust = crust or PizzaCrust.THICK

        # This base price is so we can monitor what price is before other toppings
        self._base_price = price

        # Instance variables desribing state of pizza
        self._pizza_state = state or PizzaState.NONE

        # Set the additional toppings of pizza and make sure they are valid
        self._toppings = additional_toppings or []

        self._adjust_price()

    def __repr__(self):
            return (
                "\nPizza(\n"
                "   name={0}\n"
                "   description={1}\n"
                "   price={2}\n"
                "   shape={3}\n"
                "   crust={4}\n"
                "   state={5}\n"
                "   toppings={6}"
                ")".format(
                    self.getName(),
                    self.getDescription(),
                    self.getPrice(),
                    self.getShape(),
                    self.getCrust(),
                    self.getState(),
                    str(self.getToppings())))

    def __str__(self):
        return (
            "\nPizza(\n"
            "   name={0}\n"
            "   description={1}\n"
            "   price={2}\n"
            "   shape={3}\n"
            "   crust={4}\n"
            "   state={5}\n"
            "   toppings={6}"
            ")".format(
                self.getName(),
                self.getDescription(),
                self.getPrice(),
                self.getShape(),
                self.getCrust(),
                self.getState(),
                str(self.getToppings())))

    def getCrust(self):
        return self._crust

    def getShape(self):
        return self._shape

    def getState(self):
        return self._pizza_state

    def add_toppings(self, *toppings):
        """Go through each topping and add it to topping list"""
        for topping in toppings:
            self._checkValidTopping(topping)
            self._toppings.append(topping)

        self._adjust_price()

    def remove_toppings(self, *toppings):
        for topping in toppings:
            self._checkValidTopping(topping)
            if topping in self._toppings:
                self._toppings.remove(topping)

        self._adjust_price()

    def remove_all_toppings(self):
        self.remove_toppings(*self._toppings)

        self._adjust_price()

    def has_topping(self, topping):
        self._checkValidTopping(topping)

        return (topping in self._toppings)

    def getToppings(self):
        return self._toppings

    #####################################################
    # Public method functions to change state of pizza
    #####################################################
    def preparePizza(self):
        self._pizza_state = PizzaState.PREPARED

    def bakePizza(self):
        self._pizza_state = PizzaState.BAKED

    def cutPizza(self):
        self._pizza_state = PizzaState.CUT

    def boxPizza(self):
        self._pizza_state = PizzaState.BOXED

    #####################################################
    # Public method functions to determine state of pizza
    #####################################################
    def isPrepared(self):
        return (self._pizza_state == PizzaState.PREPARED)

    def isBaked(self):
        return (self._pizza_state == PizzaState.BAKED)
    
    def isCut(self):
        return (self._pizza_state == PizzaState.CUT)

    def isBoxed(self):
        return (self._pizza_state == PizzaState.BOXED)

    def isFinished(self):
        """Determine if the pizza has finished being processed"""
        return (
            self.isPrepared() and
            self.isBaked() and
            self.isCut() and
            self.isBoxed())

    def _adjust_price(self):
        """Internal method to adjust the price based on toppings"""

        # Go through each topping and add the money amount for topping
        topping_additional_money = 0
        for topping in self._toppings:
            topping_additional_money += topping.getPrice()

        self._price = self._base_price + topping_additional_money

    def _checkValidTopping(self, topping):
        """Internal method to validate that topping is correct"""

        if not isinstance(topping, Topping):
            raise Exception("The topping given is not a valid one. Please enter valid topping.")

class Topping():
    """Class to manage all pizza toppings"""

    _UPDATE_FIELDS = [
        "ToppingName", "ToppingPrice"
    ]

    def __init__(self, topping_name, topping_price):
        self._topping_name = topping_name
        self._topping_price = topping_price

    def __repr__(self):
        return (
            "Topping(name={0}, price={1})"
            .format(self._topping_name, self._topping_price)
        )

    def __str__(self):
        return (
            "Topping(name={0}, price={1})"
            .format(self._topping_name, self._topping_price)
        )

    def setName(self, new_name):
        self._topping_name = new_name

    def getName(self):
        return self._topping_name

    def setPrice(self, new_price):
        self._topping_price = new_price

    def getPrice(self):
        return self._topping_price

class PizzaState(Enum):
    NONE = 0
    PREPARED = 1
    BAKED = 2
    CUT = 3
    BOXED = 4

class PizzaShape(Enum):
    """Enum to manage pizza shapes"""

    CIRCULAR = 0
    SQUARE   = 1

class PizzaCrust(Enum):
    """Enum to manage Pizza crusts"""

    THIN          = 0
    FLATBREAD     = 1
    THICK         = 2
    CHICAGE_STYLE = 3