#!/usr/bin/env python
  #------IMPORTACIONES----------------------------------
import tkinter as tk
from os.path import isdir
from sys import path
from tkinter import messagebox as mb
from tkinter import ttk, CENTER, END, W, E,N,S,PhotoImage
from tkinter import scrolledtext as st
from tkinter import *
from datetime import datetime
color_verde="#2ECC71"

from hora import creando_a_hora as hr
from registro import Registro as reg
import os

from sql import Others as conSql

 #------END-----IMPORTACIONES---------------------------





class root():

    def __init__(self,usr,nombre_usr):
        self.nombre_usr=nombre_usr
        print("tipo de usr",usr)
        self.usr=usr


        from sql import Others as conSql
        self.conSql=conSql




        self.vt =tk.Tk()
        self.vt.title("Farmacia Soluciones ⚚ "+nombre_usr)
        #self.vt.minsize(height=545,width=1150)
        #resizable es para borrar el boton de maximizar
        #self.vt.resizable(False, False)

        self.cuaderno1 = ttk.Notebook(self.vt)
        self.cuaderno1.grid(column=0, row=0, padx=0, pady=0)


        #______________Estilos___________________________________________
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font = ('calibri', 10, 'bold'),foreground = 'red' )
        self.style.map('TFrame',foreground="#ff385f")
        self.style.map('TButton', foreground = [('active', '!disabled', 'green')],background = [('active', 'gray')])
        self.style.configure('Treeview.Heading', background="red3")



        #___________END________ESTILOS__________________________________________

        self.consulta_por_codigo()
        if self.usr == "root" or self.usr == "semi_root":
          self.insertar_producto()
        self.registro()
        self.credito()
        #self.estadisticas()
        self.DetallesDeProductos()
        if self.usr == "root":
          self.configuraciones()
        self.informacion()
        self.octener_productos_tabla_credito()
        self.TotalVentasD()
        reg().eliminar_t()
        #self.tabla_Cliente()




        #self.octener_clientes()
        #self.cuaderno1.grid(column=0, row=0, padx=0, pady=0)
        self.vt.geometry("1170x600")
        self.vt.mainloop()



    def OctenerFecha(self):
        import calendar
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        fecha=timestampStr.split()[0]
        año_mes =dateTimeObj.strftime("%d-%m-%Y").split()[0]
        hora = dateTimeObj.strftime("%H-%M-%S")
        hora=hora.split()[0]
        return fecha,año_mes,hora


    def octener_productos(self):

        #Limpiando la tabla
        records= self.lista_producto.get_children()
        for elementos in records:
            self.lista_producto.delete(elementos)
        #Consultando los datosdef buscando_productos(self):
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows=self.conSql().run_query(query,)
        for fila in db_rows:
            self.lista_producto.insert('', 0, text=fila[1], value= (fila[2], fila[3]))


    def agregar(self,event):
        try:
            self.lista_producto.item(self.lista_producto.selection())['text'][0]
        except IndexError :
            mb.showinfo("Error","Selecione un producto para poder agregarlo")
            return
        if self.caja_cantidad_aVender.get() == "":
            mb.showinfo("Error","Dede ingresar la cantidad de producto que desea agregar")
            return
        """l_f=[]
        for ftr in self.factura.get_children():
            l=self.factura.item(ftr)['text']
            l_f.append(l)
        print(l_f)
        filt=self.lista_producto.item(self.lista_producto.selection())['text'][0]
        print()filtro =(filter(lambda x: filt in x,l_f))
       """

        try:
               multiplicandoCantidadDeVeses= int(self.caja_cantidad_aVender.get())

        except  :
                mb.showinfo("Error", "No se aceptan letras ni simbolos")
                self.caja_cantidad_aVender.delete(0,END)
                return

        cur_id = self.lista_producto.focus()
        c_1=int(self.caja_cantidad_aVender.get())
        c_2=int(float(self.lista_producto.item(cur_id)['values'][1]))
        sud_total= int(float(self.lista_producto.item(cur_id)['values'][0])) * c_1

        if c_2 <= 0:
                mb.showinfo("Error","Este producto se a agotado")
                self.caja_cantidad_aVender.delete(0,END)
                return

        if c_1 > c_2:
            r_c=c_1 - c_2
            mb.showinfo("Error","No hay esa cantidad de productos asen falta "+str(r_c)+" "+self.lista_producto.item(cur_id)["text"])
            self.caja_cantidad_aVender.delete(0,END)
            return

        if cur_id:
            pasando_producto= self.lista_producto.item(cur_id)['values'][1]
            pasando_producto1= self.lista_producto.item(cur_id)['values'][0]

            if multiplicandoCantidadDeVeses == 0:
                mb.showinfo("Error","Como sete ocurre que vas agregar un producto ingresando '0'")
                self.caja_cantidad_aVender.delete(0,END)
                return

            self.factura.insert("",0,text=self.lista_producto.item(cur_id)["text"], values=(pasando_producto1,str(multiplicandoCantidadDeVeses),sud_total))
            self.caja_cantidad_aVender.delete(0,END)

        lista=self.lista_producto.item(cur_id)
        dicionario=lista['values']
        dc=dicionario[0]
        dcc=float(dc)
        #SACANDO TOTAL PARA SCROLLTEXT
        total = 0
        for item in self.factura.get_children():
            celda = float(self.factura.set(item, "#1"))
            celda_cantidad=int(self.factura.set(item, "#2"))
            sumas_de_celda= celda * celda_cantidad
            total +=sumas_de_celda
            self.tt_credito=total

        cur_id = self.lista_producto.focus()
        lista=self.lista_producto.item(cur_id)
        dicionario=lista['values']
        b=lista['text']




    def total(self):
        global lista_factura
        print("-----comensando funcion venta----------")
        total = 0

        for item in self.factura.get_children():
            celda = float(self.factura.set(item, "#1"))
            celda_cantidad=int(self.factura.set(item, "#2"))
            sumas_de_celda= celda * celda_cantidad
            print("pasamos")
            total +=sumas_de_celda




        #MOSTRANDO MENSAJE EN ṔANTALLA DEL TOTAL
        total="{0:.2f}".format(total)
        self.result['text'] = 'Total: {}'.format(total)
        self.tt=float(total)



        #CAPTURANDO DATOS DE LA TABLA FACTURA
        ba=self.factura.get_children()
        for child in ba:
            lista_factura=self.factura.item(child)["text"]
            lista_factura_n=self.factura.item(child)["values"]
            l_s_i=lista_factura+" " + str(lista_factura_n[0]+"C$")
            print(l_s_i)
            lis=[]
            a=open('lista','r')
            l=a.read() + ' '+lista_factura
            a.close()
            b=open('lista','w')
            b.write(l)
            b.close()
        #pendiente para saber ubicarla
        """for i in timestampStr:
            str(timestampStr)"""

        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        print("la hora es: "+timestampStr)








        query="SELECT SUM(cantidad) FROM ventas"
        k=self.conSql().run_query(query,).fetchall()[0][0]
        k=str(k)
        file=open("total.txt","w")
        file.write(k)
        file.close()
        fecha=timestampStr
        print(fecha)

        self.convirtiendo_dollar()
        self.InsertandoReristro(v='1')
        if float(total) >= 1:
           self.Ventanaconfirmar_venta(total,timestampStr)

    def Ventanaconfirmar_venta(self,total,timestampStr):
        cf_vt= Toplevel()
        cf_vt.resizable(False, False)
        lb_confirmar_venta= ttk.Label(cf_vt,text="Confirmar Venta")
        lb_confirmar_venta.grid(row=0,column=0,padx=20,pady=5)
        self.lb_total=ttk.Label(cf_vt,text="Total")
        self.lb_total.grid(row=1,column=0,padx=10,pady=5)
        lb_cambio=ttk.Label(cf_vt,text="Cabio de dinero")
        lb_cambio.grid(row=2,column=0,padx=10,pady=5)
        lb_mb_e = Label(cf_vt,text="",fg="red")
        lb_mb_e.grid(row =3,column=1)
        self.caja_cambio= ttk.Entry(cf_vt)
        self.caja_cambio.grid(row=2,column=1,padx=10,pady=5)
        bt_canselar= ttk.Button(cf_vt,text="Canselar",command=lambda:(cf_vt.destroy(), self.limpiar()))
        bt_canselar.grid(row=4,column=0,padx=10,pady=5)
        bt_confirmar= ttk.Button(cf_vt,text="Confirmar",command=lambda :self.Confirmar_venta(total,cf_vt,timestampStr,lb_mb_e))
        bt_confirmar.grid(row=4,column=1,padx=10,pady=5)
        self.lb_total["text"]="Total cordobas: {}   Dollar: {}".format(total,self.Total_en_dolar)

    def Confirmar_venta(self,total,cf_vt,timestampStr,lb_mb_e):
        listap=""
        for item in self.factura.get_children():
            c=self.factura.item(item)["text"]
            d=self.factura.item(item)["values"][0]
            g=self.factura.item(item)["values"][1]
            usr=self.nombre_usr

            hr().RestandoProductoVendido(c,g)
            hr().registro_ventas(c,d,usr)
            rango=slice(3,6)
            clave_producto=c[:4]+self.OctenerFecha()[1][rango]+self.nombre_usr[2]+self.OctenerFecha()[2]
            hr().registro_ventas_hoy(parameters=(self.OctenerFecha()[0],g,self.nombre_usr,c,clave_producto,d))

            g=str(g)
            while len(c) < 30:
                c+=" "
            while len(d) < 12:
                d+=" "
            listap += c+d+g+"\n"
            print("se imprime g",g)
        print(listap,"====")


        if self.caja_cambio.get() == "":
            lb_mb_e['text']="{}".format("Se nesesita que ingrese el cambio")
            return
        try:
          cambio= float(self.caja_cambio.get()) - float(total)
          cambio=cambio="{0:.2f}".format(cambio)
          if float(self.caja_cambio.get()) < float(total):
             lb_mb_e['text']="{}".format("Error el pago es menor al total de los productos")
             return
        except:
            lb_mb_e['text']="{}".format("No se admiten letras")
            self.caja_cambio.delete(0,END)
            return

        """ query='INSERT INTO ventas(fecha,cantidad,vtusr,producto,clave_producto,presio) VALUES(?,?,?,?,?,?)'
        self.conSql().run_query(query,parameters)"""

        #La condicion if esta para asegurar que no se valla acrear un archivo de registro cuando se reinicie la funcion total
        if float(total) > 0:


           pago="{0:.2f}".format(float(self.caja_cambio.get()))

           parametros=(listap,total,pago,str(cambio),str(g))
           hr().ch(parametros,ur=self.nombre_usr,)
        #este es el registro permanente

        cf_vt.destroy()
        mb.showinfo("Exito","El vuelto es: "+str(cambio))
        self.octener_productos()
        self.limpiar()
        self.ProductosApuntoAgotarse()
        self.IenTdetalles_ventas()

        with open("total.txt","r") as archivo:
          for linea in archivo:
             linea=float(linea)
             linea="{0:.2f}".format(linea)
             self.hoy['text'] = 'Total de hoy: {}'.format(linea)
             return



    def TotalVentasD(self):
        query="SELECT fecha FROM ventas"

        try:
            ff=self.conSql().run_query(query,).fetchall()[0]
            try:
              query="SELECT SUM(cantidad) FROM ventas"
              aa=self.conSql().run_query(query,).fetchall()[0]
              dateTimeObj = datetime.now()
              timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
              fecha=timestampStr.split()[0]

              with open("totalHoy","w") as f:
                  fj=ff[0]
                  gg=fj.split()[0]
                  print("igual "+fecha)
                  print("igual "+gg)
                  print("arriba")
                  listando=[gg,aa]
                  lis=str(listando)
                  time=str(fecha)
                  com=lis[0]
                  f.write(lis)
            except:print("error")
        except :print("Error")



    def buscar(self):

        octener_datos=self.caja_buscar.get() + "%"
        print(octener_datos)
        parameters=(octener_datos,)
        #query='SELECT * FROM product WHERE name like = ?'
        query='SELECT * FROM product WHERE name LIKE  ?'

        bqd=self.conSql().run_query(query,parameters)
        #bqd=self.cn().buscar_producto(parameters,)

        #Limpiando la tabla
        records= self.lista_producto.get_children()
        for elementos in records:
            self.lista_producto.delete(elementos)

        for fila in bqd:
            self.lista_producto.insert('', 0, text=fila[1], value= (fila[2], fila[3]))
        if octener_datos == "":
            self.octener_productos()
            print("nos vamos a ver al mago")





    def limpiar(self):
        self.factura.delete(*self.factura.get_children())
        print("exito")
        self.total()
        self.result_dolar['text']='Total Dollars: {}'.format(0)



    def credito_agregar(self):
        query="SELECT nombre,apellido from credito"
        datos=self.conSql().run_query(query,).fetchall()
        self.vt_credito= Toplevel()
        self.text_elegir_user=Label(self.vt_credito,text="Elige un cliente").grid(row=0,column=0)
        self.caja_clientes= ttk.Combobox(self.vt_credito,values=datos)
        self.caja_clientes.grid(row=0,column=1,padx=10,pady=10)
        self.bt_Dar_credito=Button(self.vt_credito,text="Darle credito",command=self.DarleCredito)
        self.bt_Dar_credito.grid(row=1,column=1,padx=10,pady=10)
        self.vt_credito.mainloop()

    def DarleCredito(self):
        #try:
           listap=""
           p=self.caja_clientes.get()
           p=p.split()
           nombre=p[0]
           apellido=p[1]
           query="SELECT * FROM credito where nombre=? and apellido=?"
           trallendo_deuda1=self.conSql().run_query(query,parameters=(nombre,apellido)).fetchall()[0][5]

           for item in self.factura.get_children():
               c=self.factura.item(item)["text"]
               b=self.factura.item(item)["values"][0]
               g=self.factura.item(item)["values"][1]
               hr().RestandoProductoVendido(c,g)
               prueba="10"
               query="INSERT INTO product_en_creditos(nombre,precio,fecha,codigo_cliente,cantidad) VALUES(?,?,?,?,?)"
               d=self.OctenerFecha()[0]

               e=trallendo_deuda1
               parameters=(c,b,d,e,g)
               self.conSql().run_query(query,parameters)
               listap += c+", "
           print(listap,"====")

           deuda=9
           query="SELECT * FROM credito where nombre=? and apellido=?"
           trallendo_deuda=self.conSql().run_query(query,parameters=(nombre,apellido))
           tr=[]
           tr=trallendo_deuda.fetchall()[0]
           tr=tr[4]
           print(tr)
           sumando_deuda=tr + self.tt_credito
           #hr().registroCredito(listap,nombre,apellido)
           print(apellido)
           parameters=(sumando_deuda,nombre,apellido)
           #self.run_query(query,)
           query="UPDATE credito SET deuda =? where nombre=? and apellido= ?"
           self.conSql().run_query(query,parameters)
           self.octener_productos_tabla_credito()
           self.vt_credito.destroy()
           mb.showinfo("Exito","Sele a dado el cridito a: "+"("+nombre+")")
           self.octener_productos()
           self.limpiar()

        #except: mb.showinfo("Error","No selepudo dar credito a: "+"("+nombre+")")





    def QuitarProducto(self):
        try:
          selecsionar_item= self.factura.selection()[0]
          self.factura.delete(selecsionar_item)
        except:
            mb.showinfo("Error","Selecione el producto que quiere quitar de la factura")





#--------------------------------------------------------------------------------------------------------------------

                      #AQUI INICIA LAS FUNCIONES QUE CONTRULLEN LA INTERFAS
#_____________________________________________________________________________________________________________________


    def consulta_por_codigo(self):
        #CREANDO FRAME
        self.pagina1=ttk.Frame(self.cuaderno1)

        #MENSAJE CUANTO ESTA EL DOLAR
        #self.lb_dolar= Label(self.pagina1,text="Dollar=").grid(row=0,column=0,columnspan=2)

        self.cuaderno1.add(self.pagina1, text="Carga de artículos")
        navidad_f= self.OctenerFecha()[1]
        navidad_f=navidad_f.replace("-"," ")
        navidad_f=navidad_f.split()
        print("sacando navidaad", navidad_f)
        if navidad_f[1] == "12":
           lb_navidad= Label(self.pagina1,text="Feliz navidad",fg=color_verde,font=("Arial", 25) ).grid(row=0,column=0,pady=0)
           self.style.configure('Treeview.Heading', background=color_verde)

        #_______________________________________________________________________________________________
        #_________________LABELFRAME-1__________________________________________________________________
        self.labelframe1=LabelFrame(self.pagina1, text="Artículo")
        self.labelframe1.grid(column=0, row=1, padx=20)

        #TABLA |Lista de productos
        self.lista_producto=ttk.Treeview(self.labelframe1,height=18,columns=("#0", "#1"))
        self.lista_producto.heading('#0',text='Nombre',anchor= CENTER)
        self.lista_producto.heading('#1',text='Presio',anchor=CENTER)
        self.lista_producto.heading('#2',text='cantidad',anchor=CENTER)
        self.lista_producto.column("#0",width=400)
        self.lista_producto.column("#1",width=80)
        self.lista_producto.column("#2",width=80)
        self.lista_producto.grid(row=0,column=0,padx=20,pady=10,sticky=W+E,columnspan=4)
        self.lista_producto.bind('<Double-Button-1>',self.agregar)
        #CAJA |BUSCAR
        if self.usr== "root":
          self.caja_buscar=ttk.Entry(self.labelframe1,textvariable=self.buscar)
          self.caja_buscar.grid(column=0, row=1, sticky=W+E,columnspan=3)
        elif self.usr != "root":
            self.caja_buscar=ttk.Entry(self.labelframe1,textvariable=self.buscar)
            self.caja_buscar.grid(column=0, row=1, sticky=W+E,columnspan=4)


        #BOTON |BUSCAR
        if self.usr == "root":
          self.bt_buscar =ttk.Button(self.labelframe1,text="🔍",command=self.buscar,style = 'W.TButton')
          self.bt_buscar.grid(column=3,row=1,sticky=W+E,columnspan=1)
        elif self.usr != "root":
            self.bt_buscar =ttk.Button(self.labelframe1,text="🔍",command=self.buscar,style = 'W.TButton')
            self.bt_buscar.grid(column=0,row=2,sticky=W+E,columnspan=4)


        #MENSAJE |PRODUCTO BORRADO
        """self.message = ttk.Label(self.labelframe1,text = '')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)"""



        #______________________________________________________________________________________________
        #____________________END____________FRAME-1____________________________________________________



        #_______________________________________________________________________________________________
        #_________________LABELFRAME-2__________________________________________________________________
        self.labelframe2=LabelFrame(self.pagina1,text="Facturar productos")
        self.labelframe2.grid(column=1, row=1)

        #TABLA FACTURA
        self.factura=ttk.Treeview(self.labelframe2,height=18, column=("#0",2,3))
        self.factura.heading('#0',text='Nombre',anchor= CENTER)
        self.factura.column('#1',width=100)
        self.factura.heading('#1',text='Presio',anchor=CENTER)
        self.factura.column("#2",width=80)
        self.factura.heading('#2',text='Cantidad',anchor=CENTER)
        self.factura.heading('#3',text='Sub total',anchor=CENTER)
        self.factura.column("#3",width=80)
        self.factura.grid(row=1,column=0,padx=20,pady=10,columnspan=3)


        self.bt_quitar=ttk.Button(self.labelframe2,text="Quitar",command=self.QuitarProducto)
        self.bt_quitar.grid(row=3,column=1,sticky=W+E,columnspan=2)
        self.bt_vender=ttk.Button(self.labelframe2,text="Vender",command=self.total)
        self.bt_vender.grid(row=6,column=1,sticky=W + E,columnspan=2)

        #MENSAJE TOTAL
        self.result = Label(self.labelframe2, text='Total: 0',fg="#0091ff",font=20)
        self.result.grid(row=2,column=2)

        self.result_dolar = Label(self.labelframe2, text='Total Dollar: 0',fg="#1c6e35",font=20)
        self.result_dolar.grid(row=2,column=1)                                            #TOTAL DE LAS VENTAS

        self.hoy=Label(self.labelframe2,text="Ventas de hoy: ",font=20,fg='#3f9592')
        self.hoy.grid(row=2,column=0)

        #CAJA |NUMERO DE VESES
        self.caja_cantidad_aVender=ttk.Entry(self.labelframe2)
        self.caja_cantidad_aVender.grid(row=3,column=0,sticky=W + E,columnspan=1)


        #BOTON |CREDITO
        self.bt_credito= ttk.Button(self.labelframe2,text="Dar en credito",command=self.credito_agregar)
        self.bt_credito.grid(row=6,column=0,sticky=W+ E,columnspan=1)
        self.octener_productos()






        #______________________________________________________________________________________________
        #____________________END____________FRAME-2____________________________________________________

####################################################################################################
############### INSERTAR PRODUCTO ##################################################################
####################################################################################################
    def LimpiandoCajasInsertar(self):
        self.caja_nombre.delete(0, END)
        self.caja_precio.delete(0, END)
        self.caja_cantidad.delete(0, END)
        self.caja_porcentage.delete(0, END)
        self.caja_fechaVencimiento.delete(0, END)
        self.caja_mes_antelacion_d.delete(0, END)
        self.caja_descuento.delete(0, END)
        self.caja_cantidadxmallor.delete(0,END)
    def MostrarProductos(self):
        query= "select * from product"
        datos=self.conSql().run_query(query).fetchall()
        records= self.tabla_detalles_producto.get_children()
        for elementos in records:
            self.tabla_detalles_producto.delete(elementos)

        for x in datos:
          self.tabla_detalles_producto.insert("",0,text=x[1],value=(x[2],int(x[3]),x[4],x[6],x[7],x[8]))

    def ProductosApuntoAgotarse(self):
        query="Select name,cantidad from product WHERE cantidad < 10"
        dato=conSql().run_query(query,).fetchall()
        recorrer=self.tabla_detalles_producto.get_children()
        for r in recorrer:
            self.tabla_detalles_producto.delete(r)
        for d in dato:
           self.tabla_detalles_producto.insert("",END,text=d[0],values=('',d[1],))
    def MostrarProductosApuntoDeVenser(self):

        query="Select name,cantidad from product WHERE cantidad < 10"
        dato=conSql().run_query(query,).fetchall()
        recorrer=self.tabla_detalles_producto.get_children()
        for r in recorrer:
            self.tabla_detalles_producto.delete(r)
        for d in dato:
           self.tabla_detalles_producto.insert("",END,text=d[0],values=('',d[1],))


    def MirandoQueProductoSeEstanPorCaducar(self):
     try:
      query="SELECT  name,fecha_vencimiento,fechaDeAlertaVencimiento FROM  product"
      contando=1
      datoss=self.conSql().run_query(query).fetchall()
      recoriendo=self.tabla_detalles_producto.get_children()
      for r in recoriendo:
            self.tabla_detalles_producto.delete(r)
      for datos in datoss:

        fechaActual= self.OctenerFecha()[1]
        fechaAlerta=datos[2]
        fechaVencimiento=str(datos[1])
        print("imprimiendo fechavenciomiuento",fechaVencimiento)
        fvr=str(fechaVencimiento.replace("/"," "))
        fvrl=fvr.split()
        far=str(fechaActual.replace("-"," "))
        farl=far.split()
        print("pr",fvrl,"se",farl)
        if fvrl[2] >= farl[2] :
           if fvrl[2] == farl[2]:
              r=int(fvrl[1])-int(farl[1])
              c=r-int(fechaAlerta)
              if c <= int(fechaAlerta):
               print(c)
               print("este producto esta apunto de llegar al mpounto de nodevolucion",datos[0])
               self.tabla_detalles_producto.insert("",END,text=datos[0],values=('','',datos[1],))
           elif fvrl[2] > farl[2]:
                r=12-int(farl[1])
                f=r+ int(fvrl[1])
                if f <= int(fechaAlerta):
                  print("el producto esta por venser",datos[0])
                  self.tabla_detalles_producto.insert("",END,text=datos[0],values=('','',datos[1],))
                print(f)

        elif fvrl[2]< farl[2]:
            self.tabla_detalles_producto.insert("",END,text=datos[0],values=('','',datos[1],))
            print("sele fue")

        else:print("errp")
     except:
         mb.showinfo("Error","Algo salio mal")



    def RadioButonProductos(self):
        if self.selecion.get() == 0:
            self.MostrarProductos()
        elif self.selecion.get() ==1:
            self.MirandoQueProductoSeEstanPorCaducar()
        elif self.selecion.get() ==2:
            self.ProductosApuntoAgotarse()
        else:print("opcion invalida")


    def validacion(self):
        return len(self.caja_nombre.get()) !=0 and len(self.caja_precio.get()) !=0 and len(self.caja_cantidad.get()) !=0 and len(self.caja_porcentage.get()) !=0

    def sumar_porcentage(self):
        if self.caja_nombre.get() == "" or self.caja_precio.get() == "" or self.caja_cantidad.get() == "" or self.caja_porcentage.get()== "":
            mb.showinfo("Error","No puede insertar nuevo producto si no inserta (nombre precio cantida y porsentaje)")
            return
        try:
            float(self.caja_precio.get())
            int(self.caja_cantidad.get())
            int(self.caja_porcentage.get())
            int(self.caja_descuento.get())
        except:
            mb.showinfo("Error","En la caja (precio, cantidad, porsentaje solo se admiten numeros")
            return
        if len(self.caja_fechaVencimiento.get()) != 10:
            mb.showinfo("Error","En la fecha debe ingresar 10 caracteres ni uno menos ni uno mas")
            return
        cantidad_sin_g=float(self.caja_precio.get())
        precio=float(self.caja_precio.get())

        porcentage1=float(self.caja_porcentage.get())
        porcentage=porcentage1 / 100 * precio
        print(porcentage)
        precio=precio+porcentage
        print(precio)

        if self.validacion():
           parameters=(self.caja_nombre.get(),precio,self.caja_cantidad.get(),self.caja_fechaVencimiento.get(),cantidad_sin_g,self.caja_mes_antelacion_d.get(),self.caja_descuento.get(),self.caja_cantidadxmallor.get())
           query = "insert into product values(NULL, ?, ?, ?, ?, ?, ?,?,?)"
           self.conSql().run_query(query,parameters)
           mb.showinfo("Exito✅", "Sea guardado en la base de datos "+"("+self.caja_nombre.get()+")")
           self.LimpiandoCajasInsertar()

        else:
           mb.showinfo("Error🚫", "El nombre el precio y la cantidad son requeridos")
           return
        self.octener_productos()
        self.MostrarProductos()

    def edit_product(self,event):
        self.var= 2
        try:
            self.tabla_detalles_producto.item(self.tabla_detalles_producto.selection())['values'][0]
        except IndexError as e:
            mb.showinfo("Error🚫","Porfavor selecione un producto")
            return
        self.nameA = self.tabla_detalles_producto.item(self.tabla_detalles_producto.selection())['text']
        datos = self.tabla_detalles_producto.item(self.tabla_detalles_producto.selection())['values']

        self.LimpiandoCajasInsertar()

        self.caja_nombre.insert(0,self.nameA)
        self.caja_precio.insert(0,datos[0])
        self.caja_cantidad.insert(0,datos[1])
        self.caja_fechaVencimiento.insert(0,datos[2])
        self.caja_mes_antelacion_d.insert(0,datos[3])
        self.caja_descuento.insert(0,datos[4])

        self.bt_porcentage["text"]="{}".format("Actualizar")



        #Button(self.edit_wind, text = 'Actualisar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price,new_cantidad.get(),cantidad_vieja,lb_error)).grid(row = 7, column = 2, sticky = W)

    def edit_records(self):
        if self.caja_precio.get() == "0":
            mb.showinfo("Error","El presio que estas poniendo es igual a 0 no puedes regalar el producto")
            return
        try:
            float(self.caja_precio.get())
            int(self.caja_cantidad.get())
        except:
            mb.showinfo("Error","No se acetan letras ni simbolos")
            return


        query = 'UPDATE product SET name = ?, price=?, cantidad=?,fecha_vencimiento=?,mesProximoDevovlucion=?,descuento=?,cantidad_xmayor=? WHERE name = ?'
        parameters = (self.caja_nombre.get(),self.caja_precio.get(),self.caja_cantidad.get(),self.caja_fechaVencimiento.get(),self.caja_mes_antelacion_d.get(),self.caja_descuento.get(),self.caja_cantidadxmallor.get(),self.nameA)
        self.conSql().run_query(query, parameters)
        mb.showinfo("Exito✅",self.nameA+" Se a actualisado")
        self.bt_porcentage["text"]="{}".format("Insertar")
        self.var=1
        self.LimpiandoCajasInsertar()
        self.octener_productos()
        self.MostrarProductos()

    def delete_product(self):

        try:
           self.tabla_detalles_producto.item(self.tabla_detalles_producto.selection())['text'][0]
        except IndexError as e:
            mb.showinfo("Error🚫","Porfavor Selecione Un Producto")
            return

        name = self.tabla_detalles_producto.item(self.tabla_detalles_producto.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.conSql().run_query(query, (name, ))
        mb.showinfo("Exito✅","El farmaco se a borrado")
        self.octener_productos()
        self.MostrarProductos()
    def BuscarProductoEnAdministrarP(self):
        octener_datos=self.caja_buscar2.get() + "%"
        print(octener_datos)
        parameters=(octener_datos,)
        #query='SELECT * FROM product WHERE name like = ?'
        query='SELECT * FROM product WHERE name LIKE  ?'

        bqd=self.conSql().run_query(query,parameters)
        #bqd=self.cn().buscar_producto(parameters,)

        #Limpiando la tabla
        records= self.tabla_detalles_producto.get_children()
        for elementos in records:
            self.tabla_detalles_producto.delete(elementos)

        for fila in bqd:
            self.tabla_detalles_producto.insert('', 0, text=fila[1], value= (fila[2], fila[3]))
        if octener_datos == "":
            self.tabla_detalles_producto()
            print("nos vamos a ver al mago")





    def insertar_producto(self):
        self.pagina2= ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2,text="Administrar Productos")
        self.labelframe1=ttk.Labelframe(self.pagina2,text="Consultar producto")
        self.labelframe1.grid(row=1,column=0,padx=200,pady=10)
        self.labelframe2=ttk.Labelframe(self.pagina2,text="INGRSE NUEVO PRODUCTO")
        self.labelframe2.grid(row=0,column=0,padx=20,pady=10)

        self.tabla_detalles_producto=ttk.Treeview(self.labelframe1,height=12,column=('#1','#2','#3','#4','#5','#6'))
        self.tabla_detalles_producto.grid(row=0,column=0,columnspan=5)
        self.tabla_detalles_producto.column('#0',width=160)
        self.tabla_detalles_producto.column('#1',width=100)
        self.tabla_detalles_producto.column('#2',width=100)
        self.tabla_detalles_producto.column('#3',width=100)
        self.tabla_detalles_producto.column('#3',width=100)
        self.tabla_detalles_producto.column('#4',width=120)
        self.tabla_detalles_producto.column('#5',width=80)
        self.tabla_detalles_producto.column('#6',width=120)

        self.tabla_detalles_producto.heading('#0',text="Nombre producto",anchor=CENTER)
        self.tabla_detalles_producto.heading('#1',text="Precio",anchor=CENTER)
        self.tabla_detalles_producto.heading('#2',text="Cantidad",anchor=CENTER)
        self.tabla_detalles_producto.heading('#3',text="Fecha de vencimiento",anchor=CENTER)
        self.tabla_detalles_producto.heading('#4',text="Alerta vencimiento",anchor=CENTER)
        self.tabla_detalles_producto.heading('#5',text="%Descuento",anchor=CENTER)
        self.tabla_detalles_producto.heading('#6',text="Cantidad X Mayor",anchor=CENTER)
        self.tabla_detalles_producto.bind('<Double-Button-1>',self.edit_product)
        self.selecion=IntVar()
        self.caja_buscar2=ttk.Entry(self.labelframe1)
        self.caja_buscar2.grid(row=1,column=0,sticky=W+E,columnspan=4,padx=0)
        self.bt_buscar2 =ttk.Button(self.labelframe1,text="🔍",command=self.BuscarProductoEnAdministrarP,style = 'W.TButton')
        self.bt_buscar2.grid(row=1,column=4,columnspan=1,sticky=W+E)
        #BOTON |BORRAR
        self.bt_borrar=ttk.Button(self.labelframe1,text="Borrar 🗑", command=self.delete_product)
        if self.usr=="root":
          self.bt_borrar.grid(row=2,column=4,columnspan=1,sticky=W+E)
        self.rdb_mostrarproductos=ttk.Radiobutton(self.labelframe1,text="Todos los productos",value=0,variable=self.selecion,command=self.RadioButonProductos)
        self.rdb_mostrarproductos.grid(row=2,column=0,)
        self.rdb_mostrarproductosVensidos=ttk.Radiobutton(self.labelframe1,text="Productos vencidos",value=1,variable=self.selecion,command=self.RadioButonProductos)
        self.rdb_mostrarproductosVensidos.grid(row=2,column=1,)
        self.rdb_mostrarproductosAgotados=ttk.Radiobutton(self.labelframe1,text="Productos Agotados",value=2,variable=self.selecion,command=self.RadioButonProductos)
        self.rdb_mostrarproductosAgotados.grid(row=2,column=2,)




        self.lb_nombre= ttk.Label(self.labelframe2,text="Nombre")
        self.lb_nombre.grid(row=0,column=0,padx=50, pady=10)
        self.caja_nombre = ttk.Entry(self.labelframe2)
        self.caja_nombre.grid(row=0,column=1,padx=40)
        #PRECIO


        self.lb_precio= ttk.Label(self.labelframe2,text="Precio")
        self.lb_precio.grid(row=0,column=2,padx=50, pady=10)
        self.caja_precio = ttk.Entry(self.labelframe2)
        self.caja_precio.grid(row=0,column=3)
        #CANTIDAD


        self.lb_cantidad= ttk.Label(self.labelframe2,text="Cantidad")
        self.lb_cantidad.grid(row=0,column=4,padx=0, pady=10)
        self.caja_cantidad = ttk.Entry(self.labelframe2)
        self.caja_cantidad.grid(row=0,column=5)

        #porcentage

        self.lb_porcentage=ttk.Label(self.labelframe2,text="Igresar porcentage")
        self.lb_porcentage.grid(row=1,column=0,padx=10, pady=10)
        self.caja_porcentage=ttk.Entry(self.labelframe2)
        self.caja_porcentage.grid(row=1,column=1)

        self.lb_fechaVencimiento= ttk.Label(self.labelframe2,text="Ingrese fecha vencimiento")
        self.lb_fechaVencimiento.grid(row=1,column=2,padx=20)
        self.caja_fechaVencimiento=ttk.Entry(self.labelframe2)
        self.caja_fechaVencimiento.grid(row=1,column=3)

        #BOTON | MENSAJE DE ALERTA
        self.lb_mes_antelacion_d= ttk.Label(self.labelframe2,text="Mes proximo devolucion")
        self.lb_mes_antelacion_d.grid(row=1,column=4,pady=10)
        self.caja_mes_antelacion_d = ttk.Entry(self.labelframe2)
        self.caja_mes_antelacion_d.grid(row=1,column=5)
        self.estado_boton=0

        #DESCUENTO
        self.lb_descuento= ttk.Label(self.labelframe2,text="Porsentaje de descuento")
        self.lb_descuento.grid(row=2,column=0,pady=10)
        self.caja_descuento = ttk.Entry(self.labelframe2)
        self.caja_descuento.grid(row=2,column=1)

        #CANTIDAD X MAYOR
        self.lb_cantidadxmayor= ttk.Label(self.labelframe2,text="Cantidad x MaYor")
        self.lb_cantidadxmayor.grid(row=2,column=2,pady=10)
        self.caja_cantidadxmallor = ttk.Entry(self.labelframe2)
        self.caja_cantidadxmallor.grid(row=2,column=3)

        #BOTON |INSERTAR

        self.var=1
        self.bt_porcentage =ttk.Button(self.labelframe2,text="Insertar",command= self.deside)
        self.bt_porcentage.grid(row=2,column=4,pady=20)
    def deside(self):
        if self.var ==1 :
            self.sumar_porcentage()
        elif self.var ==2:
            self.edit_records()
        else:print("la variable cambio",self.var)



        #mensaje
        self.message =tk.Label(text= '', fg='white')
        self.message.grid(row=6, column =0,columnspan=2, sticky= W + E)
        self.octener_productos()


####################################################################################################
############### REGISTRO ###########################################################################
####################################################################################################

    def insertando_datos_archivos(self,vrb):
        nombrearch=self.t.focus()
        dicionario=self.t.item(nombrearch)['text']
        print(dicionario)
        #j=str(dicionario)
        if vrb == '1':
          f=open("registro/facturas/"+dicionario,"r",encoding='UTF-8')
        elif vrb == '2':
            f=open("registro/credito/"+dicionario,"r",encoding='UTF-8')
        v=f.read()
        print(v)
        f.close()
        self.scrolledtext1.delete("1.0", "2000.0")
        self.scrolledtext1.insert("1.0",v)



    def registro(self ):
        #CREANDO FRAME
        self.pagina3= ttk.Frame(self.cuaderno1)
        #CREANDO LABELFRAME
        self.labelframe1= ttk.Labelframe(self.pagina3,text="Ventas")
        self.labelframe1.grid(row=0,column=0,padx=60,pady=20)
        self.labelframe2= ttk.Labelframe(self.pagina3,)
        self.labelframe2.grid(row=0,column=1,padx=10,pady=20)
        self.cuaderno1.add(self.pagina3,text="Registro")


        self.scrolledtext1=st.ScrolledText(self.labelframe2, width=80, height=23)
        self.scrolledtext1.grid(row=0,column=1)
        self.t= ttk.Treeview(self.labelframe1,height=17)
        self.t.column("#0",width=220)
        self.t.heading("#0",text="Registro",anchor=CENTER)


        self.t.grid(row=0,column=0,padx=20,columnspan=2)
        variableRB=StringVar()
        self.radiobuton_f=Radiobutton(self.labelframe1,text="factura",variable=variableRB,value=1,command=lambda :self.InsertandoReristro(v=variableRB.get())).grid(row=2,column=0,padx=0)
        self.radiobuton_C=Radiobutton(self.labelframe1,text="credito",variable=variableRB,value=2,command=lambda :self.InsertandoReristro(v=variableRB.get())).grid(row=2,column=1,padx=0)
        boton= ttk.Button(self.labelframe2,text="Abrir",command=lambda :self.insertando_datos_archivos(vrb=variableRB.get()))
        boton.grid(row=2,column=1,sticky=W+E)

    def InsertandoReristro(self,v):

        records= self.t.get_children()
        for elementos in records:
         self.t.delete(elementos)
        try:
          if v== '1':
             self.b=os.listdir("/home/elisa/Documentos/farmaciaSoluciones/registro/facturas")
          elif v == '2':
             self.b=os.listdir("/home/elisa/Documentos/farmaciaSoluciones/registro/credito")
        except:
           if v== '1':
             self.b=os.listdir("/home/lord_ader/Prollectos/Python/farmaciaSoluciones/registro/facturas")
           elif v == '2':
             self.b=os.listdir("/home/lord_ader/Prollectos/Python/farmaciaSoluciones/registro/credito")

        for fila in self.b:
            pass
            self.t.insert("",0,text=fila)




####################################################################################################
############### CREDITO ############################################################################
####################################################################################################

    def validacion_credito(self):
        return  len(self.caja_nombre_credito.get()) !=0 and len(self.caja_apellido.get()) !=0 and len(self.cb_sexo.get()) !=0


    def insertar_credito(self):
        if self.validacion_credito():
            self.deuda='0'

            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            fecha=timestampStr.split()[0]

            codigo_cli=self.caja_nombre_credito.get()[0]+self.caja_apellido.get()[0]+self.cb_sexo.get()[0]+fecha
            print(codigo_cli)
            datos_creditos=(self.caja_nombre_credito.get(),self.caja_apellido.get(),self.cb_sexo.get(),self.deuda,codigo_cli)
            query = "insert into credito(nombre,apellido,sexo,deuda,codigo) values(?, ?,?,?,?)"
            parameters=datos_creditos
            self.conSql().run_query(query,parameters)
            mb.showinfo("Exito✅", "Los datos fueron insertados").format(self.caja_nombre_credito.get())
            self.caja_nombre_credito.delete(0, END)
            self.caja_apellido.delete(0, END)
            self.cb_sexo.delete(0, END)
            #DESTRULLENDO COGIGO PARA VOLVER A CARGARLO
            self.consulta_por_codigo()

        else:
            mb.showinfo("Alerta", "El nombre el apellido y el sexo son requeridos")
        self.octener_productos_tabla_credito()


    def octener_productos_tabla_credito(self):
        #linpiando la tabla
        records= self.tabla_credito.get_children()
        for elementos in records:
            self.tabla_credito.delete(elementos)
        query='SELECT * FROM credito ORDER BY nombre DESC'
        self.db_rows=self.conSql().run_query(query)

        for fila in self.db_rows:
            self.tabla_credito.insert('',0, text=fila[1], value= (fila[2],fila[4]))


    def tabla_Cliente(self):
        #linpiando la tabla
        records= self.tabla_cliente.get_children()
        for elementos in records:
            self.tabla_cliente().delete(elementos)
        query='SELECT * FROM credito ORDER BY nombre DESC'
        self.db_rows=self.conSql().run_query(query,)
        for fila in self.db_rows:
            self.tabla_cliente.insert('',0, text=fila[1], value= (fila[2],fila[4]))






    def saldarDeuda(self):
        try:
           self.tabla_credito.item(self.tabla_credito.selection())["values"][1]
        except IndexError as e:
            mb.showinfo("Error🚫", "Selecione a un deudor")
            return
        deudor=self.tabla_credito.item(self.tabla_credito.selection())["values"][1]
        nombre=self.tabla_credito.item(self.tabla_credito.selection())["text"]
        apellido=self.tabla_credito.item(self.tabla_credito.selection())["values"][0]

        self.pagar_deuda= Toplevel()
        print(apellido)
        self.pagar_deuda.title("Pagar deuda")

        #DEUDA
        Label(self.pagar_deuda,text="Nombre").grid(row=0,column=0,padx=10,pady=5)
        Entry(self.pagar_deuda,textvariable=StringVar(self.pagar_deuda,value=nombre),state="readonly").grid(row=0,column=1,padx=10)

        Label(self.pagar_deuda,text="Deuda").grid(row=1,column=0,padx=10,pady=5)
        Entry(self.pagar_deuda,textvariable=StringVar(self.pagar_deuda,value=deudor),state="readonly").grid(row=1,column=1,padx=10)


        #PAGO
        Label(self.pagar_deuda,text="Pagar$").grid(row=2,column=0,padx=10,pady=5)
        ppago=ttk.Entry(self.pagar_deuda)
        ppago.grid(row=2,column=1,padx=10)
        ttk.Button(self.pagar_deuda, text="Aceptar", command=lambda : self.Pago(nombre,apellido,deudor,ppago.get())).grid(row=3, column=1, sticky=W,padx=5)

    def Pago(self,nombre,apellido,deudor,ppago):
        pg=float(ppago)
        dud=float(deudor)
        resta= dud-pg
        if resta < 0:
            resta=resta=0
        if dud == 0:
            self.pagar_deuda.destroy()
            mb.showinfo('Error','El cliente no debe nada')
            return
        resta='{0:.2f}'.format(resta)
        print(resta,apellido)
        query = "UPDATE credito SET deuda =? where nombre=? and apellido= ?"
        parameters=(resta,nombre,apellido)
        self.conSql().run_query(query,parameters)
        self.pagar_deuda.destroy()
        mb.showinfo("Exito✅","Se a saldado la cuenta")
        self.octener_productos_tabla_credito()
        query="select codigo from credito where nombre =? and apellido= ?"
        trallendo_nombre=self.conSql().run_query(query,parameters=(nombre,apellido)).fetchall()[0][0]
        query="select nombre,precio from product_en_creditos where codigo_cliente = ?"
        trallendo_datos=self.conSql().run_query(query,parameters=(trallendo_nombre,)).fetchall()
        usr=self.nombre_usr

        hr().registroCredito(trallendo_datos,parametros=(nombre,apellido,usr,dud,pg,resta,trallendo_nombre))





    def AbrirListaProductosFiados(self):
        n=self.tabla_credito.focus()
        m=self.tabla_credito.item(n)['text']
        p=self.tabla_credito.item(n)['values'][0]
        query="SELECT * from credito where nombre=? and apellido =?"
        dato=self.conSql().run_query(query,parameters=(m,p)).fetchall()[0][5]
        query="SELECT * from product_en_creditos where codigo_cliente =?"
        dato2=self.conSql().run_query(query,parameters=(dato,)).fetchall()
        self.OctenerListaCredito(dato2)

    def OctenerListaCredito(self,dato2):
        #linpiando la tabla
        records= self.tabla_informacion_c.get_children()
        for elementos in records:
            self.tabla_informacion_c.delete(elementos)

        for fila in dato2:
            self.tabla_informacion_c.insert('',0, text=fila[1], value= (fila[2],fila[5],fila[3]))

    def BorrarCliente(self):
        n=self.tabla_credito.focus()
        m=self.tabla_credito.item(n)['text']
        p=self.tabla_credito.item(n)['values'][0]
        query="DELETE from credito where nombre=? and apellido =?"
        self.conSql().run_query(query,parameters=(m,p))
        self.octener_productos_tabla_credito()








    def credito(self):
        #CRANDO FRAME CREDITO
        self.pagina4= ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina4,text="Credito")

        #_____________________________________________________________________________________
        #____________________CREANDO LABELFRAME-1_____________________________________________
        self.labelframe1= LabelFrame(self.pagina4,text="Lista de personas con credito")
        if self.usr== "root":
            self.labelframe1.place(x=50,y=120)
            #self.labelframe1.grid(column=0, row=1,padx=20,pady=20)
        elif self.usr != "root":
            self.labelframe1.grid(column=0, row=0,padx=20,pady=20)
        #TABLA |CREDITO
        self.tabla_credito= ttk.Treeview(self.labelframe1,height=15,column=("#0","1"))
        self.tabla_credito.grid(row=0,column=0,padx=0,pady=5,columnspan=2)
        self.tabla_credito.heading("#0",text="Nombre",anchor=CENTER)
        self.tabla_credito.heading("#1",text="Apellido",anchor=CENTER)
        self.tabla_credito.heading("#2",text="Deuda",anchor=CENTER)
        self.tabla_credito.column("#2",width=80)

        #BOTON |SALDAR_DEUDA
        if self.usr == "root":
          bt_borrar_cliente= Button(self.labelframe1,text="Borrar cliente",command=self.BorrarCliente).grid(row=1,column=0,sticky=W+E)
          bt_saldar_deuda= Button(self.labelframe1,text="Saldar deuda",command=self.saldarDeuda).grid(row=1,column=1,sticky=W+E)
        else: bt_saldar_deuda= Button(self.labelframe1,text="Saldar deuda",command=self.saldarDeuda).grid(row=1,column=0,sticky=W+E,columnspan=2)


        #___________________________________________________________________________________________
        #_______________END___LABELFRAME-1__________________________________________________________


        #_____________________________________________________________________________________
        #____________________CREANDO LABELFRAME-2_____________________________________________
        self.labelframe2= ttk.Labelframe(self.pagina4,text="Insertar nuevo ¡Cliente!")
        """esta condicion es para que solo el usuario root le aparesca el frame de insertar nuevo cliente"""
        if self.usr == "root":
          self.labelframe2.place(x=50,y=20)
        #LABEL NOMBRE
        self.lb_nombre=ttk.Label(self.labelframe2,text="Nombre")
        self.lb_nombre.grid(column=0,row=0,padx=20,pady=5)
        #CAJA NOMBRE
        self.caja_nombre_credito=ttk.Entry(self.labelframe2)
        self.caja_nombre_credito.grid(row=0,column=1)

        #LABEL APELLIDO
        self.lb_apellido=ttk.Label(self.labelframe2,text="Apellido")
        self.lb_apellido.grid(column=2,row=0,pady=5)
        #CAJA APELLIDO
        self.caja_apellido=ttk.Entry(self.labelframe2)
        self.caja_apellido.grid(row=0,column=3)
        #LABEL SEXO
        self.lb_sexo=ttk.Label(self.labelframe2,text="Sexo")
        self.lb_sexo.grid(row=0,column=4,pady=5)
        #COMBOBOX SEXO
        self.cb_sexo=ttk.Combobox(self.labelframe2,values=[
            "Hombre",
            "Mujer",
            "No binario"
        ])
        self.cb_sexo.grid(row=0,column=5)
        #BOTON CREDITO
        self.bt_nuevo_cliente=ttk.Button(self.labelframe2,text="Insertar nuevo cliente",command=self.insertar_credito)
        self.bt_nuevo_cliente.grid(row=1,column=1,pady=5)
        #___________________________________________________________________________________________
        #_______________END___LABELFRAME-2__________________________________________________________

        #_____________________________________________________________________________________
        #____________________CREANDO LABELFRAME-3_____________________________________________

        self.labelframe3=ttk.Labelframe(self.pagina4,text="Detalles de Credito")
        if self.usr == "root":
           self.labelframe3.place(x=600,y=120)
        else: self.labelframe3.grid(row=0,column=1,padx=20,pady=20)
        self.tabla_informacion_c= ttk.Treeview(self.labelframe3,height=15,column=("#0",1,2))
        self.tabla_informacion_c.column("#0",width=140)
        self.tabla_informacion_c.column("#1",width=80)
        self.tabla_informacion_c.column("#2",width=80)
        self.tabla_informacion_c.heading("#0",text="Nombre product",anchor=CENTER)
        self.tabla_informacion_c.heading("#1",text="Precio",anchor=CENTER)
        self.tabla_informacion_c.heading("#2",text="Cantidad",anchor=CENTER)
        self.tabla_informacion_c.heading("#3",text="Fecha",anchor=CENTER)

        self.tabla_informacion_c.grid(row=0,column=0,pady=5)
        bt_abrir_lista=Button(self.labelframe3,text="Productos Fiados",command=self.AbrirListaProductosFiados).grid(row=1,column=0,sticky=W+E)





####################################################################################################
############### DETALLES DE PRODUCTOS ########################################################################
####################################################################################################

    def IenTdetalles_ventas(self):
        query="select * from ventas"
        datos=self.conSql().run_query(query,).fetchall()
        recorer=self.tabla_detalles_ventas.get_children()
        for r in recorer:
            self.tabla_detalles_ventas.delete(r)
        for d in datos:
            self.tabla_detalles_ventas.insert("",0,text=d[1],values=d[3])

    def IenTdetalles_ventas2(self,event):
        dato1=self.tabla_detalles_ventas.item(self.tabla_detalles_ventas.selection())["text"]
        print("YYYYY ",dato1)
        query="select * from ventas where fecha=? "
        datos=self.conSql().run_query(query,parameters=(dato1,)).fetchall()
        recorer=self.tabla_detalles_ventas2.get_children()
        for r in recorer:
            self.tabla_detalles_ventas2.delete(r)
        for d in datos:
            self.tabla_detalles_ventas2.insert("",0,text=d[4],values=(d[6],d[2]))
    def DesaserVenta(self):
        dato1=self.tabla_detalles_ventas2.item(self.tabla_detalles_ventas.selection())["text"]
        query="select cantidad from product where name =?"
        consulta=self.conSql().run_query(query,parameters=(dato1,)).fetchall()
        consulta= int(consulta)
        consulta= consulta +1
        query="UPDATE  product set cantidad=?  name where fecha=? "
        datos=self.conSql().run_query(query,parameters=(dato1,self.datoss))




    def DetallesDeProductos(self):
        self.pagina5= ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina5,text="Detalles de Ventas")
        self.labelframe1=LabelFrame(self.pagina5,text="Detalles de ventas de hoy")
        self.labelframe1.grid(row=0,column=0,padx=100,pady=20)

        self.labelframe2=LabelFrame(self.pagina5,text="Detalles de ventas de hoy")
        self.labelframe2.grid(row=0,column=1,padx=50,pady=20)


        self.tabla_detalles_ventas=ttk.Treeview(self.labelframe1,height=18,columns=('#1',))
        self.tabla_detalles_ventas.grid(row=0,column=1)
        self.tabla_detalles_ventas.column("#0",width=155)
        self.tabla_detalles_ventas.column("#1",width=150)
        self.tabla_detalles_ventas.heading("#0",text="fecha")
        self.tabla_detalles_ventas.heading("#1",text="usuario")

        self.tabla_detalles_ventas2=ttk.Treeview(self.labelframe2,height=18,columns=('#1','#2'))
        self.tabla_detalles_ventas2.column("#0",width=300)
        self.tabla_detalles_ventas2.column("#1",width=100)
        self.tabla_detalles_ventas2.column("#2",width=100)
        self.tabla_detalles_ventas2.heading("#0",text="Productos")
        self.tabla_detalles_ventas2.heading("#1",text="precio")
        self.tabla_detalles_ventas2.heading("#2",text="cantidad")
        self.tabla_detalles_ventas2.grid(row=0,column=0)
        self.tabla_detalles_ventas.bind('<Double-Button-1>',self.IenTdetalles_ventas2)
        bt_desaser_venta=ttk.Button(self.labelframe2,text="Desaser venta")
        bt_desaser_venta.grid(row=1,column=0,sticky=W+E)
        self.IenTdetalles_ventas()



####################################################################################################
###############ESTADISTICAS#########################################################################
####################################################################################################
    def estadisticas(self):
        fecha=self.OctenerFecha()[1]+"%"
        print(fecha,"ffffffffffffffffff")

        query="SELECT fecha FROM registro_ventas WHERE fecha LIKE  ?"
        dgl=self.conSql().run_query(query,parameters=(fecha,)).fetchall()[0][0]
        ddf=dgl[0:10]
        date = ddf.replace("-", " ")
        print(date)
        query="SELECT  sum(precio) FROM registro_ventas where fecha LIKE ?"
        dgf=self.conSql().run_query(query,parameters=(fecha,)).fetchall()[0]

        import datetime
        import calendar

        def findDay(date):
            born = datetime.datetime.strptime(date, '%Y %m %d').weekday()
            return (calendar.day_name[born])

        date=(findDay(date))

        a=[3,1,5,4,6,3]
        b=["Lunes","Martes","Miercoles","Jueves","Viermes","Sabado"]
        self.pagina6= ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina6,text="Estadisticas")

        """_______________________________________________"""
        data=[date,dgf]
        fig = Figure(figsize=(5, 2), dpi=200)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).bar(data[0],data[1])#AÑADIR "subbplot"




        c=(a,b)
        canvas = FigureCanvasTkAgg(fig, master=self.pagina6)  # CREAR AREA DE DIBUJO DE TKINTER.
        canvas.draw()


        canvas.get_tk_widget().grid(column=0,row=0,padx=80)



#-----------------------------BOTÓN "cerrar"----------------------------------
    def cerrar(self):
        root.quit()
        root.destroy()

        button = tk.Button(master=root, text="cerrar", command=self.cerrar)
####################################################################################################
############### CONFIGURACIONES ####################################################################
####################################################################################################

    def dollar(self):

        self.wind=Toplevel()
        query="SELECT atributos FROM configuraciones  WHERE nombre_cf='dollar'"
        precio_dollar= self.conSql().run_query(query,).fetchall()[0]
        lb_precio_anterior_dollar= Label(self.wind,text='Precio anterior').grid(row=0,column=0)

        caja_precio_anterior_dollar=ttk.Entry(self.wind)
        caja_precio_anterior_dollar.insert('',precio_dollar)
        caja_precio_anterior_dollar['state']="readonly"
        caja_precio_anterior_dollar.grid(row=0,column=1,padx=10)

        lb_nuevo_precio_dollar=Label(self.wind,text='Inserte nuevo precio').grid(row=1,column=0)
        self.caja_dollar= ttk.Entry(self.wind)
        self.caja_dollar.grid(row=1,column=1,padx=10)
        Button(self.wind,text="Actualizar",command=self.funDolar).grid(row=2,column=1,pady=10)
        self.wind.mainloop()

    def funDolar(self):
        dll=str(self.caja_dollar.get())
        print(dll)
        query="UPDATE configuraciones SET  atributos=? WHERE nombre_cf=?"
        dollar="dollar"
        parameters=(dll,dollar)

        self.conSql().run_query(query,parameters)
        self.wind.destroy()
        mb.showinfo("Exito","El precio del dollar se a actualisado")

    def convirtiendo_dollar(self):
        query="SELECT * FROM configuraciones  WHERE nombre_cf='dollar'"
        total_en_dollar=self.conSql().run_query(query,).fetchall()[0]
        total_en_dollar=total_en_dollar[2]
        #print(total_en_dollar + self.tt)
        r=self.tt / total_en_dollar
        r="{0:.2f}".format(r)
        self.Total_en_dolar= r

        self.result_dolar['text']='Total Dollars: {}'.format(r)

        #self.lb_dolar['text'] = 'Dollar: {}'.format("22")

    def verificacion(self,mirando):


        self.vt_conprovacion= Toplevel()
        lb_ingrese_contraseña= Label(self.vt_conprovacion,text="Ingrese contraseña").grid(row=0,column=0,pady=5,padx=10)

        self.caja_ingrese_contra=ttk.Entry(self.vt_conprovacion,show="*")
        self.caja_ingrese_contra.grid(row=0,column=1,padx=10)



        bt_Acectar= Button(self.vt_conprovacion,text="Acectar",command=lambda :self.VdeContraseña(mirando)).grid(row=1,column=1,pady=5,padx=10)
        self.vt_conprovacion.mainloop()

    def VdeContraseña(self,mirando):

        try:
            query="SELECT contraseña FROM usuario WHERE contraseña=?"
            parameters=(self.caja_ingrese_contra.get(),)
            self.octeniendo_contraseña=self.conSql().run_query(query,parameters).fetchall()[0][0]
            print(self.octeniendo_contraseña)
            #if self.caja_ingrese_contra.get() == self.octeniendo_contraseña:
            if mirando == 'nueva_contraseña':
                self.vt_conprovacion.destroy()
                self.NuevaContraseña()
            elif mirando == 'inicir_ventana_usr':
                self.usuarios()
                self.vt_conprovacion.destroy()

        except IndexError:
            self.caja_ingrese_contra.delete(0,tk.END)
            self.vt_conprovacion.configure(background="red")
            mb.showinfo("Error","Contraseña incorrecta")


    def NuevaContraseña(self):
        self.vt_cambiar_contra=Toplevel()
        #caja_contraseña_vieja.insert()
        lb_nueva_contraseña=Label(self.vt_cambiar_contra,text="Nueva contraseña").grid(row=0,column=0,pady=5,padx=10)
        self.caja_contraseña_nueva=ttk.Entry(self.vt_cambiar_contra)
        self.caja_contraseña_nueva.grid(row=0,column=1,padx=10)
        bt_acectar=Button(self.vt_cambiar_contra,text="Acectar",command=self.cambiandoContra).grid(row=1,column=1,pady=5)
        self.vt_cambiar_contra.mainloop()

    def cambiandoContra(self):
        query="UPDATE usuario SET contraseña=? WHERE contraseña=?"
        parameters=(self.caja_contraseña_nueva.get(),self.octeniendo_contraseña)
        self.conSql().run_query(query,parameters)
        mb.showinfo("Exito", "Se a cambiado la contraseña")
        self.vt_cambiar_contra.destroy()

    def BorrarUsuario(self):
        lista=self.tabla_detalles_usuarios.focus()
        dato=self.tabla_detalles_usuarios.item(lista)
        nombre_usr=dato['text']
        apellido_usr=dato['values'][0]
        print("BORRANO",apellido_usr,nombre_usr)
        query="DELETE from usuario WHERE nombre=? and apellido = ? "
        parameters=(nombre_usr,apellido_usr)
        self.conSql().run_query(query,parameters)
        self.OctenerUsuarios()
        mb.showinfo("EXITO","Usuario eliminado")

    def OctenerUsuarios(self):
        records= self.tabla_detalles_usuarios.get_children()
        for elementos in records:
            self.tabla_detalles_usuarios.delete(elementos)

        query= "SELECT * from usuario"
        usuarios=self.conSql().run_query(query,).fetchall()

        for usr in usuarios:
            self.tabla_detalles_usuarios.insert("",0,text=usr[1],value=(usr[2],usr[3],usr[4],usr[5],usr[6]))

    def usuarios(self):
        self.ve_usuarios= Toplevel()
        labelframe1=ttk.LabelFrame(self.ve_usuarios,text="Inserte Nuevo Usuario")
        labelframe1.grid(row=0,column=0,padx=20,pady=10)

        lb_nombre=Label(labelframe1,text="Inserte el nombre").grid(column=0,row=0)
        caja_nombre=ttk.Entry(labelframe1)
        caja_nombre.grid(row=0,column=1)

        lb_apellido=Label(labelframe1,text="Inserte el apellido").grid(column=2,row=0)
        caja_apellido=ttk.Entry(labelframe1)
        caja_apellido.grid(row=0,column=3)

        lb_numero_t=Label(labelframe1,text="Inserte el numero de telefono").grid(column=0,row=1)
        caja_numero_t=ttk.Entry(labelframe1)

        caja_numero_t.grid(row=1,column=1)

        lb_numero_c=Label(labelframe1,text="Inserte el numero de cedula").grid(column=2,row=1)
        caja_numero_c=ttk.Entry(labelframe1)
        caja_numero_c.grid(row=1,column=3)

        lb_contraseña=Label(labelframe1,text="Inserte la contraseña").grid(column=0,row=2)
        caja_contraseña=ttk.Entry(labelframe1)
        caja_contraseña.grid(row=2,column=1)

        lb_permiso=Label(labelframe1,text="Elija el tipo de permiso").grid(column=2,row=2)
        cbx_permiso=ttk.Combobox(labelframe1,values=['root','semi_root','usr_sinprevilegios'])
        cbx_permiso.grid(row=2,column=3)

        bt_agregar=ttk.Button(labelframe1,text="Agregar",command=lambda :self.InsertarUsr(caja_nombre.get(),caja_apellido.get(),caja_numero_t.get(),caja_numero_c.get(),caja_contraseña.get(),cbx_permiso.get()))
        bt_agregar.grid(row=3,column=1,pady=10,columnspan=2)

        #LABEL FRAME2 ////////////////////////

        labelframe2=ttk.LabelFrame(self.ve_usuarios,text="Detalles de usuarios")
        labelframe2.grid(row=1,column=0)
        self.tabla_detalles_usuarios=ttk.Treeview(labelframe2,column=("#0","#1","#2","#3","#4"))
        self.tabla_detalles_usuarios.grid(row=0,column=0,columnspan=2)
        self.tabla_detalles_usuarios.column("#0",width=120)
        self.tabla_detalles_usuarios.column('#1',width=120)
        self.tabla_detalles_usuarios.column("#2",width=120)
        self.tabla_detalles_usuarios.column("#3",width=140)
        self.tabla_detalles_usuarios.column("#5",width=120)
        self.tabla_detalles_usuarios.heading("#0",text="Nombre",anchor=CENTER)
        self.tabla_detalles_usuarios.heading("#1",text="Apellido",anchor=CENTER)
        self.tabla_detalles_usuarios.heading("#2",text="Numero Telefono",anchor=CENTER)
        self.tabla_detalles_usuarios.heading("#3",text="Numero Cedula",anchor=CENTER)
        self.tabla_detalles_usuarios.heading("#4",text="Contraseña",anchor=CENTER)
        self.tabla_detalles_usuarios.heading("#5",text="Permiso",anchor=CENTER)
        self.OctenerUsuarios()



        bt_actualizar_usr = ttk.Button(labelframe2,text='Actualizar Usuario')
        bt_actualizar_usr.grid(row=1,column=0,columnspan=1,sticky=W+E)

        bt_borrar_usr=ttk.Button(labelframe2,text='Borrar Usuario',command=self.BorrarUsuario)
        bt_borrar_usr.grid(row=1,column=1,columnspan=1,sticky=W+E)



    def InsertarUsr(self,caja_nombre,caja_apellido,caja_numero_t,caja_numero_c,caja_contraseña,cbx_permiso):
        #print(caja_nombre,caja_apellido,caja_numero_t,caja_numero_c,caja_contraseña,cbx_permiso)
        query="INSERT into usuario(nombre,apellido,numero_telefono,numero_cedula,contraseña,permisos) VALUES(?,?,?,?,?,?)"
        parameters=(caja_nombre,caja_apellido,caja_numero_t,caja_numero_c,caja_contraseña,cbx_permiso)

        self.conSql().run_query(query,parameters)
        """caja_nombre.delete(0,END)
        caja_apellido.delete(0,END)
        caja_numero_t.delete(0,END)
        caja_numero_c.delete(0,END)
        caja_contraseña.delete(0,END)
        cbx_permiso.delete(0,END)"""
        self.ve_usuarios.destroy()
        self.usuarios()
        mb.showinfo("Exito", "Se a insertado ala bases de dato el nuevo usuario")





#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    def configuraciones(self):


        self.pagina7= ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina7,text="Configuraciones")
        #_____________________________________________________________________________________
        #____________________CREANDO LABELFRAME-1_____________________________________________
        self.labelframe1=LabelFrame(self.pagina7,bd=0)
        self.labelframe1.grid(row=0,column=0,padx=500,pady=150)

        bt_price_dollar= Button(self.labelframe1,text="Ajustar precio del Dollar",command=self.dollar).grid(row=0,column=0,pady=30)


        bt_cambiar_conytaseña=Button(self.labelframe1,text="Cambiar contraseña",command=lambda :self.verificacion(mirando='nueva_contraseña')).grid(row =1,column=0)

        bt_usuarios=Button(self.labelframe1,text="Administrar Usurios",command=lambda : self.verificacion(mirando="inicir_ventana_usr")).grid(row=3,column=0)



####################################################################################################
############### INFORMACION ########################################################################
####################################################################################################

    def informacion(self):


        self.style.configure('W.TLabel', font =
               ('calibri', 12, 'bold'),
                foreground = 'green')

        self.pagina8= ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina8,text="informacion")

        #LABEL |LENGUAJE
        lenguaje= "Esta aplicacion de escritorio fue desarrollada por ADER YASMIR ZEAS ROCHA.\n" \
                  "\n"\
                  "     Esta aplicacion se de sarollo en el lenguaje de programacion de Python \n" \
                  "en su version 3.9 para aser la interfas grafica se uso una libreria llamada: Tkinter. \n " \
                  " \n"\
                  "        EL entorno de desarrollo que se uso fue Pycharn-edu-2021.1. \n" \
                  "\n"\
                  "         Contactar al programador: aderjasmirzeasrocha@gmail.com"

        query="SELECT SUM(price*cantidad) FROM product"
        cap=self.conSql().run_query(query,).fetchall()
        capital_s=cap

        query="SELECT SUM((price - cantidad_sin_ganansia) * cantidad  ) FROM product"
        gananciaV=self.conSql().run_query(query,).fetchall()

        capital_s =str(capital_s)
        gananciaV=str(gananciaV)
        
        lb_ganancia=ttk.Label(self.pagina8,text="Ganancia= "+gananciaV)
        lb_ganancia.grid(row=3,column=2)
        capital=ttk.Label(self.pagina8,text="CAPITAL= "+capital_s)
        capital.grid(row=3,column=4)

        separator = ttk.Separator(self.pagina8, orient='horizontal')
        separator.grid(row=2,column=0 ,ipadx=400, pady=10,columnspan=6)
        lb_crador=ttk.Label(self.pagina8,text=lenguaje,style = 'W.TLabel')
        lb_crador.grid(row=1,column=1,padx=300,pady=100,columnspan=6)




class verificar:
    def __init__(self):

        vt = tk.Tk()
        self.photo = PhotoImage(file ="image.png")

        self.lb_contraceña = ttk.Label(vt, text="Contraceña")
        self.lb_contraceña.place(x=20,y=140)

        def vr():

            try:
                query="SELECT * FROM usuario where contraseña=?"
                datos=conSql().run_query(query,parameters=(self.caja.get(),)).fetchall()
                octeniendo_contraseña=datos[0][5]
                print('esta es la clave :'+octeniendo_contraseña)

                if self.caja.get() == octeniendo_contraseña:
                   usr=datos[0][6]
                   nombre_usr=datos[0][1]
                   nombre_usr=nombre_usr +" "+ datos[0][2]
                   print(nombre_usr)
                   salir()
                   run=root(usr,nombre_usr)
                else:print('ubo un errrrrror')

            except IndexError:
                color()



        def salir():
            vt.destroy()
            print("saliendo")
        def color():
                    mb.showinfo("Error", "Contraseña incorrecta ")
                    vt.configure(background="#e50000")
                    self.lb_contraceña = tk.Label(vt, text="Contraceña", bg="#e50000",bd=0)
                    self.titulo= tk.Label(vt,text="Farmacia Soluciones",font=("Z003",24,"bold") ,bg="#e50000")
                    self.caja.delete(0,tk.END)



        vt.title("Verifique su contraseña")
        vt.geometry("300x230")

        self.caja = ttk.Entry(vt,show="*")
        self.caja.place(x=70,y=160)
        self.boton = ttk.Button(vt, text="Verificar", command=vr)
        self.boton.place(x=110, y=190)
        self.lb_logo = ttk.Label(vt, image=self.photo,width=10)
        self.lb_logo.place(x=100,y=20)
        self.titulo= tk.Label(vt,text="Farmacia Soluciones",font=("Z003",24,"bold")).place(x=20,y=120)
        self.caja.focus()


        vt.mainloop()



app = verificar()
