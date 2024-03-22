import os
import time
import pyodbc
import logging
import datetime
import threading
import pandas as pd 
from app import *
from config import *

from utils.Class_Passbolt import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService

class WebDriver():#CLASE QUE MANIPULA LOS ELEMENTOS WEB Y FUNCIONES
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #CONTRUCTOR DEL NAVEGADOR
    def __init__(self) -> None:
        global driver                
        try: 
            driver = webdriver.Chrome() 
            driver.maximize_window()   
            driver.delete_all_cookies()
        except Exception as error: 
              logger.log_error("Error en apertura del Navegador : " + error.args)  
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO PARA OBTENER EL DRIVER
    def GetDriver(self,elemt):
        driver.get(elemt[1])  
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE HACE CLICK EN UN ELEMENTO CON UN WAITHEXPLICITI A ENCONTRAR UN ELEMENTO HASTA QUE SEA CLICLEABLE
    def Click(self,elemt):#SELENIUM LLENAR UN TEXT BOX     
         self.Implicit_Waith(elemt[1])
         driver.find_element(By.XPATH,elemt[1]).click()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE HACE CLICK EN UN ELEMENTO SIEMPRE Y CUANDO SEA CLICKEABLE
    def click_when_clickable(self,element):
        # Esperar hasta que un elemento específico sea cliclable (puedes ajustar el selector según tus necesidades)
        elemento_clicable = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, element)))
        # Realizar clic en el elemento
        elemento_clicable.click()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE NOS DEBUELVE UN TEXTO
    def get_text(self,elemt): 
        return driver.find_element(By.XPATH , elemt[1]).text 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO ENCARGADO DE LLENAR UN TEXTBOX COMO PARÉMETROS SE LE ENVÍA EL TEXTBOX Y EL TEXTO QUE DEBE LLENAR
    def Fill_Text_Box(self,textbox,texto):#SELENIUM LLENAR UN TEXT BOX
        self.Implicit_Waith(textbox[1])              
        driver.find_element(By.XPATH,textbox[1]).clear()
        for texto in texto:
               driver.find_element(By.XPATH,textbox[1]).send_keys(texto)
               time.sleep(0.03)          
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #IMPLICITYWAITH DE 180 SEGUNDOS QUE SI QUIERES CONFIGURAR MAS SEGUNDOS EN CONFIG LA VARIEBLE TIMESLEEP
    def Implicit_Waith(self,element):#SE LE HACE UN WAITH IMPLICITI A LOS ELEMENTOS WEB 
               wait = WebDriverWait(driver, 180)
               wait.until(EC.presence_of_element_located((By.XPATH, element)))   
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #DEBUELVE LA CANTIDAD DE FILAS DE UNA TABLA
    def RowCount(self,table): 
        time.sleep(2)         
        return len(driver.find_elements(By.XPATH , table[1]))
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------      
    #SCREENSHOT EL PARÁMETRO QUE SE LE ENVIA EN EL NÚMERO DE ORDEN
    def Screenshot(self,name):
        driver.save_screenshot(os.getcwd()+ ScreenShot_Path +str(name)+".png")       
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------               
    #CERRAMOS EL DRIVER
    def  Close(self):#CERRAMOS EL DRIVER WEB
        driver.close() 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
    #MÉTODO QUE SE ENCARGA DE INICIAR SECCIÓN
    def  Open_Section(self):
        #api = PassboltAPI(KEY_ID)
        #result =api.Get_Resource_Info(BotToExecute) ##Recursoq eu Buscamos es por el Nombre
        try:
            self.GetDriver(ADFS[0])             #Open Index Page TOMS Web with          
            self.Click(ADFS[1])                 #Click To Goin Loggin Page
            self.Fill_Text_Box(ADFS[2],UserToms)  #Tipping User
            self.Fill_Text_Box(ADFS[3],PassToms)  #Tipping Pass           
            #self.Fill_Text_Box(ADFS[2],result['user_resource'])  #Tipping User
            #self.Fill_Text_Box(ADFS[3],result['pass_resource'])  #Tipping Pass
            self.Click(ADFS[4])                 #Click Loggin Page
            #logguin Control
            try:
                response = self.get_text(ADFS[5]) #manejamos en caso de que este mal el usuario o la contraseña               
                logger.log_critical("Error en Inicio de Seccion " + str(response))                 
                return False            
            except:
                try: 
                    if self.get_text(ADFS[6])=="Rpa Compara Valida GA TOMS [U: UYRPALOGVALIDA001]": #QUE HABRIMOS SECCION Y QUE ESTAMOS ENL PAGINA DE INICIO                    
                       logger.log_info("Seccion Iniciada") 
                       return True                 
                except Exception as error:   
                    logger.log_critical("Error en Inicio de Seccion " + str(error.args))                     
                    return False            
        except Exception as error: 
                logger.log_critical("Error en Abrir Sección: " + str(error.args))                
                return False 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE CAMBIA DE PARÁMETROS SI ESTA EN TELEMRKETING A B2B Y VICEVERSA
    def  ChangeParams(self,bodega):
        self.Click(ADFS[7])
        if bodega=="B2B":
            location = B2B
        else:
            location = TELEMARKETING            
        try: 
            interaction=0
            while self.get_text(ADFS[8])!=location or self.get_text(ADFS[8])==""  and interaction < 5 :   
                  self.Click(ADFS[9])  #LINK Parámetros
                  self.Click(ADFS[10])  #LINK Editar                  
                  self.Click(ADFS[11])  #LINK Editar
                  self.Fill_Text_Box(ADFS[12],location)  #Tipping localización Telemarketing o B2B                 
                  self.Click(ADFS[13]) #CLICK en el List Box Para Fijar la Localización
                  self.Click(ADFS[14]) #CLICK Actualizar Parametro      
                  interaction +=1                   
                  self.Click(ADFS[7])
            if self.get_text(ADFS[8])!=location and interaction != 5:
                logger.log_info("Parámetros Actualizado a: "+ str(bodega)) 
                return True 
            else:
                logger.log_info("Parámetros: "+ str(bodega))   
                return True        
        except Exception as error: 
                logger.log_error("Error en Cambio de Parámetros: " + str(error.args))
                return False
            
    def elemento_presente(self):        
        try: 
             # Intenta encontrar el elemento
             if driver.find_element(By.XPATH,"//html[1]/body[1]/div[6]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/table[1]/tbody[1]"):
                return True
        except NoSuchElementException:
             # Si el elemento no se encuentra, devuelve False
             return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE MANEJA LA BUSQUEDA Y ACCIÓN DEL CLIENTE TANTO B2B Y TELEMARKETING
    def Client(self,array):
         self.Click(ADFS[15])  #LINK Menu Buscar                         
         if array['Bodega']== "Telemarketing":        
                  self.Click(ADFS[16])  #LINK  Leads Residenciales 
                  self.Fill_Text_Box(ADFS[18],array['ID'])  #TEXTBOX Clientes Residenciales 8
         else:
                  self.Click(ADFS[17])  #LINK  Leads Empresariales
                  self.Fill_Text_Box(ADFS[19],array['ID'])  #TEXTBOX Clientes Empresariles  4   
         self.Click(ADFS[20]) #CLICK Button Buscar   
         time.sleep(5)    
         x=1
         while x < 100: # intentar encontrar el elemento 1 segundos, sino, continua con el código
              try: 
                   rows = self.RowCount(ADFS[22]) # Obtenemos Todos los Resultados de la Tabla Cliente
                   if rows>=2:     
                       for row in range(rows-1) : # Recorremos Todas las Filas Encontradas 
                           flags=1  
                           client_name=driver.find_element(By.XPATH,"//tbody/tr["+str(row+1)+"]/td[2]/div[1]/div[1]/a").text # Obtenemos el Nombre
                           client_status=driver.find_element(By.XPATH," //table/tbody/tr["+str(row+1)+"]/td[4]/div/div/div/span[2]").text   #Obtenemos el Estado
                           if (client_status=='Activo' or  client_status=='Activación pendiente'):# Esta Activo     
                                 self.click_when_clickable("//tbody/tr["+str(row+1)+"]/td[2]/div[1]/div[1]/a[1]")                                                                           
                                 logger.log_info("Cliente "+str(client_name)+ " esta " + str(client_status))                              
                                 return True                                              
                       if(flags==1): #No Esta Activo
                           self.Screenshot(str(array['Orden']))
                           logger.log_warning("Cliente: "+str(array['Orden'])+" no esta Activo ni Activo Pendiente")
                           CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","CLIENTE NO ACTIVO")
                           CNX.SET_TOMADO(str(array['Orden']))
                           return False
                   else:
                       self.Screenshot(str(array['Orden'])) 
                       logger.log_warning("No Existe Datos Asociados a: "+str(array['Orden'])) 
                       CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","ID SIN RESULTADOS")
                       CNX.SET_TOMADO(str(array['Orden']))
                       return False             
              except: # en caso de no encontrarlo                      
                     x += 1 # Aumenta el contador    
                     time.sleep(5)
         if (x==100):
              self.Screenshot(str(array['Orden']))
              logger.log_critical("Ocurrio un Error a la Hora de Buscar el resultado del Cliente " + str(array['Orden']))
              CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","REDUNDANCIA CÍCLICA CLIENTE")
              CNX.SET_TOMADO(str(array['Orden']))
              return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE MANEJA LA ORDEN DE VENTA 
    def OrdenVenta(self,array):
         self.Click(ADFS[24])  #LINK Menu Buscar 
         self.Click(ADFS[25])  #LINK Menu Buscar 
         self.Fill_Text_Box(ADFS[26],array['Orden'])  #LINK Menu Buscar                 
         self.Click(ADFS[27])  #LINK Menu Buscar 
         time.sleep(5)
         x=1
         while x < 100: # intentar encontrar el elemento 1 segundos, sino, continua con el código
             try:  
                 rows = self.RowCount(ADFS[28]) # Obtenemos Todos los Resultados de la Tabla Order  
                 if rows>=2:  #Se encontro una orden                  
                        client_order=driver.find_element(By.XPATH,"//div[3]/div[2]/div/table/tbody/tr["+str(1)+"]/td[2]/div[1]/div[1]/a").text # Obtenemos el Nombre                                             
                        self.Click(ADFS[29])                        
                        if client_order== self.get_text(ADFS[30]):
                            logger.log_info("Orden: "+ str(array['Orden']) + " Resultado Busqueda: " + str(client_order)) 
                            return True 
                 else:
                        self.Screenshot(str(array['Orden']))
                        logger.log_warning("No Existe Datos Asociados a la Orden: "+str(array['Orden']))                         
                        CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","NO EXISTE DATOS DE ORDEN")
                        CNX.SET_TOMADO(str(array['Orden']))
                        return False   
             except: # en caso de no encontrarlo                      
                     x += 1 # Aumenta el contador
                     time.sleep(5) 
         if (x==100):
              self.Screenshot(str(array['Orden']))
              logger.log_critical("Ocurrio un Error a la Hora de Buscar el resultado de la Orden " + str(array['Orden']))
              CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","REDUNDANCIA CÍCLICA ORDEN")
              CNX.SET_TOMADO(str(array['Orden']))
              return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #METODO QUE OBTIENE EL PARÁMETRO DE LA ORDEN DE MOVIMIENTO Y DA CLICK
    def get_orden_mov(self,array):
        x =1
        time.sleep(5)
        while x < 100: # intentar encontrar el elemento 1 segundos, sino, continua con el código
             try:                 
                 orden_movimiento = self.get_text(ADFS[31])  
                 if (orden_movimiento!="" and  ("MO-PLATERAN" in orden_movimiento)):
                     logger.log_info("Resultado encontrado: "+ str(array['Orden']) + " : " + str(orden_movimiento)) 
                     self.click_when_clickable("//tr[16]/td[4]/div/table/tbody/tr/td/div/div/a")                    
                     return True
                 else:
                     self.Screenshot(str(array['Orden']))
                     logger.log_warning("No se Encontraron Orden de Movimiento Para Orden: " + str(array['Orden']))
                     CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","NO EXISTE ORDEN DE MOVIMIENTO")
                     CNX.SET_TOMADO(str(array['Orden']))
                     return False   
             except: # en caso de no encontrarlo                      
                 x += 1 # Aumenta el contador
                 time.sleep(2) 
        if (x==100):
              self.Screenshot(str(array['Orden']))
              logger.log_critical("Ocurrio un Error a la Hora de Buscar el resultado de la Orden " + str(array['Orden']))
              CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","REDUNDANCIA CÍCLICA EN MO-PLATERAN")
              CNX.SET_TOMADO(str(array['Orden']))
              return False
              
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE BUSCAR LOS ELEMENTOS QUE APARECEN EL LA WEB Y LOS COMPARA CON LOS DE TOMS
    def DocumentoActivo(self,array,products):
        products_ga = json.loads(products)
        time.sleep(5)
        x =1
        while x < 100: # intentar encontrar el elemento 1 segundos, sino, continua con el código
            try:
                  self.Click(ADFS[32]) #Damos Click lavel para Poner 200
                  self.Click(ADFS[33]) #Damos Click en 200
                  rows = self.RowCount(ADFS[34])-1# Obtenemos Todos los Resultados de la Tabla Order
                      # Verificar que las listas tengan la misma longitud    
                  if(rows!=products_ga["Productos"]):
                        self.Screenshot(str(array['Orden']))
                        logger.log_warning("No Coinciden la Cantidad de Productos de Toms ")
                        CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","GA Y TOMS NO COINCIDEN")
                        CNX.SET_TOMADO(str(array['Orden']))
                        return False 
                  # Recorrer las listas simultáneamente
                  else:
                       Tom = True
                       for row in range(rows) : # Recorremos Todas las Filas Encontradas 
                             GA = False
                             product_name=driver.find_element(By.XPATH,"//div[3]/div/div/div/div/div/table/tbody/tr["+str(row+1)+"]/td[2]/div/div/a").text # Obtenemos el Nombre                             
                             product_cant=driver.find_element(By.XPATH,"//div[3]/div/div/div/div/div/table/tbody/tr["+str(row+1)+"]/td[3]/div/div").text # Obtenemos el Nombre
                             for index, product in enumerate(products_ga["Data"]):
                                 if product_name == product["Producto"]:
                                     if(int(product_cant) == product["Cantidad"]):
                                          logger.log_info("Producto Toms "+ str(product_name) + " Cantidad: "+ str(product_cant) +" | "+ "Producto GA "+ str( product["Producto"]) + " Cantidad: "+ str(product["Cantidad"])+ " Coinciden.")
                                          GA=True    
                                          break 
                             if(GA==False):
                                 logger.log_warning("Producto Toms "+ str(product_name) + " Cantidad: "+ str(product_cant) +" | "+ "Producto GA "+ str( product["Producto"]) + " Cantidad: "+ str(product["Cantidad"])+" No Coinciden.")   
                                 Tom = False                 
                       if (Tom==False):
                              self.Screenshot(str(array['Orden']))
                              logger.log_warning("No Coinciden la Cantidad de Productos de Toms : "+str(rows) + " y GA" + str(products_ga["Productos"]))
                              CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","GA Y TOMS NO COINCIDEN")
                              CNX.SET_TOMADO(str(array['Orden']))
                              return False 
                       else:
                             logger.log_info("Coinciden TOMS y GA para Orden" + str(array['Orden']))
                             CNX.SET_LOG_TBRegistro(array['Orden'],"APPROVED","GA Y TOMS COINCIDEN")
                             CNX.SET_SERIES(array,products_ga)
                             CNX.SET_TOMADO(str(array['Orden']))
                             return False                     
            except: # en caso de no encontrarlo                      
                 x += 1 # Aumenta el contador
                 time.sleep(5)   
        if (x==100):
              self.Screenshot(str(array['Orden']))
              logger.log_critical("Inesperado en Hacer la Comparación de los productos de la Orden " + str(array['Orden']))
              CNX.SET_LOG_TBRegistro(array['Orden'],"ERROR","REDUNDANCIA CÍCLICA PRODUCTOS")
              CNX.SET_TOMADO(str(array['Orden']))
              return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO ENCARGADO DE LLEVAR A LA PAGINA DE INICIO PRA COMENZAR OTRO CLIENTE EN TOMS
    def BACK(self):
        x =1
        while x < 100: # intentar encontrar el elemento 1 segundos, sino, continua con el código
            try:  
                  
                  self.Click(ADFS[35])  #LINK Regresar al Inicio     
                  time.sleep(2)        
                  return True        
            except: # en caso de no encontrarlo                      
                  x += 1 # Aumenta el contador
                  time.sleep(5)   
        if (x==100):
              return False