#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: To define menus in the system
# Patterns: Composition
#
#######################################################

from abc import ABC, abstractmethod

#######################################################
#
# Composite design pattern is perfect on a menu
# because it is possible for a menu to contain submenus.
#
# For this reason, we defined an interface 'SubmenuInterface'
# to allow a menu tree to print all submenus.
#
#######################################################
class SubmenuInterface(ABC):
    """SubmenuInterface is to return submenus"""

    @abstractmethod
    def getSubmenus(self):
        pass

class Menu(SubmenuInterface):
    """Class to represent a menu to be displayed to users"""
    
    _UPDATE_FIELDS = [
        "MenuName",    # --> self._menu_name
        "Description", # --> self._description
        "items",       # --> self._items
        "submenus"     # --> self._submenus
    ]

    def __init__(self, menu_name, description=None, items=None, submenus=None):
        self._menu_name = menu_name
        self._description = description or ""
        self._items = items or []
        self._submenus = submenus or []

        self._parent_menu = None

    def getMenuName(self):
        return self._menu_name

    def getDescription(self):
        return self._description

    def getItems(self):
        return self._items

    def getNumItems(self):
        return len(self._items)

    def getSubmenus(self):
        return self._submenus

    def hasSubmenus(self):
        return (True if len(self._submenus) > 0 else False)

    def hasItems(self):
        return (True if len(self._items) > 0 else False)

    def addItem(self, item):
        """Add item if not already in menu"""
        if item not in self._items:
            self._items.append(item)

    def addItems(self, *items):
        for item in items:
            self.addItem(item)

    def addSubmenu(self, menu):
        """Add submenu if not already in list.
        In addition to adding the menu to submenu list,
        make the current menu the submenus parent.
        """
        if menu not in self._submenus:
            menu.setParent(self)
            self._submenus.append(menu)

    def addSubmenus(self, *menus):
        for menu in menus:
            self.addSubmenu(menu)

    def getSubmenu(self, menu_name):
        """Search for a name in the submenus.
        Return the submenu if found, None if not.
        """
        for menu in self._submenus:
            if menu.name == menu_name:
                return menu
        return None

    def getItem(self, item_name):
        """Search for a name in the items.
        Return the item if found, None if not.
        """
        for item in self._items:
            if item.name == item_name:
                return item
        return None

    def setParent(self, parent_menu):
        """Set the parent menu"""
        self._parent_menu = parent_menu

    def getParent(self):
        """Get the parent menu"""
        return self._parent_menu

class MenuHierarchy(SubmenuInterface):
    def __init__(self, menu_list):
        self._menu_list = menu_list

    def getSubmenus(self):
        for menu in self._menu_list:
            print("({} -> {})".format(menu.getMenuName(), str(menu.getSubmenus())))

    def getSubmenuHierarchy(self):
        """Iterate through each submenu and get their submenus
        Returns a dict of tuples -> menu name maps to menu object, submenus
        """
        def getHierarchy(menu_list, menu_dict, original_list):
            temp_list = menu_list.copy()
            for menu in temp_list:
                if menu not in original_list:
                    continue
                original_list.remove(menu)
                if menu.hasSubmenus():
                    submenus = menu.getSubmenus()
                    menu_dict[menu.getMenuName()] = {}
                    getHierarchy(submenus, menu_dict[menu.getMenuName()], original_list)
                else:
                    menu_dict[menu.getMenuName()] = None

            return menu_dict

        original_list = self._menu_list.copy()
        hierarchy = getHierarchy(original_list, {}, original_list)

        return hierarchy