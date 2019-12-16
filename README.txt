The project described here demonstrates the functionality of an Online Pizza System.
There are 3 sub-systems that encompass the full system:
    1. Customer Application
    2. Employee Application
    3. Pizza Store Database

The Customer application is responsible for interaction with the customers,
and allows the customers to make orders and view order order_status.

The Employee application is responsible for managing the orders that are placed
by the customers. With this application, admins can also add employees, add orders,
add items, etc. Basically, every element of the database can be manipulated through
this application.

The Pizza Store database is responsible for keeping all data in the data Store
so that both parties can manipulate and enter data as appropriate.

THE DATABASE MUST BE CREATED WITH DATABASE_GENERATOR.PY BEFORE THE APPLICATION CAN BE RUN!

There should only be one external dependency to run the application.
This dependency is: sqlalchemy. Please install before trying to run.

This file is just a basic README to identify some
common things in the project. IT IS NOT CONCLUSIVE.

database_generator.py - This is the file to create the initial design
                        of database. This should not be run unless setting up.

database_viewer.py - This is a file to see the state of the database.
                     You can invoke this file to see what the database
                     looks like in testing.

main.py - Main entry point of program. To invoke driver,
          type `python main.py`.

application.py - This is where the main interaction with users take place.
                 There are two classes defined: CustomerApplication and EmployeeApplication,
                 obviously one to be used by customer and other employee.
                 All functionality to be achieved in the project runs through these
                 two interfaces. Nothing else should be needed.

manager.py - This file does the major heavy lifting in the project. The application.py
             basically routes all interface options to one of the managers defined in this
             file, and then this file has classes to call the appropriate actions.

viewers.py - This is kind of a sloppy file, but this provides basic viewing options
             for customers to certain items such as order_status. In a production environment,
             the functionality defined in this file would be refined.

The rest of the modules are pretty self-explanatory on what they accomplish.

This project is in development phase.