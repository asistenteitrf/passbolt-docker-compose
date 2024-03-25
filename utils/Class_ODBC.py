import os
import json
import pyodbc
import pandas as pd

from config import *

insertobjets=[]
class ClassMySQL:
    def insert_into_query(self,table, columns, values):
        return 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, values)

    def delete_from_query(self,table, column, value):
        return "DELETE FROM %s WHERE %s = '%s'" % (table, column, value)

    def update_where_query(self,table, value, condition):
        return "UPDATE %s SET %s WHERE %s" % (table, value, condition)

    def select_from_query(self,column, table, condition=None):
        return "SELECT %s FROM %s WHERE %s" % (column, table, condition) if condition else "SELECT %s FROM %s" % (column, table)

    def move_to_query(self,table_to, table_from, condition):
        return "INSERT INTO %s SELECT * FROM %s WHERE %s" % (table_to, table_from, condition)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO QUE TIENE LA CONFIGURACIÓN DE LA CONECCIÓN DE LA BASE DE DATOS
    def getConn(self):
        return pyodbc.connect( "Driver={%s};Server=%s;Database=%s;UID=%s;PWD=%s;Trusted_Connection=no;" % (os.getenv('SQL_DRIVER'),os.getenv('SQL_SERVER'), os.getenv('SQL_DB'),os.getenv('SQL_USR'),os.getenv('SQL_PASS'))) 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO OBTENEMOS DATAFRAME
    def getDataFrame(self,sqlQuery):
        try:
            conn = self.getConn()
            sql_query = pd.read_sql_query(sqlQuery, conn)
            conn.close()
            return (True, pd.DataFrame(sql_query))
        except pyodbc.Error as ex:
            sqlstate = ex.args[0] + " | " + ex.args[1]
            return (False, sqlstate)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO EXECUTE
    def execute(self,sql_query):
        try:
            conn = self.getConn()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()
            cursor.close()
            conn.close()
            return (True, "Execute OK")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0] + " | " + ex.args[1]
            return (False, sqlstate)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO OBTENEMOS LAS ORDENES SEGÚN EL PROCESO
    def GET_OP_LIST(self,proceso):
        p = self.getDataFrame('''
                              SELECT DISTINCT TOP 5 TBOP as Orden,
                              PDANombreCliente as Nombre,
                              TBNumeroDocCliente as ID,
                              PDATelefonoContacto as Telefono, 
                              TBBodega as Bodega,                             
                              TBFechaMov AS Hora 
                              FROM
                              TareasBot    
                              INNER JOIN 
                              PedidosDatosAnexos ON PedidosDatosAnexos.PDAOp = TareasBot.TBOP AND PedidosDatosAnexos.PDACliente = TareasBOT.TBCliente                                                         
                              WHERE  
                              TBProceso = '%s' 
                              AND TBTomado = 0
                              AND TBBodega IN ('Telemarketing','B2B')                             
                              ORDER BY TBFechaMov ASC
        '''% (proceso)
        )
        return(p)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO OBTENER DADO UNA ORDEN TODOS LOS PRODUCTOS Y SUS EMEI
    def GET_OP_DATA_PRODUCT(self,order):
        datos = self.getDataFrame('''
                              SELECT PDANombreCliente as Nombre, TBNumeroDocCliente as ID , PDATelefonoContacto as Telefono,TBOP as Orden , TBProducto as Producto, TBCantidad as Cantidad  , TBIMEI as EMEI 
                              FROM TareasBot
                              INNER JOIN PedidosDatosAnexos ON PedidosDatosAnexos.PDAOp = TareasBot.TBOP AND PedidosDatosAnexos.PDACliente = TareasBOT.TBCliente
                              WHERE TBOP='%s'
                              AND TBProceso = 'VALIDADOS'                            
                              AND TBBodega IN ('Telemarketing','B2B')
                              ORDER BY TBProducto DESC
        '''% (order)
        )
        print(datos)
        insertobjets.clear()
        if(datos[0]==True):  
            list_imei=[]  
            Producto=""
            for indice, row in datos[1].iterrows():#Recorrermos Todas las OP Disponibles 
                   if indice==0:
                       Producto=row['Producto']
                   if (Producto == row['Producto']):
                       list_imei.append(row['EMEI'])
                   else:
                       self.AppendProduct(Producto,list_imei)
                       Producto = row['Producto']
                       list_imei=[]
                       list_imei.append(row['EMEI'])                                     
            self.AppendProduct(row['Producto'],list_imei)   
            datajson={
                      "Status":200,
                      "Order":order, 
                      "Productos": len(insertobjets),
                      "Data":insertobjets}
            json_data = json.dumps(datajson,indent=2)
            return  json_data   
        else:       
            datajson={
                      "Satatus":200}
            json_data = json.dumps(datajson,indent=2)
            return  json_data        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO TOMADO
    def SET_TOMADO(self,op):
        sql_query = self.execute(self.update_where_query("TareasBOT"," TBTomado = 1 , TBFechaProcesado =getdate()","TBOP = '%s' and TBProceso = 'VALIDADOS'" % (op)))
        return(sql_query) 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO INSERTAR EN LA TBREGISTRO 
    def SET_LOG_TBRegistro(self,op,estate,log):
            query = "INSERT INTO [Ga_Logistica].[dbo].[Registro] (RegOP,RegNDB,RegEstado,RegRepeticion,RegDate,RegLog) VALUES  ('%s','VALIDADOS','%s',1,getdate(),'%s');" % (op,estate,log)
            return(self.execute(query))
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MÉTODO INSERTAR EN LA TBREGISTRO 
    def SET_SERIES(self,array,productos):
         for index, product in enumerate(productos["Data"]):
             for index, emei in enumerate(product['IMEI']): 
                    query = ("INSERT INTO TareasBOT(TBNumeroDocCliente,TBProceso,TBTomado,TBCliente,TBOP,TBProducto,TBCantidad,TBIMEI,TBBodega) VALUES ('"+str(array['ID'])+"','SERIES',0,'45000','"+str(array['Orden'])+"','"+str(product['Producto'])+"',1,'"+str(emei)+"','"+str(array['Bodega'])+"')") 
                    self.execute(query)
                             
    def Aprobe(self,op):
        return(self.execute("UPDATE [Ga_Logistica].[dbo].[Registro] SET RegEstado = 'APROBADO', RegLog=CONCAT(RegLog, 'APROBADO;') WHERE RegOP = '%s';" % (op)))

    def getNotEndedImput(self):
        p = self.getDataFrame('''
           SELECT RegOP FROM Registro WHERE RegEstado = 'PROCESANDO' AND RegOP NOT IN 
           (SELECT RegOP FROM Registro WHERE RegEstado != 'PROCESANDO') 
           ORDER BY RegDate DESC '''
        )
        return(p)  
    
#-------------------- APPEND FUNCTION ---------------------
    def AppendProduct(self,Product, DataSerie) :   
        data_order={
                     "Producto": Product ,
                     "Cantidad": len(DataSerie) ,
                         "IMEI": DataSerie                                         
                                   }
        insertobjets.append(data_order)  