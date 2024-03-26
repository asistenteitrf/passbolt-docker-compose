#---------------------------------------------------------------
#       BOT VERIFICACION DE SERIES Y PRODUCTOS
#---------------------------------------------------------------
from config import *
from utils.Class_WebDriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def SecuenciaBot():      
     Datos = CNX.GET_OP_LIST(Proceso)  #
     if(Datos[0]):  
          TOMS=WebDriver()  
          if (TOMS.Open_Section()==True): #Inicio de Sección
              for indice, dato in Datos[1].iterrows():#Recorrermos Todas las OP Disponibles 
                  if ("SO #" in dato['Orden']) and len(dato['Orden'])==14:  #VERIFICAMOS SI LA OP NO TIENE SO# O TIENE AL FINAL UN #1 NO SE PROCESA              
                      logger.log_info("------------------------------------------------- START ------------------------------------------------------- ")  
                      logger.log_info(f"Índice: {indice}, Orden: {dato['Orden']}, Nombre: {dato['Nombre']}, Id: {dato['ID']}, Tel: {dato['Telefono']}, Bodega: {dato['Bodega']}")                 
                      if(TOMS.ChangeParams(dato['Bodega'])==True): #Cambio de Prametros en Casos de B2B pasa a Plateran y Viceversa                           
                          if(TOMS.Client(dato)==True):  # sI ENCUENTRO CLIENTE SIGO
                              if (TOMS.OrdenVenta(dato)==True): #SI ORDEN DE VENTA SIGO
                                  if(TOMS.get_orden_mov(dato)==True): #SI ORDEN DE MOVIMIENTO                                                                   
                                      if(TOMS.DocumentoActivo(dato,CNX.GET_OP_DATA_PRODUCT(dato['Orden']))==True): #COMPARACION DE LOS PRODUCTOS
                                           terminado=0                             
                      TOMS.BACK()  
                  else:
                      CNX.SET_TOMADO(dato['Orden'])
              logger.log_info("------------------------------------------------- END ------------------------------------------------------- ") 
              TOMS.Close()                         
     else:
          logger.log_info("Sin Registros")
             
    
    