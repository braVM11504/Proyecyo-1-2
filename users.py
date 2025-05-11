# Estos son los paquetes que se deben instalar
# pip install pycryptodome
# pip install pyqrcode
# pip install pypng
# pip install pyzbar
# pip install pillow
# No modificar estos módulos que se importan
import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode
from PIL import Image
from json import dumps
from json import loads
from hashlib import sha256
from Crypto.Cipher import AES
import base64
import pyqrcode
from os import urandom
import io
from datetime import datetime
ruta="C:\\Users\\Usuario\\OneDrive\\Documents\\proyecto 1 prog\\users.txt"
espacio_parqueo = [
    {"name": "A1", "coords": (240, 70, 130, 60), "tipo": "Student"},
    {"name": "A2", "coords": (240, 155, 130, 60), "tipo": "Student"},
    {"name": "A3", "coords": (240, 240, 130, 60), "tipo": "Student"},
    {"name": "A4", "coords": (240, 325, 130, 60), "tipo": "Student"},
    {"name": "A5", "coords": (240, 415, 130, 65), "tipo": "Student"},
    {"name": "A6", "coords": (243, 499, 130, 70), "tipo": "Student"},
    {"name": "B1", "coords": (620, 72, 120, 70), "tipo": "profesor"},
    {"name": "B2", "coords": (620, 160, 120, 60), "tipo": "profesor"},
    {"name": "B3", "coords": (620, 250, 130, 60), "tipo": "profesor"},
    {"name": "B4", "coords": (620, 335, 130, 60), "tipo": "profesor"},
    {"name": "B5", "coords": (620, 420, 130, 60), "tipo": "profesor"},
    {"name": "B6", "coords": (618, 499, 140, 70), "tipo": "profesor"}
    ]


# Nombre del archivo cn la base de datos de usuarios
usersFileName="users.txt"

# Fecha actual
date=None
# Clave aleatoria para encriptar el texto de los códigos QR
key=None

# Función para encriptar (no modificar)
def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

# Función para desencriptar (no modificar)
def decrypt_AES_GCM(encryptedMsg, secretKey):
    (ciphertext, nonce, authTag) = encryptedMsg
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

# Función que genera un código QR (no modificar)
def generateQR(id,program,role,buffer):
    # Variables globales para la clave y la fecha
    global key
    global date

    # Información que irá en el código QR, antes de encriptar
    data={'id': id, 'program':program,'role':role}
    datas=dumps(data).encode("utf-8")

    # Si no se ha asignado una clave se genera
    if key is None:
        key =urandom(32) 
        # Se almacena la fecha actual
        date=datetime.today().strftime('%Y-%m-%d')
    
    # Si cambió la fecha actual se genera una nueva clave y 
    # se actualiza la fecha
    if date !=datetime.today().strftime('%Y-%m-%d'):
        key =urandom(32) 
        date=datetime.today().strftime('%Y-%m-%d')

    # Se encripta la información
    encrypted = list(encrypt_AES_GCM(datas,key))

    # Se crea un JSON convirtiendo los datos encriptados a base64 para poder usar texto en el QR
    qr_text=dumps({'qr_text0':base64.b64encode(encrypted[0]).decode('ascii'),
                                'qr_text1':base64.b64encode(encrypted[1]).decode('ascii'),
                                'qr_text2':base64.b64encode(encrypted[2]).decode('ascii')})
    
    # Se crea el código QR a partir del JSON
    qrcode = pyqrcode.create(qr_text)

    # Se genera una imagen PNG que se escribe en el buffer                    
    qrcode.png(buffer,scale=8)       

# Se debe codificar esta función
# Argumentos: id (entero), password (cadena), program (cadena) y role (cadena)
# Si el usuario ya existe deber retornar  "User already registered"
# Si el usuario no existe debe registar el usuario en la base de datos y retornar  "User succesfully registered"


def registerUser(id,password,program,role):  
    print("entro")
    users={}
    try:
        with open(ruta, "r") as file: 
            users=loads(file.read())
    except FileNotFoundError:
        print("No se encontro el archivo")
        pass
    if str(id) in users: 
        return "user already registered"
    users[str(id)]={"password":password,"program":program,"role":role} 
    print("registro")
    with open(ruta,"w") as file:
        file.write(dumps(users))
        return ("users succesfully registered")
    print("finaliza la funcion")

#Se debe complementar esta función
# Función que genera el código QR
# retorna el código QR si el id y la contraseña son correctos (usuario registrado)
# Ayuda (debe usar la función generateQR)
def getQR(id,password):
    print("entra a la funcion")
    buffer = io.BytesIO() 
    try:
        with open(ruta, "r") as file: 
            users=loads(file.read())
    except FileNotFoundError:
        print("No se encontro el archivo")
        pass  
    if str(id) not in users: 
        return ("El usuario no esta registrado")
    if users[str(id)]["password"]!=password:
        return print("La contraseña es incorrecta")
    print("verifico correctamente los datos")
    program=users[str(id)].get("program")
    role=users[str(id)].get("role")
    # Aquí va su código     
    generateQR(id,program,role,buffer)
    print("finaliza")
    return buffer



# Se debe complementar esta función
# Función que recibe el código QR como PNG
# debe verificar si el QR contiene datos que pueden ser desencriptados con la clave (key), y si el usuario está registrado
# Debe asignar un puesto de parqueadero dentro de los disponibles.
def sendQR(png):

    # Decodifica código QR
    decodedQR = decode(Image.open(io.BytesIO(png)))[0].data.decode('ascii')

    #Convierte el JSON en el texto del código QR a un diccionario
    data=loads(decodedQR)


    # Desencripta con la clave actual, decodificando antes desde base64. Posteriormente convierte a diccionario (generar error si la clave expiró)
    decrypted=loads(decrypt_AES_GCM((base64.b64decode(data["qr_text0"]),base64.b64decode(data["qr_text1"]),base64.b64decode(data["qr_text2"])), key))
    print(decrypted)
    id=str(decrypted["id"])
    role=str(decrypted["role"])
    

    try:
        with open(ruta, "r") as file:
                users = loads(file.read())  
    except FileNotFoundError:
        print ("Base de datos de usuarios no encontrada")
        pass 

    if id not in users:
        return print("Usuario no registrado")

    # Luego debe verificar qué puestos de parqueadero existen disponibles según el rol, si hay disponibles le debe asignar 
    # un puesto al usuario y retornarlo como una cadena
    cam = cv2.VideoCapture('http://172.20.10.8:8080/video')


    ret, frame = cam.read()
    if not ret:
        cam.release()
        error = "No se pudo capturar imagen de la camara"
        print(error)
        return error
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    bordes = cv2.Canny(gray, 100, 200)
    espacios_libres={"Student":[],
                     "profesor":[]}

    for e in espacio_parqueo:
            x, y, w, h = e["coords"]

            # Extraer región de interés 
            reg=bordes[y:y+h, x:x+w]

            
            can_bordes = cv2.countNonZero(reg)
            area = w * h
            o = can_bordes / area

            # Establecer un umbral para determinar si está ocupado o no
            umbral = 0.07
            status = "Ocupado" if o > umbral else "Libre"
            #color = (0, 0, 255) if status == "Ocupado" else (0, 255, 0)
            if status=="Libre":
                espacios_libres[e["tipo"]].append(e["name"])
            #cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            #cv2.putText(frame,f"{e["name"]}-{status}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    
    if role in espacios_libres and espacios_libres[role]:
        s= espacios_libres[role].pop(0)  
        spot = f"Puesto asignado a {id}: {s}"
        print(spot)
        return spot
    else:
        ss=f"No hay espacios disponibles para el rol: {role}"
        print(ss)
        return ss








    

