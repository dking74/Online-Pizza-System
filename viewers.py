#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: To allow customers to view items from database
#
#######################################################

from abc import ABC, abstractmethod

from users import Customer

class Viewer(ABC):
    """ABC for interface to all viewers"""

    @abstractmethod
    def get(self, item):
        pass

    def __init__(self, database):
        self._database = database
        self._customer = Customer()

class LoginStatusViewer(Viewer):
    """Class to get login status funcitonality"""

    def get(self, login_account):
        """Get the user login to see if already one available"""

        return self._database.execute(
            "SELECT * FROM UserLogin "
            "WHERE Username='{0}' AND Password='{1}'".format(
                    login_account.getUsername(),
                    login_account.getPassword()))

class OrderStatusViewer(Viewer):
    """Class to get the status of an order"""

    def get(self, menu):
        """Get the menu to see if already one available"""
        return self._database.execute(
            "SELECT * FROM Menus WHERE MenuName='{0}' AND Description='{1}'".format(
                    menu.getMenuName(), menu.getDescription()))

class MenuViewer(Viewer):
    """Class to view the menus"""

    def get(self, menu):
        """Get the menu to see if already one available"""
        return self._database.execute(
            "SELECT * FROM Menus WHERE MenuName='{0}' AND Description='{1}'".format(
                    menu.getMenuName(), menu.getDescription()))
