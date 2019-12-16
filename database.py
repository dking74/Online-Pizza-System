#######################################################
#
# Author: Devon King
# Github: Kingster636
#
# Purpose: To define database connections in system
# Patterns: Facade and Singleton (Proxy later)
#
#######################################################

from enum import Enum
from abc import ABC, abstractmethod

import sqlalchemy

class DatabaseType(Enum):
    MYSQL       = 0
    SQL_SERVER  = 1
    ORACLE      = 2
    SQLITE      = 3
    POSTGRES    = 4

##############################################################
#
# These classes/interfaces utilizes 3 design patterns:
#   1. Facade
#   2. Singleton
#   3. Proxy
#
# There are a couple reasons for using both patterns:
#   1. We don't want multiple connections to a database open,
#      so we use a singleton instance.
#   2. We want to allow "smart" decisions regarding the creation of databases.
#      Using the connect method allows the class to return a connection
#      to a database that we want through facade.
#   3. The DatabaseProxy makes sure that multiple queries to same
#      databases arent going on at same time. We check to make sure
#      query isnt going on. If not, proceed. This just allows
#      traffic to stop until processing of other commands is done.
#
##############################################################
class DatabaseInterface(ABC):
    """Interface for Database connections"""

    @abstractmethod
    def execute(self):
        pass

class Database(DatabaseInterface):
    """Database Singleton for connections to databases"""
    _instance = None

    def __new__(cls, host=None, port=None, database_name=None, database_type=None, user=None, password=None, debug=False):
        """Create a new instance, but only one

        @param: host: string
              : The host to connect to / server
        @param: port: int
              : The port to listen on for server
        @param: database_name: string
              : The name of the database to connect to
        @param: database_type: DatabaseType
              : The type of database to connect to
        @param: user:string
              : The username which to connect with
        @param: password: string
              : The password associated with username
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._host = host
            cls._instance._port = port
            cls._instance._database = database_name
            cls._instance._database_type = database_type
            
            cls._instance._username = user
            cls._instance._password = password

            cls._instance._connecter = None
            cls._instance._executing = False

            cls._instance._debug = debug
        return cls._instance

    def connect(self):
        """Facade method to decide on database and connect.

        @return: The appropriate database connector instance
        """

        u  = (      self._username) if (self._username is not None) else ""
        pa = (":" + self._password) if (self._password is not None) else ""
        h  = ("@" + self._host    ) if (self._host     is not None) else ""
        po = (":" + self._port    ) if (self._port     is not None) else ""
        d  = ("/" + self._database) if (self._database is not None) else ""
        template_string = "{t}://{u}{pa}{h}{po}{d}"

        if self._database_type == DatabaseType.MYSQL:
            self._connecter = sqlalchemy.create_engine(
                template_string.format(t="mysql", u=u, pa=pa, h=h, po=po, d=d)).connect()
        elif self._database_type == DatabaseType.SQL_SERVER:
            self._connecter = sqlalchemy.create_engine(
                template_string.format(t="mssql", u=u, pa=pa, h=h, po=po, d=d)).connect()
        elif self._database_type == DatabaseType.ORACLE:
            self._connecter = sqlalchemy.create_engine(
                template_string.format(t="oracle", u=u, pa=pa, h=h, po=po, d=d)).connect()
        elif self._database_type == DatabaseType.SQLITE:
            self._connecter = sqlalchemy.create_engine(
                template_string.format(t="sqlite", u=u, pa=pa, h=h, po=po, d=d)).connect()
        elif self._database_type == DatabaseType.POSTGRES:
            self._connecter = sqlalchemy.create_engine(
                template_string.format(t="postgresql", u=u, pa=pa, h=h, po=po, d=d)).connect()
        elif self._database_type is None:
            return None

        # All databases we want foreign keys enabled
        res = self.execute("PRAGMA foreign_keys = 1")

        return self._connecter

    def execute(self, execution_string):
        """Execute the string from connector and get the results"""
        
        try:
            results = self._connecter.execute(execution_string)
            if results.returns_rows:
                return_data = results.fetchall()
            else:
                return []
        except Exception as e:
            if (self._debug):
                print(e)
            return_data = e

        return return_data

    def getConnecter(self):
        """Get the connection instance created by sqlalchemy"""
        return self._connecter

    def isConnected(self):
        """Determine if the connection is not none; determines connectivity"""
        return (self._connecter is not None)

    @classmethod
    def getInstance(cls):
        """Get the current connection instance"""
        return cls._instance

    def close(self):
        """Close connection, if there"""
        if self.isConnected():
            self._connecter.close()
            self._connecter = None