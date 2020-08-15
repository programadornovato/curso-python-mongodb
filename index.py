from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="escuela"
MONGO_COLECCION="alumnos"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLECCION]
ID_ALUMNO=""
def mostrarDatos():
    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find():
            tabla.insert('',0,text=documento["_id"],values=documento["nombre"])
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido "+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb "+errorConexion)
def crearRegistro():
    if len(nombre.get())!=0 and len(calificacion.get())!=0 and len(sexo.get())!=0 :
        try:
            documento={"nombre":nombre.get(),"calificacion":calificacion.get(),"sexo":sexo.get()}
            coleccion.insert(documento)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrarDatos()
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO=str(tabla.item(tabla.selection())["text"])
    #print(ID_ALUMNO)
    documento=coleccion.find({"_id":ObjectId(ID_ALUMNO)})[0]
    #print(documento)
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    sexo.delete(0,END)
    sexo.insert(0,documento["sexo"])
    calificacion.delete(0,END)
    calificacion.insert(0,documento["calificacion"])
    crear["state"]="disabled"
    editar["state"]="normal"
def editarRegistro():
    global ID_ALUMNO
    if len(nombre.get())!=0 and len(sexo.get())!=0 and len(calificacion.get())!=0 :
        try:
            idBuscar={"_id":ObjectId(ID_ALUMNO)}
            nuevosValores={"nombre":nombre.get(),"sexo":sexo.get(),"calificacion":calificacion.get()}
            coleccion.update(idBuscar,nuevosValores)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    crear["state"]="normal"
    editar["state"]="disabled"

ventana=Tk()
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="NOMBRE")
tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana,text="Nombre").grid(row=2,column=0)
nombre=Entry(ventana)
nombre.grid(row=2,column=1)
#Sexo
Label(ventana,text="Sexo").grid(row=3,column=0)
sexo=Entry(ventana)
sexo.grid(row=3,column=1)
#Calificacion
Label(ventana,text="Calificacion").grid(row=4,column=0)
calificacion=Entry(ventana)
calificacion.grid(row=4,column=1)
#Boton crear
crear=Button(ventana,text="Crear alumno",command=crearRegistro,bg="green",fg="white")
crear.grid(row=5,columnspan=2)
#Boton editar
editar=Button(ventana,text="Editar alumno",command=editarRegistro,bg="yellow")
editar.grid(row=6,columnspan=2)
editar["state"]="disabled"
mostrarDatos()
ventana.mainloop()