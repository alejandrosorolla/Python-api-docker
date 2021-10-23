#Librerias necesarias para el funcionamiento
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

#Metodos de gestion de Json
def cargarProductos(fichero):
    with open(fichero) as file:
        return json.load(file)

def guardarProductos(fichero, data):
    with open(fichero, 'w') as file:
        json.dump(data, file, indent=4)

#Creacion de la app asi como gestor de peticiones
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

#Ruta al fichero Json de los productos
FICHERO_JSON = "listaProductos.json"
#LISTA_PRODUCTOS=cargarProductos(FICHERO_JSON)

#Clase que gestiona las peticiones sobre la direccion: http://LOCAL_HOST:4000/productos/
#Contiene peticiones GET y POST
class ListaProductos(Resource):
    def get(self):
        return cargarProductos(FICHERO_JSON)

    def post(self):
        listaProductos = cargarProductos(FICHERO_JSON)
        parser.add_argument("nombre")
        parser.add_argument("marca")
        parser.add_argument("distribuidor")
        parser.add_argument("precio")
        params = parser.parse_args()

        if params["nombre"] is None:
            return "Unprocessable Entity", 422

        idProducto = int(max(listaProductos.keys())) + 1
        listaProductos[str(idProducto)] = {
            "nombre": params["nombre"],
            "marca": params["marca"] if params["marca"] is not None else "Desconocido",
            "distribuidor": params["distribuidor"] if params["distribuidor"] is not None else "Desconocido",
            "precio": params["precio"] if params["precio"] is not None else "Desconocido"
        }
        guardarProductos(FICHERO_JSON, listaProductos)
        return listaProductos, 201

#Clase que gestiona las peticiones sobre la direccion: http://LOCAL_HOST:4000/productos/<idProducto>
#Contiene peticiones GET, PUT y DELETE
class Producto(Resource):
    def get(self, idProducto):
        listaProductos = cargarProductos(FICHERO_JSON)
        if idProducto not in listaProductos:
            return "NOT FOUND", 404
        else:
            return listaProductos[idProducto]

    def put(self, idProducto):
        listaProductos = cargarProductos(FICHERO_JSON)
        parser.add_argument("nombre")
        parser.add_argument("marca")
        parser.add_argument("distribuidor")
        parser.add_argument("precio")
        params = parser.parse_args()

        if idProducto not in listaProductos:
            return "NOT FOUND", 404
        else:
            producto = listaProductos[idProducto]

            producto["nombre"] = params["nombre"] if params["nombre"] is not None else producto["nombre"]
            producto["marca"] = params["marca"] if params["marca"] is not None else producto["marca"]
            producto["distribuidor"] = params["distribuidor"] if params["distribuidor"] is not None else producto[
                "distribuidor"]
            producto["precio"] = params["precio"] if params["precio"] is not None else producto["precio"]

            listaProductos[idProducto] = producto
            guardarProductos(FICHERO_JSON, listaProductos)
            return producto, 200

    def delete(self, idProducto):
        listaProductos = cargarProductos(FICHERO_JSON)
        if idProducto not in listaProductos:
            return "NOT FOUND", 404
        else:
            del listaProductos[idProducto]
            guardarProductos(FICHERO_JSON, listaProductos)
            return '', 204


#Añadir en la api los recursos creados
api.add_resource(ListaProductos, '/productos/')
api.add_resource(Producto, '/productos/<idProducto>')

if __name__ == '__main__':
    #Lanzamiento de la api
    app.run(host="0.0.0.0",port=4000,debug=True)

