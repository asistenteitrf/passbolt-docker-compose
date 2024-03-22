from config import *
import schedule
import time

from app import SecuenciaBot

# Programa la tarea cada 5 minutos
schedule.every(0.10).minutes.do(SecuenciaBot)

# Ejecuta el planificador
while True:
    schedule.run_pending()
    time.sleep(1)