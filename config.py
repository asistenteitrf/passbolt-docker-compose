import os
from dotenv import load_dotenv
from utils.Class_Log import LogManager 
from utils.Class_ODBC import ClassMySQL
 
load_dotenv()
 
IP = os.environ['IP']
PORT = os.environ['PORT']
KEY_ID= os.environ['KEYID']
USER= os.environ['USER_MAIL']
BASE_URL = f'https://{IP}:{PORT}/'

#Folder To Save Sreenshot
ScreenShot_Path=os.environ['SCREENSHOTFOLDER']
LogsFile_Path=os.environ['DATA_LOGGS']

# temp USer
UserToms=os.environ['ValUser'] 
PassToms=os.environ['ValPass']

#BOT A EJECUTAR
BotToExecute=os.environ['VALIDADOS']

B2B = "PLATERAN B2B - Comercial"
TELEMARKETING= "PLATERAN Telemarketing"

Proceso= 'VALIDADOS'

TIMES_SLEEP = 180

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ADFS=[#FLUJO DE ELEMENTOS WEB DE TOMS Y FUNCIONES[ACCION,RUTA DEL ELEMENTO XPHAT,"DESCRIPCION DEL ELEMENTO WEB"] EN LA POSICION 0=[0-URL,1-HACER CLICK CON WAITH EXPLICITI,2-TEXT BOX A LLENAR,3-FUNCIONES]
                [0,"https://upretoms.temu.com.uy",'UR-Toms'],
                [1,'//input[@value="Inicie sesión como usuario de NT"]',"BTN-Inicie sesión como usuario de NT"],
                [2,"//input[@id='userNameInput']", 'IMPUT TEXT-Usuario'],
                [3,"//input[@id='passwordInput']", "IMPUT TEXT-Contraseña "],
                [4,"//span[contains(.,'Iniciar sesión')]","BTN-Iniciar Seccion Accionado"],
                [5,"//span[@id='errorText']","Texto Error"],
                [6,"//div[@id='nc-header']/div[3]/h1/a","LAVEL-Para Confirmar Que Habrio Sección"],
                [7,"//a[contains(text(),'Todas las tareas')]","LINK Todas Las Tareas"],
                [8,"//div[@id='title_attributes_id']/div/div[2]","En este Span Obtenemos si esta en Plateran Marketing o Plateran B2B"],      
                #Parametros
                
                [9,"//a[contains(text(),'Parámetros')]"," LINK Parámetros"],
                [10,"//a[contains(.,'Editar')]"," LINK Editar"],
                [11," //td[2]/span/table/tbody/tr/td/div/div/i"," Imput List Parámetros"],
                [12,"(//input[@type='text'])[9]"," Imput List Parámetros"],
                [13,"//td[2]/span/table/tbody/tr/td/div/div/i"," Ckick Parametros "],
                [14,"//a[contains(.,'Actualizar')]","Actualizar Parametros "],
                
                # Clientes
                [15,"//a[contains(text(),'Búsqueda')]","CLICK Busqueda"],   
                [16,"//span[contains(.,'Búsqueda de cuenta de cliente residencial')]","CLICK Leads Residenciales"],              
                [17,"//span[contains(.,'Búsqueda de cuenta de cliente empresarial')]","CLICK Leads Empresariales"],           
                [18,"(//input[@type='text'])[8]","IMPUT Clientes Residenciales"],
                [19,"(//input[@type='text'])[4]","IMPUT Clientes Empresariales"],                
                [20,"//button[contains(.,'Búsqueda')]","BUTTON BUSCAR"],                 
                [21,"(//input[@type='checkbox'])[106]","Check Como Elelemto para parar la Busqueda"],   
                                              
                [22,"/html[1]/body[1]/div[6]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/table[1]/tbody/tr","TABLE Cliente Result"],
                [23,"//h1/a","Indice de La Tabla Para Ver Si Encontraron Elementos"],  
                # OP 
                [24,"//a[contains(text(),'Órdenes de Venta')]","Orden de Venta"], 
                [25,"//div[3]/div[2]/div/table/thead/tr/th[2]/div/span[2]","FILTRO DE ORDEN"], 
                [26,"(//input[@type='text'])[3]","INPUT TEXT ORDER"], 
                [27,"(//button[@type='button'])[9]","BUTTON BUSCAR"],                  
                [28,"//div[3]/div[2]/div/table/tbody/tr","TABLE Order Result"], 
                [29,"//div[3]/div[2]/div/table/tbody/tr[1]/td[2]/div[1]/div[1]/a","TABLE Order Result lINK"],       
                [30,"//h1/a","LABEL Resultados De la Orden"],
                #ORDEN DE MOVIMIENTO
                #//div[@id='9139449226313357733']/div/form/table/tbody/tr/td/table/tbody/tr[16]/td[4]/div/table/tbody/tr/td/div/div/a
                # //body[1]/div[6]/div[3]/div[1]/div[2]/div[2]/div[2]/div[1]/form[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[16]/td[4]
                [31,"//body[1]/div[6]/div[3]/div[1]/div[2]/div[2]/div[2]/div[1]/form[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[16]/td[4]","LABEL Resultados De la Orden de Movimiento"],
                #RESULTADOS DE LA BUSQUEDA
                [32,"//div[2]/div/a","Ver todos los Registros"],
                [33,"(//div[@onclick=''])[4]","Level 4 Ver Todos los Registros"],
                [34,"//div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/table/tbody/tr","Tabla Resultado de los Productos y Cantidad"],
                [35," //a[contains(@href, '/startpage.jsp')]","CLICK Regresar Al Inicio"]
                ]
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


CNX = ClassMySQL()
logger = LogManager(max_log_size_mb=1)  # Configura el límite de tamaño en 1 MB para propósitos de demostración
