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

    # Implementa el lenguaje Cypher para crear un nodo con etiqueta Person
    # con atributos 'name y age '
    @staticmethod
    def _create_person(tx, name, age):
        tx.run("CREATE (:Person {name: $name, age: $age}) ", name=name, age=age)

    # Implementa el lenguaje Cypher para crear un nodo con etiqueta Destination
    # con atributos 'place_name y location '
    @staticmethod
    def _create_place(tx, place_name, location):
        tx.run("CREATE (:Destination {placeName: $place_name, location: $location})",
               place_name=place_name, location=location)



if __name__ == "__main__":
    # Connect to Server
    greeter = Turismo("bolt://localhost:7687", "neo4j", "Buxup2020")

    print("\n\n******************************************************************")
    print("\n\t\t\t Turismo")

    print("\n\n\t1. Crear usuario")
    print("\t2. Crear un lugar turistico")
    opcion =int((input("\n\tQue desea hacer?: ")))

    if (opcion == 1):
        name = input("\n\tIngrese nombre: ")
        age = int(input("\tIngrese edad: "))
        greeter.save_name(name, age) # LLama las funciones para crear  un usuario en la base de datos
        print("\n\tUsuario" ,name , "creado exitosamente")

    if(opcion == 2):
        place_name = input("\n\tIngrese nombre: ")
        location = input("\tUbicacion: ")
        # score = int(input("\tPuntuacion: "))
        # place_type = input("\tTipo de turismo: ")
        greeter.save_place(place_name, location)
        print("\n\tDestino ", place_name, " creado exitosamente")

    greeter.close()
