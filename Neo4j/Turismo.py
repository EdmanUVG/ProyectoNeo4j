import sys

from neo4j import GraphDatabase
import os
from sys import platform
import time

class Turismo:


    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self.driver.close()



    # Envia el codigo del metodo '_create_person' a la base de datos.
    def save_name(self, name, age):
        with self.driver.session() as session:
            session.write_transaction(self._create_person, name, age)
