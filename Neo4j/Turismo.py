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
    def save_name(self, name, age, home, preference):
        with self.driver.session() as session:
            session.write_transaction(self._create_person, name, age, home, preference)

    def save_place(self, place_name, location):
        with self.driver.session() as session_save_place:
            session_save_place.write_transaction(self._create_place, place_name, location)

    def find_user(self, username):
        with self.driver.session() as session_find_user:
            session_find_user.read_transaction(self._search_user, username)

    def create_visit_relation(self, username, place_name):
        with self.driver.session() as session_create_visit_relation:
            session_create_visit_relation.write_transaction(self._create_visit_relation, username, place_name)

    def create_like_relation(self, username, place_name):
        with self.driver.session() as session_create_like_relation:
            session_create_like_relation.write_transaction(self._create_like_relation, username, place_name)

    def create_review_relation(self, username, place_name, rate, summary):
        with self.driver.session() as session_create_review_relation:
            session_create_review_relation.write_transaction(self._create_review_relation, username, place_name, rate, summary)

    def delete_user(self, username):
        with self.driver.session() as session_delete_user:
            session_delete_user.write_transaction(self._delete_user, username)


    # Implementa el lenguaje Cypher para crear un nodo con etiqueta Person
    # con atributos 'name y age '
    @staticmethod
    def _create_person(tx, name, age, home, preference):
        tx.run("CREATE (:Person {name: $name, age: $age, home: $home, preference: $preference}) ",
               name=name, age=age, home=home, preference=preference)

        tx.run("MATCH (p:Person), (l:Location)"
               " WHERE p.name=$name AND l.locationName=$home"
               " CREATE (p)-[r:LIVES_IN]->(l)", name=name, home=home)

    # Implementa el lenguaje Cypher para crear un nodo con etiqueta Destination
    # con atributos 'place_name y location '
    @staticmethod
    def _create_place(tx, place_name, location):
        tx.run("CREATE (:Destination {placeName: $place_name, location: $location})",
               place_name=place_name, location=location)

    # Implementa el lenguaje Cypher para buscar un nodo con etiqueta Person
    # con atributos 'name '
    @staticmethod
    def _search_user(tx, username):
        global preferencia
        global home
        for record in tx.run("MATCH (p:Person)"
                             " WHERE p.name=$username"
                             " RETURN p.name, p.preference, p.home", username=username):
            user_account(record["p.name"])
            preferencia = record["p.preference"]
            home = record["p.home"]

        for record in tx.run("MATCH (d:Destination) "
                             "WHERE d.classification=$preference "
                             "RETURN d.placeName LIMIT 2", preference=preferencia):
            print("\t", record["d.placeName"])

        for record in tx.run("MATCH (d:Destination)"
                             " WHERE d.location=$home"
                             " RETURN d.placeName LIMIT 2", home=home):
            print("\t", record["d.placeName"])

        for record in tx.run("MATCH (p:Person {name:$username})-[:LIKED|VISITED|REVIEWED]-(d:Destination)"
                             " RETURN d.placeName", username=username):
            print("\t", record["d.placeName"])

        for record in tx.run("MATCH (p:Person)-[:VISITED|LIKED|REVIEWED]->(d:Destination)"
                             " RETURN d.placeName LIMIT 2"):
            print("\t", record["d.placeName"])

    @staticmethod
    def _create_visit_relation(tx, username, place_name):
        tx.run("MATCH (p:Person), (d:Destination)"
               " WHERE p.name= $username AND d.placeName= $place_name"
               " CREATE (p)-[:VISITED]->(d)", username=username, place_name=place_name)

    @staticmethod
    def _create_like_relation(tx, username, place_name):
        tx.run("MATCH (p:Person), (d:Destination)"
               " WHERE p.name= $username AND d.placeName= $place_name"
               " CREATE (p)-[:LIKED]->(d)", username=username, place_name=place_name)

    @staticmethod
    def _create_review_relation(tx, username, place_name, rate, summary):
        tx.run("MATCH (p:Person), (d:Destination)"
               " WHERE p.name= $username AND d.placeName=$place_name"
               " CREATE (p)-[r:REVIEWED {rate: $rate, summary:$summary}]->(d)",
               username=username, place_name=place_name, rate=rate, summary=summary)

    @staticmethod
    def _delete_user(tx, username):
        tx.run("MATCH (p:Person)"
               " WHERE p.name=$username"
               " DETACH DELETE p",  username=username)


# Limpia consola
def clear_screen():
    if (platform == "darwin"):
        os.system('clear')
    elif (platform == "win32"):
        os.system('cls')


def user_account(name):
    clear_screen()
    header_screen()
    _global_username = name
    # _global_preference = preference

    print("\n\t\t\t\t\t\tWelcome: ", _global_username)

    print("\n\n\t\tRecomendaciones\n\n")


def loading_screen():

    toolbar_width = 40
    # setup toolbar
    sys.stdout.write("\t\t[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

    for i in range(toolbar_width):
        time.sleep(0.1)  # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")  # this ends the progress bar


def header_screen():
    print("\n\n**********************************************************************"
          "****************************************************************")
    print("\n\t\t\t\t\t\t\tTurismo")


def menu():
    clear_screen()
    header_screen()
    print("\n\n\n\t\t1. Crear usuario")
    print("\n\t\t2. Crear un lugar turistico")
    print("\n\t\t3. Ingresar a mi cuenta")
    print("\n\t\t4: Eliminar usuario")
    print("\n\t\t5: Salir")


    opcion = int((input("\n\n\t\tQue desea hacer?: ")))

    global username

    if (opcion == 1):
        clear_screen()
        header_screen()
        print("\n\n\t\t\t\tCrear usuario")
        username = input("\n\t\tIngrese nombre: ")
        age = int(input("\n\t\tIngrese edad: "))
        home = input("\n\t\tIngrese departamento donde vive: ")
        preference = input("\n\t\tIngrese preferencias: ")
        greeter.save_name(username, age, home, preference)  # LLama las funciones para crear  un usuario en la base de datos
        time.sleep(1)
        print("\n\n\t\tUsuario:", username, "creado exitosamente\n")
        time.sleep(1)
        print("\n\n\t\tCargando recomendaciones....\n")
        loading_screen()
        greeter.find_user(username)
        menu()


    elif (opcion == 2):
        place_name = input("\n\n\t\tIngrese nombre: ")
        location = input("\n\t\tUbicacion: ")
        greeter.save_place(place_name, location)
        print("\n\n\t\tDestino:", place_name, "creado exitosamente\n")
        loading_screen()
        clear_screen()
        menu()



    elif (opcion == 3):
        clear_screen()
        header_screen()
        print("\n\n\t\t\t\tIngresar a mi cuenta")
        username = input("\n\n\t\tIngrese usuario: ")
        print("\n")
        loading_screen()
        greeter.find_user(username)
        acount_menu()

    elif (opcion == 4):
        clear_screen()
        header_screen()
        print("\n\n\t\t\t\tEliminar usuario")
        username = input("\n\n\t\tIngrese usuario: ")
        print("\n")
        print("\n\n\t\tEliminando usuario....\n")
        loading_screen()
        greeter.delete_user(username)
        print("\n\n\t\tUsuario:", username, "eliminado exitosamente\n")
        menu()

    elif (opcion == 5):
        clear_screen()
        sys.exit(0)

    else:
        print("\n\n\t\tOpcion incorrecta. Intentar de nuevo")
        menu()


def acount_menu():
    print("\n\t\t1: Visitar destino: ")
    print("\n\t\t2: Like destino: ")
    print("\n\t\t3: Review destino: ")
    print("\n\t\t4: Cerrar Session")

    opcion = int(input("\n\n\t\tQue desea hacer?: "))

    if (opcion == 1):
        place_name = input("\n\n\t\tIngrese lugar turistico: ")
        greeter.create_visit_relation(username, place_name)
        print("\n")
        loading_screen()
        print("\n\n\t\tRelacion creada exitosamente\n")
        time.sleep(0.4)
        clear_screen()
        header_screen()
        greeter.find_user(username)
        acount_menu()

    elif (opcion == 2):
        place_name = input("\n\n\t\tIngrese lugar turistico: ")
        greeter.create_like_relation(username, place_name)
        print("\n")
        loading_screen()
        print("\n\n\t\tRelacion creada exitosamente\n")
        time.sleep(0.4)
        clear_screen()
        header_screen()
        greeter.find_user(username)
        acount_menu()

    elif (opcion == 3):
        place_name = input("\n\n\t\tIngrese lugar turistico: ")
        rate = input("\n\n\t\tIngrese calificacion de 1 a 5: ")
        summary = input("\n\n\t\tIngrese comentario: ")
        greeter.create_review_relation(username, place_name, rate, summary)
        print("\n")
        loading_screen()
        print("\n\n\t\tRelacion creada exitosamente\n")
        time.sleep(0.4)
        clear_screen()
        header_screen()
        greeter.find_user(username)
        acount_menu()

    elif(opcion == 4):
        menu()

    else:
        print("\n\n\t\tOpcion incorrecta. Intentar de nuevo")
        acount_menu()


if __name__ == "__main__":
    # Connect to Server
    greeter = Turismo("bolt://localhost:7687", "neo4j", "Buxup2020")

    menu()

    greeter.close()
