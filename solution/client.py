
import requests

url = "http://localhost:8000/"

#Creando nuevo Personaje
print("----> Creando personaje.....")
crear_personaje={
    "name": "Gandalf",
    "level": 10,
    "role": "Wizard",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response_crear=requests.post(url+"characters", json=crear_personaje)
print(response_crear.text)

#Listar los personajes
print("\n----> Lista de los Personajes.....")
response=requests.get(url+"characters")
print(response.text)

#buscar por id
print("\n----> Buscando al ID.....")
response_id = requests.get(url+"characters/2")
print(response_id.text)

#Listar personajes rol Archer, 5, 10
print("\n----> Buscando Caracteristicas.....")
response_caracteristicas = requests.get(url+"characters/?role=Archer&level=5&charisma=10")
print(response_caracteristicas.text)

#Actualizar por Id
print("\n----> Actualizar por ID.....")
actualizando={
    "charisma": 20,
    "strength": 15,
    "dexterity": 15,
}
response_actualizar=requests.put(url+"characters/2", json=actualizando)
print(response_actualizar.text)

#Eliminar personaje por Id
print("\n----> Eliminar Personaje.....")
eliminandoP = requests.delete(url+"characters/3")
print(eliminandoP.text)

#Creando nuevo Personaje
print("\n ----> Creando nuevo personaje.....")
crear_personaje={
    "name": "Legolas",
    "level": 5,
    "role": "Archer",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response_crear=requests.post(url+"characters", json=crear_personaje)
print(response_crear.text)

#Listar los personajes
print("\n----> Lista de los Nuevos Personajes.....")
response=requests.get(url+"characters")
print(response.text)