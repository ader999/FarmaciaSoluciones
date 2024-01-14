class creando_a_hora():

    def fecha(self):
        from datetime import datetime
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S")
        fecha=timestampStr.split()[0]
        año_mes =dateTimeObj.strftime("%d-%m-%Y").split()[0]
        hora = dateTimeObj.strftime("%H-%M-%S")
        hora=hora.split()[0]
        return fecha,año_mes,hora

    def conexion(self,query,parameters):
        from sql import Others as conSql
        return conSql().run_query(query,parameters)



    def RegistroText(self, parametros, ur):
       import os

       def ch():
        print(self.fecha())
        current_date = self.fecha()[1]+".txt"
        print(current_date)
        last_file_date = None
        if last_file_date != current_date:
            last_file_date = current_date
            file_name = "registro/facturas/"+ current_date
            try:
                file = open(file_name, "x")
                print("The file does not exist, creating a new file.")
            except FileExistsError:
                print("The file already exists, creating a new file.")
                file = open(file_name, "a")
        else:
            file_name = "registro/facturas/" + " " + current_date
            file = open(file_name, "a")
            print("The file already exists, appending to it.")

        factura="\n"+"\n"+"                                     FARMACIA SOLUCIONES"+"\n"+"----------------------------------------------------------------------------------------------"+"\n"+"Fecha= "+self.fecha()[0]+"\n"+"Atendido por= "+ur+"\n"+"----------------------------------------------------------------------------------------------"+"\n" "Articulos                                                   Precio    Cantidad    SudTotal"+"\n"+"----------------------------------------------------------------------------------------------" +"\n"+parametros[0]+"\n"+"----------------------------------------------------------------------------------------------"+"\n"+"Total    =         "+parametros[1]+"\n"+"Pago con =         "+parametros[2]+"\n"+"Vuelto   =         "+parametros[3]+"\n"+"----------------------------------------------------------------------------------------------"+"\n"
        file.write(factura)
        file.close()
       ch()



    def registroCredito(self,listap,datos):

        file = open("registro/credito/" +datos[0] + ".txt", "a")
        credito="                                     FARMACIA SOLUCIONES"+"\n"+"----------------------------------------------------------------------------------------------"+"\n"+"Fecha= "+self.fecha()[0]+"\n"+"Atendido por= "+datos[1]+"\n"+"Cliente= "+datos[0]+"\n"+"----------------------------------------------------------------------------------------------"+"\n" "Articulos                                                   Precio    Cantidad    SudTotal" +"\n"+"----------------------------------------------------------------------------------------------"+"\n"+listap + "\n"+"----------------------------------------------------------------------------------------------" + "\n"+"Total    =         "+str(datos[2])+"\n"+"\n"+"\n"
        file.write(credito)
        file.close()



    def RestandoProductoVendido(self,c,g):
        parameters=(c,)
        from sql import Others as con
        query="SELECT * FROM product WHERE name=?"
        datos=con().run_query(query,parameters).fetchall()[0][3]
        if datos <= 0:
           return
        restando = datos -int(g)
        nombre=c
        query="UPDATE product SET cantidad=? WHERE name=?"
        parameters=(restando,nombre)
        con().run_query(query,parameters)


        print(restando,"yaaaa")


    def registro_ventas(self,nombre,precio,f,usr,cantidad,code,):

        query = "SELECT descuento FROM product where name=?"

        descuento = self.conexion(query, parameters=(nombre,)).fetchall()[0][0]
        print('se inprime el descuento ',descuento)


        parameters = (nombre,precio,f,usr,cantidad,code,descuento)

        query = 'INSERT INTO registro_ventas(nombre,precio,fecha,usuario,cantidad,identificador,descuento) VALUES(?,?,?,?,?,?,?)'
        self.conexion(query,parameters)
        print("READy")

    def registro_ventas_hoy(self,parameters):
        query='INSERT INTO ventas(fecha,cantidad,vtusr,producto,clave_producto,presio) VALUES(?,?,?,?,?,?)'
        self.conexion(query,parameters)
