#!/bin/bash

# Instalar Python (si no está instalado)
sudo apt-get update
sudo apt-get install python3

# Instalar pip (administrador de paquetes de Python)
sudo apt-get install python3-pip

# Instalar algunas dependencias comunes (puedes agregar más según tus necesidades)
pip install pandas numpy requests


# pip install selenium
pip install selenium

# pip install schedule
pip install schedule

# pip install python-dotenv
pip install python-dotenv

# pip install logging3
pip install logging3

# pip install pandas
pip install pandas

# pip install httpx
pip install httpx

# pip install gnupg
pip install gnupg

# pip install pyodbc
pip install pyodbc

# pip install pyodbc
cp .env .env_config



echo "¡Instalación completa!"
