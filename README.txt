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

I hope this is sufficient...If given more time, this project would
be much better. However, for demo, I think this gets the point across.

I will probably work on this a little more moving forward because I became
really interested in it, but just didn't have enough time to implement further.