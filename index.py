import time
import schedule
from config import *
from app import SecuenciaBot

# Programa la tarea cada 10 segundos
schedule.every(0.10).minutes.do(SecuenciaBot)

# Ejecuta el planificador
while True:
    schedule.run_pending()
    time.sleep(1)