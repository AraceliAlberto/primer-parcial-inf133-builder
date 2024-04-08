from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

list_Personaje = [
        {
            "id": 2,
            "name": "Robin",
            "level": 5,
            "role": "Archer",
            "charisma": 10,
            "strength": 10,
            "dexterity": 10,
        },
    ]

class Personajes:
    def __init__(self):
        self.id=None
        self.name = None
        self.level = None
        self.charisma = None
        self.strength = None
        self.dexterity = None

    def __str__(self):
        return f"id:{self.id}, name:{self.name}, level:{self.level}, charisma:{self.charisma}, strength:{self.strength}, dexterity:{self.dexterity}"

class PersonajeBuilder:
    def __init__(self):
        self.personajes=Personajes()
    
    def set_id(self,id):
        self.personajes.id = id
    
    def set_id(self,name):
        self.personajes.name = name

    def set_id(self,level):
        self.personajes.level = level

    def set_id(self,charisma):
        self.personajes.charisma = charisma

    def set_id(self,strength):
        self.personajes.strength = strength
    
    def set_id(self,dexterity):
        self.personajes.dexterity = dexterity

    def get_personaje(self):
            return self.personajes


class PersonajeService:
    @staticmethod
    def crear_personaje(data):
        personaje_nuevo = {
            "id": data.get("id"),
            "name": data.get("name"),
            "level":data.get("level"),
            "role": data.get("role"),
            "charisma":data.get("charisma"),
            "strength":data.get("strength"),
            "dexterity": data.get("dexterity"),
        }

        PersonajeBuilder.set_id = len(list_Personaje)+1
        list_Personaje.append(personaje_nuevo)
        return list_Personaje
    
    @staticmethod
    def actualizar_personaje(id, data):
        personaje = PersonajeService.buscar_personaje(id)
        if personaje:
            personaje.update(data)
            return list_Personaje
        else:
            return None
    
    @staticmethod
    def eliminar_personaje(id):
        personaje = PersonajeService.buscar_personaje(id)
        if personaje:
            list_Personaje.remove(id)
            return list_Personaje
        else:
            return None
        
    @staticmethod
    def buscar_personaje(id):
        personaje_encontrado = None
        for encontrado in list_Personaje:
            if encontrado["id"] == id:
                personaje_encontrado = encontrado
                break
        return personaje_encontrado

    @staticmethod
    def buscando_caracteristicas(role, level, charisma):
        rol_encontrado = None
        for encontrado in list_Personaje:
            if encontrado["role"] == "Archer" and encontrado["level"] == 5 and encontrado["charisma"] == 10:
                rol_encontrado = encontrado
                break
        return rol_encontrado
    
class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def read_data(handler):
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
class BuilderHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller=PersonajeService()
        super().__init__(*args,**kwargs)

    def do_POST(self):
        if self.path == "/characters":
            data = HTTPResponseHandler.read_data(self)
            nuevo_personaje = self.controller.crear_personaje(data)[-1]
            HTTPResponseHandler.handle_response(self, 201, nuevo_personaje)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        
        if "role" in query_params and "level" in query_params and "charisma" in query_params:
                rol = query_params['role']
                nivel = query_params['level']
                carisma = query_params['charisma']
                personaje_bus =self.controller.buscando_caracteristicas(rol, nivel, carisma)
                if personaje_bus:
                    HTTPResponseHandler.handle_response(self,200,personaje_bus)
                else:
                    HTTPResponseHandler.handle_response(self,404,{"Error":"No encontrado"})

        elif parsed_path.path == "characters/":
            id = int(self.path.split("/")[-1])
            personaje_id = self.controller.buscar_personaje(id)
            if personaje_id:
                HTTPResponseHandler.handle_response(self,200,personaje_id)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Personaje no encontrado"})

        elif parsed_path.path == "/characters":
            listapersonajes = list_Personaje
            HTTPResponseHandler.handle_response(self, 201, listapersonajes)
        else:
            HTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no encontrada"})
    
    def do_PUT(self):
            if self.path.startswith("/characters/"):
                id=int(self.path.split("/")[-1])
                data=HTTPResponseHandler.read_data(self)
                personaje=self.controller.actualizar_personaje(id,data)
                if personaje:
                    HTTPResponseHandler.handle_response(self,201,personaje)
                else:
                    HTTPResponseHandler.handle_response(self,404,{"Error":"Personaje no encontrado"})
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no encontrada"})
    
    def do_DELETE(self):
            if self.path.startswith("/characters/"):
                id = int(self.path.split("/")[-1])
                eliminando = self.controller.eliminar_personaje(id)
                if eliminando:
                    HTTPResponseHandler.handle_response(self,200,eliminando)
                else:
                    HTTPResponseHandler.handle_response(self,404,{"message":"Character deleted successfully"})
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no encotrada"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, BuilderHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
