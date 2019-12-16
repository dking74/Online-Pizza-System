#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: This file is used only to view all entries in database.
#        : Do NOT use for any other reason.
#
#######################################################

from database import Database, DatabaseType

def printEntry(table, database):
    print(database.execute("SELECT * FROM {0}".format(table)))

if __name__ == "__main__":
    # Prove that Database is a Singleton by creating instances and comparing
    database = Database(database_name= "pizza_store.db", 
                        database_type=DatabaseType.SQLITE, debug=True)

    # Try connecting to database and add data to database
    connected = database.connect()
    if (connected):
        # EMPLOYEE PRINT
        print("Employees")
        printEntry("Employees", database)
        print("\n")

        # CUSTOMER PRINT
        print("Customers")
        printEntry("Customers", database)
        print("\n")

        # USERLOGIN PRINT
        print("UserLogins")
        printEntry("UserLogin", database)
        print("\n")

        # MENUS PRINT
        print("Menus")
        printEntry("Menus", database)
        print("\n")

        # ITEMS PRINT
        print("Items")
        printEntry("Items", database)
        print("\n")

        # MENUITEMS PRINT
        print("MenuItems Link")
        printEntry("MenuItems", database)
        print("\n")

        # DRINKS PRINT
        print("Drinks")
        printEntry("Drinks", database)
        print("\n")

        # PIZZAS PRINT
        print("Pizzas")
        printEntry("Pizzas", database)
        print("\n")

        # TOPPINGS PRINT
        print("Toppings")
        printEntry("Toppings", database)
        print("\n")

        # PIZZATOPPINGS PRINT
        print("PizzaToppings Link")
        printEntry("PizzaToppings", database)
        print("\n")

        # BREADSTICKS PRINT
        print("Breadsticks")
        printEntry("Breadsticks", database)
        print("\n")

        # ORDERS PRINT
        print("Orders")
        printEntry("Orders", database)
        print("\n")

        # ORDERITEMS PRINT
        print("OrderItems Link")
        printEntry("OrderItems", database)
        print("\n")

        # PAYMENTS PRINT
        print("Payments")
        printEntry("Payments", database)
        print("\n")