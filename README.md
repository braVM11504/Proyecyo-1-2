# INFORME DE PROYECTO: SISTEMA DE PARQUEADEROS


**Proyecto ID:** 1-2
**Autor:** Brayan villada 


# RESUMEN


Este documento describe el desarrollo de un servidor para un sistema de administración de parqueaderos. El objetivo principal del sistema es permitir a los usuarios (con roles definidos como Profesor o Estudiante) ingresar mediante el escaneo de un codigo Qr el cual se les asignará automáticamente un puesto de estacionamiento disponible acorde a su rol. La información del sistema se gestiona y almacena en formato JSON.


# 1. FUNCIONALIDADES PRINCIPALES DEL PROGRAMA


El sistema implementado cuenta con lo siguientes:

* **Gestión de Usuarios y Roles:**
    * Creación de usuarios con roles (ej. Profesor, Estudiante).
* **Generación y Manejo de Códigos QR:**
    * Generación de códigos QR cifrados utilizando el algoritmo AES para mayor seguridad.
    * Escaneo de códigos QR a través de una cámara conectada o desde un archivo de imagen existente.
* **Asignación de Puestos:**
    * Asignación automática de puestos de parqueadero libres.
    * Prevención de asignación de puestos ya ocupados o repetidos.
* **Almacenamiento de Datos:**
    * Almacenamiento de toda la información relevante del sistema en un archivo con formato JSON.

# 2. DE ARCHIVOS DEL PROYECTO


La estructura de archivos del proyecto se compone de los siguientes elementos, clasificados según su modificabilidad para el funcionamiento estándar:

# 2.1. Componentes (No Modificables):

[`parking_server`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/parking_server.py): Coidgo principal del servidor y lógica de administración.
    
[`parking_client`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/parking_client.py): Codigo o módulo cliente para la interacción con el servidor 

# 2.2. Archivos de Configuración/Datos (Modificables):

  [`users`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/users.py): Archivo que implementa las funciones que se realiazan mediante la solicitud del servidor.
  
  [`test_parking_client`](https://github.com/parrado/entrega1-proyecto-1-2025/blob/main/test_parking_client.py): Archivo utilizado para pruebas unitarias o de integración del sistema de parqueo.


# 3. RESULTADOS Y ESTADO ACTUAL


El código del proyecto ha sido modificado para implementar todas las funciones requeridas. Las pruebas realizadas confirman su correcto funcionamiento. El archivo que refleja la última versión estable y funcional de la gestión de usuarios es:

[`users_modificado`](https://github.com/braVM11504/Proyecyo-1-2/blob/main/users.py)

# 4. NOTAS IMPORTANTES


Para asegurar el correcto funcionamiento del frame del estacionamiento mediante cámara, es crucial realizar la siguiente modificación:

* **Archivo a Modificar:** [`users_modificado`](https://github.com/braVM11504/Proyecyo-1-2/blob/main/users.py)
* **Función:** `sendQr` 
* **Línea Específica:** `179`
* **Modificación Requerida:** Se debe actualizar la dirección o índice de la cámara que se utilizará para la captura de video.

    **Fragmento de Código de Referencia:**
    ```python
    177 # Luego debe verificar qué puestos de parqueadero existen disponibles según el rol, si hay disponibles le debe asignar
    178 # un puesto al asignarlo y retornarlo como una cadena
    179 cem = cv2.VideoCapture("[http://172.20.10.8:8080/video](http://172.20.10.8:8080/video)") # <- ACTUALIZAR ESTA LÍNEA
    ```
    Reemplace `"http://172.20.10.8:8080/video"` con el índice de su cámara (ej. `0`, `1`) o la URL correcta del stream de video.*

