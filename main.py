#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: This is the main entry point of the test application
#
#######################################################

from application import *
from database import *
from items import *
from payment import Payment, PaymentType, PaymentLocation

def main():
    """Enter into testing the application"""
    
    database = Database(database_name= "pizza_store.db", 
                        database_type=DatabaseType.SQLITE)
    employee_application = EmployeeApplication(database).initialize()
    customer_application = CustomerApplication(database).initialize()

    print(
        "\n/***************************************/\n"
        "*                                       *\n"
        "* INTERACTION WITH EMPLOYEE APPLICATION *\n"
        "*                                       *\n"
        "/***************************************/\n")

    # Login with Admin
    print(
        "\n/***************************************/\n"
        "   LOGGING IN WITH ADMIN                 \n"
        "/***************************************/\n")
    employee_application.loginToApplication("dking74", "TestPass12")
    print("Logged in users: ", end="")
    print(employee_application.getUsersLoggedIn())
    employee_application.logoutOfApplication("dking74")

    print(
        "\n/***************************************/\n"
        "   ITEMS BEFORE ADDING                   \n"
        "/***************************************/\n")
    items = employee_application.getItems()
    print(items)

    print(
        "\n/***************************************/\n"
        "   ADDING ITEMS WITH ADMIN          \n"
        "/***************************************/\n")
    # Add pizza items
    employee_application.addItem(
       Pizza("Pepperoni Pizza", 15, PizzaShape.CIRCULAR,
           PizzaCrust.THICK, additional_toppings=[
               Topping('Pepperoni', 1.50),
               Topping('Pepper', .75)],
           description="Circular pepperoni pizza on Thick crust"))
    
    # Add drink item
    employee_application.addItem(
        Drink('Pepsi', 1.50, 18))

    # Add Breadstick item
    employee_application.addItem(
        Breadstick("Cheesy Bread", 8, 6.00))

    print(
        "\n/***************************************/\n"
        "   ITEMS AFTER ADDING                    \n"
        "/***************************************/\n")
    items = employee_application.getItems()
    print(items)

    print(
        "\n/***************************************/\n"
        "   REMOVE ITEM WITH ADMIN                \n"
        "/***************************************/\n")
    employee_application.removeItem(
        Breadstick("Cheesy Bread", 8, 6.00))

    print(
        "\n/***************************************/\n"
        "   ITEMS AFTER REMOVING                  \n"
        "/***************************************/\n")
    items = employee_application.getItems()
    print(items)

    # Login with non-admin
    print(
        "\n/***************************************/\n"
        "   LOGGING IN WITH NON-ADMIN             \n"
        "/***************************************/\n")
    employee_application.loginToApplication("jking12", "TestPass13")
    print("Logged in users: ", end="")
    print(employee_application.getUsersLoggedIn())
    employee_application.logoutOfApplication("jking12")

    print(
        "\n/***************************************/\n"
        "   ADDING PIZZA ITEM WITH NON-ADMIN      \n"
        "/***************************************/\n")
    employee_application.addItem(
       Pizza("Sausage Pizza", 15, PizzaShape.CIRCULAR,
           PizzaCrust.THICK, additional_toppings=[
               Topping('Sausage', 1.25)],
           description="Circular sausage pizza on Thick crust"))

    print(
        "\n/***************************************/\n"
        "   GETTING ITEMS WITH NON-ADMIN          \n"
        "/***************************************/\n")
    items = employee_application.getItems()
    print(items)

    print(
        "\n/***************************************/\n"
        "*                                       *\n"
        "* INTERACTION WITH CUSTOMER APPLICATION *\n"
        "*                                       *\n"
        "/***************************************/\n")    

    print(
        "\n/***************************************/\n"
        "   SIGNING UP FOR APPLICATION W/         \n" 
        "   ALREADY TAKEN ID                      \n"
        "/***************************************/\n")  
    customer_application.signupForApplication(
        "dking74", "TestPass17", "Devon", "King", "6362098949", "dking3@live.maryville.edu")

    print(
        "\n/***************************************/\n"
        "   SIGNING UP FOR APPLICATION W/         \n" 
        "   NEW, UNIQUE ID                        \n"
        "/***************************************/\n")  
    customer_application.signupForApplication(
        "dking47", "TestPass17", "Devon", "King", "6362098949", "dking3@live.maryville.edu")

    print(
        "\n/***************************************/\n"
        "   LOGGING INTO CUSTOMER APPLICATION     \n"
        "/***************************************/\n")
    customer_application.loginToApplication("dking47", "TestPass17") 

    print(
        "\n/***************************************/\n"
        "   ADDING ITEMS TO CART                   \n"
        "/***************************************/\n")
    customer_application.addToCart(
            Drink('Pepsi', 1.50, 18))
    customer_application.addToCart(
        Pizza("Pepperoni Pizza", 15, PizzaShape.CIRCULAR,
           PizzaCrust.THICK, additional_toppings=[
               Topping('Pepperoni', 1.50),
               Topping('Pepper', .75)],
           description="Circular pepperoni pizza on Thick crust"))

    print(
        "\n/***************************************/\n"
        "   GETTING THE ITEMS IN THE CART         \n"
        "/***************************************/\n")
    cart = customer_application.getCart()
    print(cart)

    print(
        "\n/***************************************/\n"
        "   SUBMITTING ORDER                      \n"
        "/***************************************/\n")
    customer_application.placeOrder(
            Payment("Devon King", 
                PaymentType.CASH,
                PaymentLocation.STORE))

    print(
        "\n/***************************************/\n"
        "   VIEWING ACTIVE ORDERS                 \n"
        "/***************************************/\n")
    current_orders = customer_application.getCurrentOrders()
    print(current_orders)

if __name__ == "__main__":
    main()