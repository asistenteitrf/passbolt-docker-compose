# BOT SCHEMA 
An easy to use and easy to understand, Windows  and Linux Ubunto compatible, Python script for using Passbolt API - SELENIUM

# INSTALATION
1) Execute install.sh Linux or install.bat windows Or Install Requirement Before install python
2) Update .env configuration.
3) Update cromedriver
3) Install Gpg4win y Kleopatra
4) Cargar Claves Generadas por Passbolt y Compartir Claves
5) Open CMD execute python3 index.py


# Requirement List
Python Install:
Windows: https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe
Ubunto: ??

# pip install pip
Administrador de paquetes predeterminado para Python y ya está incluido en la instalación estándar de Python.

# pip install selenium
El paquete selenium se utiliza para automatizar la interacción con navegadores web desde Python. Puedes usarlo para realizar pruebas automatizadas, extraer datos de sitios web o interactuar con aplicaciones web.

# pip install schedule
El módulo schedule te permite programar tareas en Python de manera sencilla. Puedes ejecutar funciones periódicamente utilizando una sintaxis amigable. Por ejemplo, puedes programar una función para que se ejecute cada 10 segundos, cada hora o incluso a una hora específica del día. Lo Utilisamos en Index.py para la ejecución infinita del programa.

# pip install python-dotenv
El paquete python-dotenv te permite leer pares clave-valor desde un archivo .env y configurarlos como variables de entorno. Esto es útil para el desarrollo de aplicaciones siguiendo los principios de las aplicaciones de 12 factores. Lo Utilizamos en config.py

# pip install logging3
El paquete logging3 proporciona mejoras útiles para el registro de eventos en Python. Si deseas utilizar el módulo estándar de registro de Python, simplemente importa el módulo logging sin necesidad de instalar nada adicional. El módulo logging ya está incluido en la biblioteca estándar de Python 

# pip install pandas
El paquete pandas es una poderosa y flexible herramienta para trabajar con datos en Python. Proporciona estructuras de datos rápidas, flexibles y expresivas diseñadas para facilitar el trabajo con datos “relacionales” o “etiquetados”. Su objetivo es ser el bloque de construcción fundamental de alto nivel para realizar análisis de datos prácticos y del mundo real en Python. Lo Utilisamos en la clase Class_ODBC.py para manipular los resultados de las consultas.

# pip install httpx
El paquete httpx es un cliente HTTP de próxima generación para Python. Incluye una interfaz de línea de comandos integrada, soporte para HTTP/1.1 y HTTP/2, y proporciona APIs tanto síncronas como asíncronas. La Utilizamos para conectar con Passbolt

# pip install gnupg
El paquete gnupg proporciona una interfaz para acceder fácilmente a las funciones de gestión de claves, cifrado y firma de GnuPG desde programas Python. Puedes interactuar con GnuPG a través de descriptores de archivos. Los argumentos de entrada se verifican estrictamente y se sanitizan, por lo que este módulo debería ser seguro para usar en aplicaciones en red que requieran entrada directa del usuario. La Utilizamos para conectar con Passbolt.

# pip install pyodbc
El paquete pyodbc es un módulo de Python de código abierto que facilita el acceso a bases de datos ODBC. Implementa la especificación DB API 2.0 y ofrece una conveniencia aún más “pythonic”. La forma más sencilla de instalar pyodbc es mediante el uso de pip:

# CROME DRIVES UPDATE
https://googlechromelabs.github.io/chrome-for-testing/

# Install Gpg4win 
Primero, descarga Gpg4win desde el sitio oficial: Gpg4win.
https://www.gpg4win.org/download.html

# Ärbol de Directorios
--------------------
index.py    ----- 
app.py      -----
config.py   -----
app.log     -----
.env        -----
install.bat -----
install.sh  -----
README.md   -----
Folder utils
  - Class_Log.py        #Logs
  - Class_ODBC.py       #Data Base
  - Class_Passbolt.py   #Passbolt
  - Class_WebDriver.py  # Web Driver Actions
Folder screenshot #Save by Order the elemnt  in error .png
  - SO #00000000.png 
Folder backup #Save Backup logs by data
  - xx_xx_xx.bak
