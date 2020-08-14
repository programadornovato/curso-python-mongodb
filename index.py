from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="escuela"
MONGO_COLECCION="alumnos"

def mostrarDatos(tabla):
    try:
        cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
        baseDatos=cliente[MONGO_BASEDATOS]
        coleccion=baseDatos[MONGO_COLECCION]
        for documento in coleccion.find():
            tabla.insert('',0,text=documento["_id"],values=documento["nombre"])
            #print(documento["nombre"]+" "+documento["sexo"]+" "+str(documento["calificacion"]))
        #cliente.server_info()
        #print("Coneccion a mongo exitosa")
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido "+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb "+errorConexion)

ventana=Tk()
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="NOMBRE")
mostrarDatos(tabla)
ventana.mainloop()