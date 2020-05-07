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

    def save_place(self, place_name, location):
        with self.driver.session() as session_save_place:
            session_save_place.write_transaction(self._create_place, place_name, location)

    def find_user(self, username):
        with self.driver.session() as session_find_user:
            session_find_user.read_transaction(self._search_user, username)

    # def load_user_preference(self, preference):
    #     with self.driver.session() as session_load_user_preference:
    #         session_load_user_preference.read_transaction(self._search_user_preference, preference)

    # Implementa el lenguaje Cypher para crear un nodo con etiqueta Person
    # con atributos 'name y age '
    
