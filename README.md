# Proyecyo-1-2
Este es el servidor que desarrollé para el sistema de administración de parqueaderos. La idea principal es que los usuarios puedan ingresar escaneando un código QR y el sistema les asigne un puesto automáticamente según su rol
# ¿Qué hace este programa?
-Crea usuarios con diferentes roles (Profesor, estudiante).
-Genera códigos QR cifrados con AES.
-Escanea QR con una cámara o desde archivo.
-Asigna puestos libres automáticamente y evita repetirlos.
-Guarda la información en un archivo .json.
# Archivos utilizados
No modificables:

-[`parking_server`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/parking_server.py)

-[`parking_client`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/parking_client.py)

Modificables

-[`users`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/users.pys)

-[`test_parking_test`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/test_parking_client.py)

# Resultados finales 

Este es el codigo ya modificado implementado las funciones requeridas y su funcionamiento correcto 
[`users_modificado`](https://github.com/braVM11504/Proyecyo-1-2/blob/main/users.py)

# nota 
Para que el codigo funcione correctamente se debe modificar la funcion sendQr exactamene en la linea 179 y poner la direccion de la camara que se desea utilizar 
![image](https://github.com/user-attachments/assets/83bf5f75-717e-482c-bafa-02a919cd1691)

