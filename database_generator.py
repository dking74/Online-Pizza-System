#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: This file is used only to generate the database.
#        : Do NOT use for any other reason.
#        : It will delete the database each time run.
#
#######################################################

from database import Database, DatabaseType

if __name__ == "__main__":
    # Prove that Database is a Singleton by creating instances and comparing
    database = Database(database_name= "pizza_store.db", 
                        database_type=DatabaseType.SQLITE, debug=True)

    # Try connecting to database and add data to database
    connected = database.connect()
    if (connected):
        # Drop tables if they exist
        database.execute("DROP TABLE PizzaToppings")
        database.execute("DROP TABLE MenuItems")
        database.execute("DROP TABLE Orders")
        database.execute("DROP TABLE OrderItems")
        database.execute("DROP TABLE Drinks")
        database.execute("DROP TABLE Pizzas")
        database.execute("DROP TABLE Breadsticks")
        database.execute("DROP TABLE Toppings")
        database.execute("DROP TABLE Addresses")
        database.execute("DROP TABLE Payments")
        database.execute("DROP TABLE UserLogin")
        database.execute("DROP TABLE Customers")
        database.execute("DROP TABLE Employees")
        database.execute("DROP TABLE Menus")
        database.execute("DROP TABLE Items")

        # Create the tables now
        database.execute(
            "CREATE TABLE Menus("
            "   MenuId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   ParentId INTEGER,"
            "   MenuName TEXT NOT NULL UNIQUE,"
            "   Description TEXT,"
            "   FOREIGN KEY(ParentId) REFERENCES Menus(MenuId)"
            ")"
        )
        database.execute(
            "CREATE TABLE Items("
            "   ItemId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   Name TEXT NOT NULL UNIQUE,"
            "   ItemType TEXT CHECK(ItemType IN('Pizza', 'Drink', 'Breadstick')),"
            "   Description TEXT,"
            "   Price REAL NOT NULL"
            ")"
        )
        database.execute(
            "CREATE TABLE MenuItems("
            "   MenuId INTEGER,"
            "   ItemId INTEGER,"
            "   FOREIGN KEY(MenuId) REFERENCES Menus(MenuId) ON UPDATE CASCADE ON DELETE CASCADE,"
            "   FOREIGN KEY(ItemId) REFERENCES Items(ItemId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )
        database.execute(
            "CREATE TABLE Drinks("
            "   DrinkId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   ItemId INTEGER,"
            "   Ounces INTEGER,"
            "   FOREIGN KEY(ItemId) REFERENCES Items(ItemId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )
        database.execute(
            "CREATE TABLE Pizzas("
            "   PizzaId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   ItemId INTEGER,"
            "   Crust INTEGER CHECK(Crust IN(0, 1, 2, 3)),"
            "   Shape INTEGER CHECK(Shape IN(0, 1)),"
            "   State INTEGER DEFAULT 0 CHECK(State IN (0, 1, 2, 3, 4)),"
            "   FOREIGN KEY(ItemId) REFERENCES Items(ItemId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )
        database.execute(
            "CREATE TABLE Breadsticks("
            "   BreadstickId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   ItemId INTEGER,"
            "   Count INTEGER,"
            "   Sauce TEXT,"
            "   FOREIGN KEY(ItemId) REFERENCES Items(ItemId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )
        database.execute(
            "CREATE TABLE Toppings("
            "   ToppingId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   ToppingName TEXT UNIQUE,"
            "   ToppingPrice REAL"
            ")"
        )
        database.execute(
            "CREATE TABLE PizzaToppings("
            "   PizzaId INTEGER,"
            "   ToppingId INTEGER,"
            "   FOREIGN KEY(PizzaId) REFERENCES Pizzas(PizzaId) ON UPDATE CASCADE ON DELETE CASCADE,"
            "   FOREIGN KEY(ToppingId) REFERENCES Toppings(ToppingId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )
        database.execute(
            "CREATE TABLE Addresses("
            "   AddressId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   Street TEXT,"
            "   City TEXT,"
            "   State TEXT,"
            "   ZipCode TEXT"
            ")"
        )
        database.execute(
            "CREATE TABLE Payments("
            "   PaymentId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   PaymentNumber INTEGER UNIQUE NOT NULL,"
            "   UserName TEXT NOT NULL,"
            "   PaymentType INTEGER NOT NULL,"
            "   PaymentLocation INTEGER NOT NULL,"
            "   CardNumber TEXT,"
            "   ExpDate TEXT,"
            "   CSV INTEGER"
            ")"
        )
        database.execute(
            "CREATE TABLE Customers("
            "   CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   FirstName TEXT NOT NULL,"
            "   LastName TEXT NOT NULL,"
            "   PhoneNumber TEXT,"
            "   EmailAddress TEXT NOT NULL UNIQUE,"
            "   PaymentId INTEGER,"
            "   FOREIGN KEY(PaymentId) REFERENCES Payments(PaymentId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )
        database.execute(
            "CREATE TABLE Employees("
            "   EmployeeId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   FirstName TEXT NOT NULL,"
            "   LastName TEXT NOT NULL,"
            "   PhoneNumber TEXT,"
            "   EmailAddress TEXT,"
            "   Pay REAL,"
            "   EmployeeType INTEGER"
            ")"
        )
        database.execute(
            "CREATE TABLE Orders("
            "   OrderId INTEGER PRIMARY KEY AUTOINCREMENT,"
            "   OrderNumber INTEGER UNIQUE,"
            "   Status INTEGER,"
            "   CustomerName TEXT NOT NULL,"
            "   CustomerEmail TEXT NOT NULL,"
            "   PaymentId INTEGER,"
            "   FOREIGN KEY(PaymentId) REFERENCES Payments(PaymentId)"
            ")"
        )
        database.execute(
            "CREATE TABLE OrderItems("
            "   OrderId INTEGER NOT NULL,"
            "   ItemId INTEGER NOT NULL,"
            "   FOREIGN KEY(OrderId) REFERENCES Orders(OrderId) ON UPDATE CASCADE ON DELETE CASCADE,"
            "   FOREIGN KEY(ItemId) REFERENCES Items(ItemId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )
        database.execute(
            "CREATE TABLE UserLogin("
            "   Username TEXT NOT NULL UNIQUE,"
            "   Password TEXT NOT NULL,"
            "   UserType TEXT CHECK(UserType IN('Customer', 'Employee')) NOT NULL,"
            "   Status INTEGER CHECK(Status IN(0, 1)) NOT NULL,"
            "   EmployeeId INTEGER,"
            "   CustomerId INTEGER,"
            "   FOREIGN KEY(EmployeeId) REFERENCES Employees(EmployeeId) ON UPDATE CASCADE ON DELETE CASCADE,"
            "   FOREIGN KEY(CustomerId) REFERENCES Customers(CustomerId) ON UPDATE CASCADE ON DELETE CASCADE"
            ")"
        )

        # Insert one admin into database for initial config
        database.execute(
            "INSERT INTO Employees ("
            "   FirstName, LastName, PhoneNumber, EmailAddress, Pay, EmployeeType"
            ") VALUES "
            " ('{0}','{1}','{2}','{3}','{4}',{5})".format(
                "Devon", "King",
                "6362098949", "dking3@live.maryville.edu",
                "70000", 1
            )
        )
        database.execute(
            "INSERT INTO Employees ("
            "   FirstName, LastName, PhoneNumber, EmailAddress, Pay, EmployeeType"
            ") VALUES "
            " ('{0}','{1}','{2}','{3}','{4}',{5})".format(
                "Jordan", "King",
                "4793727252", "jking14@live.maryville.edu",
                "72000", 3
            )
        )

        # Insert one login for admin into user logins
        database.execute(
            "INSERT INTO UserLogin ("
            "   Username, Password, UserType, Status, EmployeeId"
            ") VALUES "
            " ('{0}','{1}','{2}',{3},{4})".format(
                "dking74", "TestPass12",
                "Employee", 0, 1
            )
        )
        database.execute(
            "INSERT INTO UserLogin ("
            "   Username, Password, UserType, Status, EmployeeId"
            ") VALUES "
            " ('{0}','{1}','{2}',{3},{4})".format(
                "jking12", "TestPass13",
                "Employee", 0, 2
            )
        )

        # Create Initial Toppings to place in database
        database.execute(
            "INSERT INTO Toppings ("
            "   ToppingName, ToppingPrice"
            ") VALUES "
            "   ('Pepperoni', 1.50),"
            "   ('Chicken', 2.50),"
            "   ('Sausage', 1.25),"
            "   ('Ham', 1.50),"
            "   ('Bacon', 1.00),"
            "   ('Pepper', .75),"
            "   ('Cheese', .50),"
            "   ('Pineapple', .75)"
        )