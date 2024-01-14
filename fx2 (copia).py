

from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from datetime import datetime
import hashlib
import random
from sql import Others as ConecionSql
from hora import creando_a_hora as hr
from contraseña import GeneraContraseña




dimension_ancho= 1440
dimension_altura=900
#____________TREEVIEW_______________________________

class Inicio():

    def __init__(self,nombre_usr,permiso_usr):


        query="select * from configuraciones where  nombre_cf ='color_fondo';"
        ConecionSql().run_query(query,).fetchall()[0][2]

        color_fondo='#1e1d23'
        color_fuente='white'
        query="select * from configuraciones where  nombre_cf ='color_menu';"
        color_menu= ConecionSql().run_query(query,).fetchall()[0][2]
        '#a9dfbf'
        print(color_fondo)
        w = Tk()
        w.geometry('1440x900')
        w.configure(bg=color_fondo)  # 12c4c0')
        w.resizable(0, 0)
        w.title('Toggle Menu')
        imagen_guardar = PhotoImage(file="iconos/guardar.png")
        imagen_facturar = PhotoImage(file="iconos/facturar.png")
        iccliente = ImageTk.PhotoImage(Image.open("iconos/cliente.png"))
        icon_usuario_m = ImageTk.PhotoImage(Image.open("iconos/icons8-male-user-64.png"))
        icon_usuario_f=ImageTk.PhotoImage(Image.open("iconos/usuario_femenino.png"))
        icon_seguridad=ImageTk.PhotoImage(Image.open("iconos/seguridad.png"))




        # Creamos un estilo para el widget Treeview
        style = ttk.Style()

        # Establecemos el color de fondo del Treeview en amarillo
        style.configure("Treeview", background="#ef9a9a")

        # Establecemos el color de los títulos en rojo
        style.configure("Treeview.Heading", foreground="green")

        # Establecemos la fuente de los títulos en Arial, tamaño 12
        style.configure("Treeview.Heading", font=("Forte", 10))
        style.configure("Treeview", font=("TkDefaultFont", 12))
        style.configure("Treeview", rowheight=30)

        def on_closing():
            if mb.askokcancel("Salir", "Seguro que quieres salir?"):
                w.destroy()



        def default_home():
            f2 = Frame(w, width=1200, height=600, bg='#262626')
            f2.place(x=0, y=45)
            l2 = Label(f2, text='Home', fg='white', bg='#262626')
            l2.config(font=('Comic Sans MS', 90))
            l2.place(x=290, y=150 - 45)


        def home():
            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            l2 = Label(f2, text='Home', fg=color_fuente, bg=color_fondo)
            l2.config(font=('Comic Sans MS', 90))
            l2.place(x=290, y=150 - 45)
            toggle_win()

        def OctenerFecha():
                import calendar
                dateTimeObj = datetime.now()
                #timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                #fecha=timestampStr.split[0]()[0]
                año_mes =dateTimeObj.strftime("%d-%m-%Y").split()[0]
                hora = dateTimeObj.strftime("%H-%M-%S")
                hora=hora.split()[0]
                timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S")
                fecha=timestampStr.split()[0]
                return fecha,año_mes,hora



        def Facturar():

            def buscar(event):
                octener_datos=caja_buscar.get() + "%"
                print(octener_datos)
                parameters=(octener_datos,)
                #query='SELECT * FROM product WHERE name like = ?'
                query='SELECT * FROM product WHERE name LIKE  ?'

                bqd=ConecionSql().run_query(query,parameters)

                #Limpiando la tabla
                records= lista_producto.get_children()
                for elementos in records:
                    lista_producto.delete(elementos)

                for fila in bqd:
                    lista_producto.insert('', 0, text=fila[1], value= (fila[2], fila[3]))
                if octener_datos == "":
                    octener_productos()

            def QuitarProducto():
                try:
                  selecsionar_item= factura.selection()[0]
                  factura.delete(selecsionar_item)
                except:
                    mb.showwarning("Error","Selecione el producto que quiere quitar de la factura")

            def limpiar():
                factura.delete(*factura.get_children())
                print("exito")


            def octener_productos():

                #Limpiando la tabla
                records= lista_producto.get_children()
                for elementos in records:
                    lista_producto.delete(elementos)
                #Consultando los datosdef buscando_productos(self):
                query = 'SELECT * FROM product ORDER BY name DESC'
                db_rows=ConecionSql().run_query(query,)
                for fila in db_rows:
                    lista_producto.insert('', 0, text=fila[1], value= (fila[2], fila[3]))

            def OctenerClientes():

                def DandoCredito(event):
                    p = cb.get()
                    p = p.split()
                    nombre = p[0]
                    apellido = p[1]
                    query = "SELECT * FROM credito where nombre=? and apellido=?"
                    trallendo_deuda1 = ConecionSql().run_query(query, parameters=(nombre, apellido)).fetchall()[0][5]
                    listap = ""


                    for item in factura.get_children():
                        c = factura.item(item)["text"]
                        b = factura.item(item)["values"][0]
                        g = factura.item(item)["values"][1]
                        hr().RestandoProductoVendido(c, g)
                        octener_productos()

                        query = "INSERT INTO product_en_creditos(nombre,precio,fecha,codigo_cliente,cantidad) VALUES(?,?,?,?,?)"
                        d = OctenerFecha()[0]
                        e = trallendo_deuda1
                        parameters = (c, b, d, e, g)
                        listap += c + ", "
                    print(listap, "====")
                    listap = ""

                    total = 0
                    for item in factura.get_children():
                        celda = float(factura.set(item, "#1"))
                        celda_cantidad = int(factura.set(item, "#2"))
                        sumas_de_celda = celda * celda_cantidad
                        total += sumas_de_celda
                    print(total)

                    query = "SELECT deuda FROM credito where nombre=? and apellido=?"
                    trallendo_deuda = ConecionSql().run_query(query, parameters=(nombre, apellido))

                    tr = trallendo_deuda.fetchall()[0][0]
                    print(tr)
                    sumando_deuda = tr + total
                    print(apellido)
                    parameters = (sumando_deuda, nombre, apellido)
                    # self.run_query(query,)
                    query = "UPDATE credito SET deuda =? where nombre=? and apellido= ?"
                    ConecionSql().run_query(query, parameters)

                    vte.destroy()
                    mb.showinfo("Exito", "Sele a dado el cridito a: " + "(" + nombre + ")")
                    octener_productos()
                    limpiar()


                vte= Toplevel()
                vte.geometry('250x100')
                vte.resizable(0, 0)
                lb_selecione_cliente=Label(vte,text='Selecione cliente a darlr el credito')
                lb_selecione_cliente.place(x=5,y=5)

                query="SELECT nombre, apellido  FROM credito"
                dato=ConecionSql().run_query(query).fetchall()

                lb_icon_cliente=Label(vte,image=iccliente).place(x=5,y=33)
                cb = ttk.Combobox(vte,values=dato)
                cb.place(x=60, y=40)
                cb.bind('<Return>',DandoCredito)
                lb_total = Label(vte, text="Total: ").place(x=5,y=75)




            def agregar(event):
                cur_id0 = lista_producto.focus()
                c_s = int(float(lista_producto.item(cur_id0)['values'][1]))
                if c_s <= 0:
                    mb.showwarning("Error", "Este producto se a agotado")
                    return

                vt_inPA = Toplevel()
                lb_insetar_cantidad_p= Label(vt_inPA,text='Inserte cantidad a vender').grid(row=0,column=0)
                caja_inser_cantidad_p = ttk.Entry(vt_inPA)
                caja_inser_cantidad_p.grid(row=1,column=0)
                caja_inser_cantidad_p.focus()





                def AgregarAFactura(event):
                    cur_id = lista_producto.focus()



                    if caja_inser_cantidad_p.get() == "":
                        mb.showwarning("Error", "Dede ingresar la cantidad de producto que desea agregar")
                        return


                    try:
                        multiplicandoCantidadDeVeses = int(caja_inser_cantidad_p.get())

                    except:
                        mb.showwarning("Error", "No se aceptan letras ni simbolos")
                        caja_inser_cantidad_p.delete(0, END)
                        return

                    c_2 = int(float(lista_producto.item(cur_id)['values'][1]))
                    c_1 = int(caja_inser_cantidad_p.get())
                    sud_total = float(lista_producto.item(cur_id)['values'][0]) * c_1



                    if c_1 > c_2:
                        r_c = c_1 - c_2
                        mb.showwarning("Error", "No hay esa cantidad de productos asen falta " + str(r_c) + " " +
                                    lista_producto.item(cur_id)["text"])
                        caja_inser_cantidad_p.delete(0, END)
                        return

                    if cur_id:
                        pasando_producto = lista_producto.item(cur_id)['values'][1]
                        pasando_producto1 = lista_producto.item(cur_id)['values'][0]

                        if multiplicandoCantidadDeVeses == 0:
                            mb.showwarning("Error", "Como sete ocurre que vas agregar un producto ingresando '0'")
                            caja_inser_cantidad_p.delete(0, END)
                            return

                        factura.insert("", 0, text=lista_producto.item(cur_id)["text"],
                                            values=(pasando_producto1, str(multiplicandoCantidadDeVeses), sud_total))
                        caja_inser_cantidad_p.delete(0, END)

                    lista = lista_producto.item(cur_id)
                    dicionario = lista['values']
                    dc = dicionario[0]
                    dcc = float(dc)
                    # SACANDO TOTAL PARA SCROLLTEXT
                    total = 0
                    for item in factura.get_children():
                        celda = float(factura.set(item, "#1"))
                        celda_cantidad = int(factura.set(item, "#2"))
                        sumas_de_celda = celda * celda_cantidad
                        total += sumas_de_celda
                        tt_credito = total

                    cur_id = lista_producto.focus()
                    lista = lista_producto.item(cur_id)
                    dicionario = lista['values']
                    b = lista['text']
                    # quitamos la ventana que contruimos para insertar las cantidades de los productos
                    vt_inPA.destroy()



                caja_inser_cantidad_p.bind('<Return>', AgregarAFactura)

                vt_inPA.mainloop()

            def total():
                def convirtiendo_dollar(total):
                    query = "SELECT * FROM configuraciones  WHERE nombre_cf='dollar'"
                    total_en_dollar = ConecionSql().run_query(query, ).fetchall()[0]
                    total_en_dollar = total_en_dollar[2]
                    r = total / total_en_dollar
                    r = "{0:.2f}".format(r)
                    print(r)
                    return r



                def Confirmar_venta(total, cf_vt, lb_mb_e, caja_cambio, CheckVar1,t):

                        pago="{0:.2f}".format(int(caja_cambio.get()))

                        print("valor del check ", CheckVar1.get())
                        clave_producto = OctenerFecha()[1] + nombre_usr + OctenerFecha()[2]
                        lista = ""

                        for item in factura.get_children():
                            c = factura.item(item)["text"]
                            d = factura.item(item)["values"][0]
                            g = factura.item(item)["values"][1]


                        if caja_cambio.get() == "":
                            lb_mb_e['text'] = "{}".format("Se nesesita que ingrese el cambio")
                            return
                        try:
                            if CheckVar1.get() == 1:
                                query = "SELECT * FROM configuraciones  WHERE nombre_cf='dollar'"
                                total_en_dollar = ConecionSql().run_query(query, ).fetchall()[0]
                                total_en_dollar = total_en_dollar[2]
                                cambio = float(caja_cambio.get()) * total_en_dollar
                                cambio = cambio - total

                            else:
                                #Esta condicion es para poner de total el descuento
                                if t > 0:
                                    total=t
                                cambio = float(caja_cambio.get()) - float(total)
                                cambio = cambio = "{0:.2f}".format(cambio)
                            if CheckVar1.get() != 1:
                                if float(caja_cambio.get()) < float(total):
                                    lb_mb_e['text'] = "{}".format("Error el pago es menor al total de los productos")
                                    return
                        except Exception as e:
                            lb_mb_e['text'] = "{}".format(f"Se prdujo un error:{e}")
                            caja_cambio.delete(0, END)
                            return


                        cf_vt.destroy()
                        if CheckVar1 == 1:
                            mb.showinfo("Exito", "El buelto del cambio del dollar es: " + str(cambio))
                        mb.showinfo("Exito", "El vuelto es: " + str(cambio))


                        print('esta es la contra: ' + clave_producto)


                        hr().RestandoProductoVendido(c, g)


                        #hr().registro_ventas(parameters)


                        #rango = slice(3, 6)


                        #hr().registro_ventas_hoy(parameters)
                         #Ultimo siclo REGISTRO
                        usr = nombre_usr
                        f=OctenerFecha()[0]
                        code=GeneraContraseña()
                        listap=""
                        for item in factura.get_children():
                            nombre = factura.item(item)["text"]
                            precio = factura.item(item)["values"][0]
                            cantidad = str(factura.item(item)["values"][1])
                            parameters= (nombre,precio,f,usr,cantidad,code)

                            hr().registro_ventas(parameters)
                            print("me imprimo",parameters)
                            while len(nombre) < 60:
                                nombre+=" "
                            while len(precio) < 5:
                                precio+=" "
                            while len(cantidad) < 7:
                                cantidad+=" "
                            sud_total=float(precio)*float(cantidad)

                            listap += nombre+str(precio)+"     "+str(cantidad)+"     "+str(sud_total)+"\n"



                        cambio= float(pago) - float(total)
                        cambio="{0:.2f}".format(cambio)
                        parametros= (listap,str(total),pago,str(cambio),cantidad)
                        hr().RegistroText(parametros,ur=usr)


                        octener_productos()
                        limpiar()
                        caja_buscar.delete(0, END)
                        """self.ProductosApuntoAgotarse()
                        self.IenTdetalles_ventas()"""



                def Ventanaconfirmar_venta(total):
                    # La función AplicarDescuento recibe cuatro parámetros: precio, cantidad, porcentaje_descuento y cantidad_dar_descuento.
                    def AplicarDescuento(precio, cantidad, porcentaje_descuento, candidad_dar_descuento):
                        # Se verifica si alguno de los parámetros recibidos es None o está vacío.
                        if porcentaje_descuento is None or candidad_dar_descuento is None:
                            # Si alguno de los parámetros es None o está vacío, se retorna 0.
                            return 0

                        elif porcentaje_descuento == "" or candidad_dar_descuento == "":
                            # Si alguno de los parámetros es None o está vacío, se retorna 0.
                            return 0
                        elif porcentaje_descuento == "Null" or candidad_dar_descuento == "Null":
                            # Si alguno de los parámetros es None o está vacío, se retorna 0.
                            return 0


                        elif cantidad >= candidad_dar_descuento:
                            # Si la cantidad es mayor o igual a la cantidad_dar_descuento, se aplica el descuento.
                            print(cantidad, ' ', candidad_dar_descuento, ' Se aaplica descuento')
                            descuento = precio * (porcentaje_descuento / 100)
                            precio_final = (precio - float(descuento)) * cantidad
                            precio_final = "{0:.2f}".format(precio_final)
                            return precio_final
                        else:
                            # En caso contrario, no se aplica el descuento y se retorna el precio multiplicado por la cantidad
                            return precio * cantidad

                    # Se inicializa una variable t con valor 0.0
                    t = 0.0

                    # Se itera sobre cada elemento en factura.get_children()
                    for item in factura.get_children():
                        # Se obtiene el nombre, precio y cantidad de cada elemento
                        c = factura.item(item)["text"]
                        d = float(factura.item(item)["values"][0])
                        g = factura.item(item)["values"][1]
                        nombre = c
                        precio = d
                        cantidad = g
                        # Se ejecuta una consulta a la base de datos para obtener el porcentaje de descuento y la cantidad_dar_descuento para el producto actual
                        query = "SELECT descuento,cantidad_xmayor FROM product where name=?"
                        parameters = (nombre,)
                        datos = ConecionSql().run_query(query, parameters).fetchall()[0]
                        porcentaje_descuento = datos[0]
                        try:
                          candidad_dar_descuento =float(datos[1])
                        except:
                            print("primera ex")
                            candidad_dar_descuento =0

                        try:
                            if porcentaje_descuento >= 1 and candidad_dar_descuento >= 1:
                                 t += float(AplicarDescuento(precio, cantidad, porcentaje_descuento, candidad_dar_descuento))
                            else:
                                print("Entramos ala exsexion")
                                t += precio * cantidad
                                print(t)

                        except:t += precio * cantidad
                        if cantidad < candidad_dar_descuento:
                                t += 0

                        print("Entramos ala exesion 2")
                        """ t += float(factura.item(item)["values"][2])
                            print("Entramos ala exsexion")
                            continue"""


                    print("Este es el total",str(t))

                    cf_vt = Toplevel()
                    cf_vt.resizable(False, False)
                    cf_vt.title("Confirmar venta")


                    lb_total = ttk.Label(cf_vt, text="Total")
                    lb_total.grid(row=0, column=0, padx=10, pady=2)
                    lb_descuento = ttk.Label(cf_vt, text="Descuento")
                    lb_descuento.grid(row=1, column=0, padx=10, pady=2)
                    lb_cambio = ttk.Label(cf_vt, text="Cabio de dinero")
                    lb_cambio.grid(row=2, column=0, padx=10, pady=5)
                    lb_mb_e = Label(cf_vt, text="", fg="red")
                    lb_mb_e.grid(row=3, column=1)
                    CheckVar1 = IntVar()

                    C1 = Checkbutton(cf_vt, text="Dollares", variable=CheckVar1, \
                                     onvalue=1, offvalue=0, height=5, \
                                     width=20)
                    C1.grid(row=2, column=2)

                    caja_cambio = ttk.Entry(cf_vt)
                    caja_cambio.grid(row=2, column=1, padx=10, pady=5)
                    bt_canselar = ttk.Button(cf_vt, text="Canselar",
                                             command=lambda: (cf_vt.destroy(), limpiar(), caja_buscar.delete(0, END)))
                    bt_canselar.grid(row=4, column=0, padx=10, pady=5)
                    bt_confirmar = ttk.Button(cf_vt, text="Confirmar",
                                              command=lambda: Confirmar_venta(total, cf_vt, lb_mb_e, caja_cambio, CheckVar1,t))
                    bt_confirmar.grid(row=4, column=1, padx=10, pady=5)
                    #esto es porsi los datos igualan con el descuento y las condiciones anteriores no evitaron su avance
                    if t == total:
                        t= 0
                    lb_total["text"] = "Total cordobas: {}   Dollar: {}".format(total, convirtiendo_dollar(total))
                    lb_descuento["text"]= "Total con descuento: {}".format(t)

                if not factura.get_children():
                    mb.showwarning("Error","Debes agregar productos a la factura")
                    return
                global lista_factura
                print("-----comensando funcion venta----------")
                total = 0.0

                for item in factura.get_children():
                    celda = float(factura.set(item, "#1"))
                    celda_cantidad = float(factura.set(item, "#2"))
                    sumas_de_celda = celda * celda_cantidad
                    total += sumas_de_celda
                print(total)
                Ventanaconfirmar_venta(total)





            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)

            # TABLA |Lista de productos
            lista_producto = ttk.Treeview(f2, height=23, columns=("#0", "#1"))
            lista_producto.heading('#0', text='Nombre', anchor=CENTER)
            lista_producto.heading('#1', text='Presio', anchor=CENTER)
            lista_producto.heading('#2', text='cantidad', anchor=CENTER)
            lista_producto.column("#0", width=450)
            lista_producto.column("#1", width=80)
            lista_producto.column("#2", width=80)
            lista_producto.grid(row=0, column=0,sticky=W+E)
            lista_producto.bind('<Double-Button-1>', agregar)
            lista_producto.tag_configure("tagName", font=("TkDefaultFont", 20))

            caja_buscar = ttk.Entry(f2, width=31)
            caja_buscar.grid(column=0, row=1,sticky=W+E,pady=0)
            caja_buscar.bind("<KeyRelease>", buscar)
            caja_buscar.focus()
            caja_buscar.config(font=("Arial", 20, "bold"))



            # TABLA FACTURA
            factura = ttk.Treeview(f2, height=23, column=("#0", 2, 3))
            factura.heading('#0', text='Nombre', anchor=CENTER)
            factura.column('#0', width=400)
            factura.heading('#1', text='Presio', anchor=CENTER)
            factura.column('#1', width=100)
            factura.heading('#2', text='Cantidad', anchor=CENTER)
            factura.column("#2", width=80)
            factura.heading('#3', text='Sub total', anchor=CENTER)
            factura.column("#3", width=100)
            factura.grid(row=0, column=1,columnspan=2,sticky=W +E)

            octener_productos()
            bt_vender = Button(f2, text="Vender",width=43,command=total)
            bt_vender.grid(row=1, column=1,columnspan=1)
            bt_credito = Button(f2, text="Dar en credito",width=43,command=OctenerClientes)
            bt_credito.grid(row=1, column=2,columnspan=1)

            #Menu ppo____________________________________________
            popup = Menu(f2, tearoff=0)

            # Adding Menu Items
            popup.add_command(label="Quitar",command=QuitarProducto)
            popup.add_separator()
            popup.add_command(label="Limpiar",command=limpiar)

            def menu_popup(event):
                # display the popup menu
                try:
                    popup.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    # Release the grab
                    popup.grab_release()
            factura.bind("<Button-3>", menu_popup)
            # END_Menu ppo____________________________________________


        def AdministrarProduct():

            def BuscarTodosLosProductos(event):
                octener_datos=caja_buscar_todos_productos.get() + "%"
                print(octener_datos)
                parameters=(octener_datos,)
                #query='SELECT * FROM product WHERE name like = ?'
                query='SELECT * FROM product WHERE name LIKE  ?'

                bqd=ConecionSql().run_query(query,parameters)

                #Limpiando la tabla
                records= lista_todos_los_datos_productos.get_children()
                for elementos in records:
                    lista_todos_los_datos_productos.delete(elementos)

                for fila in bqd:
                    lista_todos_los_datos_productos.insert('', 0, text=fila[1], value= (fila[2], fila[5], fila[3], fila[4], fila[6], fila[7], fila[8]))
                if octener_datos == "":
                    octener_todos_los_productos()
            def octener_todos_los_productos():

                #Limpiando la tabla
                records= lista_todos_los_datos_productos.get_children()
                for elementos in records:
                    lista_todos_los_datos_productos.delete(elementos)
                #Consultando los datosdef buscando_productos(self):
                query = 'SELECT * FROM product ORDER BY name DESC'
                db_rows=ConecionSql().run_query(query,)
                for fila in db_rows:
                    lista_todos_los_datos_productos.insert('', 0, text=fila[1], value= (fila[2], fila[5], fila[3], fila[4], fila[6], fila[7], fila[8]))

            def BorrarProducto():
                try:
                    lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text'][0]
                except IndexError as e:
                    mb.showwarning("Error","Porfavor Selecione Un Producto")
                    return
                name=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text']
                query = 'DELETE FROM product WHERE name = ?'
                ConecionSql().run_query(query, (name,))
                mb.showinfo("Exito✅", "El producto se a borrado")
                octener_todos_los_productos()
                query="INSERT INTO notificaciones(nombre_n,fecha) values(?,?)"
                noti= "El usuario: "+nombre_usr+" borro el producto: "+name
                parameters=(noti,OctenerFecha()[0])
                ConecionSql().run_query(query,parameters)



            def ActualizarProducto():
                try:
                    lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text'][0]
                except IndexError as e:
                    mb.showwarning("Error","Porfavor Selecione Un Producto")
                    return
                name=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text']
                datos=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['values']

                caja_i_nombre.delete(0,END)
                caja_i_nombre.insert(0,name)
                caja_i_presio.delete(0,END)
                caja_i_presio.insert(0,datos[1])
                caja_i_cantidad.delete(0,END)
                caja_i_cantidad.insert(0,datos[2])
                caja_i_porsentage.delete(0,END)
                caja_i_porsentage.insert(0,datos[0])
                caja_i_fecha_vencimiento.delete(0, END)
                caja_i_fecha_vencimiento.insert(0, datos[3])
                caja_i_fecha_alerta_antes_devencer.delete(0, END)
                caja_i_fecha_alerta_antes_devencer.insert(0, datos[4])
                caja_i_descuento.delete(0,END)
                caja_i_descuento.insert(0,datos[5])
                caja_i_cantidad_dar_descuento.delete(0,END)
                caja_i_cantidad_dar_descuento.insert(0,datos[6])

                bt_i_insertar_nuevo_producto.configure(text="Actualizar")


            def ActualizandoProducto():
                if caja_i_descuento.get() == "Descuento" and caja_i_fecha_alerta_antes_devencer.get() == "Mes antelacion" and caja_i_cantidad_dar_descuento.get() == "Cantidad descuento":
                    return
                if caja_i_fecha_vencimiento.get() != "":
                    if len(caja_i_fecha_vencimiento.get()) != 10:
                        mb.showwarning("Error","La caja de la fecha nesesita que se inserten 10 digitos use / para separar ejemplo: 01/06/2023   primero el dia despues el mes y despues el año")
                        return

                name=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text']
                parameters=(caja_i_nombre.get(),caja_i_presio.get(),caja_i_cantidad.get(),caja_i_porsentage.get(),caja_i_fecha_vencimiento.get(),caja_i_fecha_alerta_antes_devencer.get(),caja_i_descuento.get(),caja_i_cantidad_dar_descuento.get(),name)
                query= 'UPDATE product SET name = ?, price=?, cantidad=?,cantidad_sin_ganansia=?,fecha_vencimiento=?,mesProximoDevovlucion=?,descuento=?,cantidad_xmayor=? WHERE name = ?'
                ConecionSql().run_query(query,parameters)
                bt_i_insertar_nuevo_producto.configure(text="Insertar")

                query="INSERT INTO notificaciones(nombre_n,fecha) values(?,?)"
                presio_viejo=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['values'][1]
                noti= "El usuario: "+nombre_usr+" Actualizo el producto: "+name+" Nuevo precio: "+caja_i_presio.get()+" precio anterior: "+presio_viejo
                parameters=(noti,OctenerFecha()[0])
                ConecionSql().run_query(query,parameters)

                """Limpiamos todas las cajas"""
                on_entry_click_nombre("")
                on_entry_click_precio("")
                on_entry_click_cantidad("")
                on_entry_click_porsentage("")
                on_entry_click_fecha_vencimiento("")
                on_entry_click_fecha_alerta_antes_devencer("")
                on_entry_click_descuento("")
                on_entry_click_cantidad_descuento("")
                InsertandoDatosDeLasCajas()
                mb.showinfo("Exito", "EL producto se a actualizado")

                octener_todos_los_productos()


            def CambiarEstadoBotonProduct():
                if bt_i_insertar_nuevo_producto.cget("text") == "Actualizar":
                    ActualizandoProducto()

                elif bt_i_insertar_nuevo_producto.cget("text") == "Insertar":
                    print("Entramos")
                    InsertarNuevoProducto()

            def InsertandoDatosDeLasCajas():
                caja_i_nombre.insert(0,"Nombre")
                caja_i_presio.insert(0, "Precio")
                caja_i_cantidad.insert(0, "Cantidad")
                caja_i_porsentage.insert(0, "Porsentage")
                caja_i_fecha_vencimiento.insert(0, "Fecha vencimiento")
                caja_i_fecha_alerta_antes_devencer.insert(0, "Mes antelacion")
                caja_i_descuento.insert(0, "Descuento")
                caja_i_cantidad_dar_descuento.insert(0, "Cantidad descuento")

            def InsertarNuevoProducto():
                if caja_i_nombre.get() == "" or caja_i_presio.get() == "" or caja_i_cantidad.get() == "":
                    mb.showwarning("Error","El nombre wl presio y las cantidades del producto son requeridos")
                    return
                """if caja_i_nombre.get()== "Nombre" or caja_i_presio.get() == "Precio" or caja_i_cantidad.get() == "Cantidad" or caja_i_porsentage.get() == "Porsentage" or caja_i_fecha_vencimiento.get()  == "Fecha vencimiento" or caja_i_fecha_alerta_antes_devencer.get() == "Mes antelacion" or caja_i_descuento.get() == "Descuento" or caja_i_cantidad_dar_descuento.get() =="Cantidad descuento":
                   mb.showwarning("Error","Todos los datos son requeridos")
                   return"""
                if len(caja_i_fecha_vencimiento.get()) != 10:
                    mb.showwarning("Error","La caja de la fecha nesesita que se inserten 10 digitos use / para separar ejemplo: 01/06/2023   primero el dia despues el mes y despues el año")
                    return

                porcentage=float(caja_i_porsentage.get()) / 100 * float(caja_i_presio.get())
                caja_i_nuevo_presio= float(caja_i_presio.get()) + porcentage
                parameters = (caja_i_nombre.get(), caja_i_nuevo_presio, caja_i_cantidad.get(), caja_i_fecha_vencimiento.get(),caja_i_presio.get(),
                               caja_i_fecha_alerta_antes_devencer.get(), caja_i_descuento.get(),
                              caja_i_cantidad_dar_descuento.get())
                query="insert into product values(NULL, ?, ?, ?, ?, ?, ?,?,?)"
                ConecionSql().run_query(query,parameters)
                """Limpiamos todas las cajas"""
                on_entry_click_nombre("")
                on_entry_click_precio("")
                on_entry_click_cantidad("")
                on_entry_click_porsentage("")
                on_entry_click_fecha_vencimiento("")
                on_entry_click_fecha_alerta_antes_devencer("")
                on_entry_click_descuento("")
                on_entry_click_cantidad_descuento("")
                InsertandoDatosDeLasCajas()
                octener_todos_los_productos()
                mb.showinfo("Exito","El producto se a guardado en la base de dato")

            def ProductosApuntoAgotarse():
                query="Select name,cantidad from product WHERE cantidad < 10"
                dato=ConecionSql().run_query(query,).fetchall()
                query = "Select name,cantidad from product WHERE cantidad == 0"
                dato2 = ConecionSql().run_query(query, ).fetchall()
                recorrer=lista_todos_los_datos_productos.get_children()
                for r in recorrer:
                        lista_todos_los_datos_productos.delete(r)



                for d in dato:
                   if int(d[1]) > 0:
                     padre=lista_todos_los_datos_productos.insert("",END,text=d[0],values=('','',d[1],))

                for d in dato:
                   if int(d[1])== 0:
                    lista_todos_los_datos_productos.insert(padre,'end',text=d[0],values=('','',d[1],))

            def MirandoQueProductoSeEstanPorCaducar():

                    # Crea una etiqueta para elementos mayores que cero
                    lista_todos_los_datos_productos.tag_configure('positive', foreground='green')

                    # Crea una etiqueta para elementos menores que cero
                    lista_todos_los_datos_productos.tag_configure('negative', foreground='red')

                    # Intenta ejecutar el código siguiente

                    # Consulta a la base de datos para obtener el nombre, fecha de vencimiento y fecha de alerta de vencimiento de todos los productos
                    query = "SELECT name, fecha_vencimiento, mesProximoDevovlucion FROM product"
                    # Ejecuta la consulta y almacena los resultados en la variable "datoss"
                    datoss = ConecionSql().run_query(query).fetchall()
                    # Recorre todos los elementos en la tabla "tabla_detalles_producto"
                    recoriendo = lista_todos_los_datos_productos.get_children()
                    for r in recoriendo:
                        # Elimina cada elemento de la tabla
                        lista_todos_los_datos_productos.delete(r)
                    # Recorre cada fila de los resultados de la consulta
                    for datos in datoss:
                        # Obtiene la fecha actual y la fecha de alerta de vencimiento
                        fechaActual = OctenerFecha()[1]
                        fechaAlerta = datos[2]
                        # Almacena la fecha de vencimiento como una cadena de texto y la formatea para poder compararla con la fecha actual
                        fechaVencimiento = str(datos[1])
                        if len(fechaVencimiento) != 10  :
                            print("repi")
                            continue
                        try:
                            int(fechaAlerta)
                        except: continue
                        fvr = str(fechaVencimiento.replace("/", " "))
                        fvrl = fvr.split()
                        # Formatea la fecha actual para poder compararla con la fecha de vencimiento
                        far = str(fechaActual.replace("-", " "))
                        farl = far.split()
                        print(farl[2])
                        print(fvrl[2])
                        try:
                            farl[2]
                        except : continue
                        # Si el año de la fecha de vencimiento es mayor o igual al año actual, entonces se comparan el mes y el día
                        if fvrl[2] >= farl[2]:
                            # Si el año y el mes son iguales, entonces se determina si el producto está por vencerse comparando la diferencia entre el mes y día de la fecha de vencimiento y la fecha actual con la fecha de alerta de vencimiento

                            if fvrl[2] == farl[2]:
                                r = int(fvrl[1]) - int(farl[1])
                                c = r - int(fechaAlerta)
                                if c <= int(fechaAlerta):
                                    # Si el producto está por vencerse, se agrega a la tabla "tabla_detalles_producto"
                                    lista_todos_los_datos_productos.insert("", END, text=datos[0], values=('', '', datos[1],))

                            # Si el año de la fecha de vencimiento es mayor al año actual, entonces se determina si el producto está por vencerse comparando la diferencia entre el mes y día de la fecha de vencimiento y la fecha actual con la fecha de alerta de vencimiento
                            elif fvrl[2] > farl[2]:
                                r = 12 - int(farl[1])
                                f = r + int(fvrl[1])
                                if f <= int(fechaAlerta):
                                    # Si el producto está por vencerse, se agrega a la tabla "tabla_detalles_producto"
                                    lista_todos_los_datos_productos.insert("", END, text=datos[0], values=('', '', datos[1],))
                        # Si la fecha de vencimiento es menor al año actual, entonces se agrega el producto a la tabla sin comprobar si está por vencerse o no
                        elif fvrl[2] < farl[2]:
                            lista_todos_los_datos_productos.insert("", END, text=datos[0], values=('', '', datos[1],))
                            print("fin")



            def RadioButoonAdministrarProducto():
                if valor.get() == 1:
                    ProductosApuntoAgotarse()
                elif valor.get() == 2:
                    MirandoQueProductoSeEstanPorCaducar()
                else: octener_todos_los_productos()




            # Define las función que se ejecutará al hacer clic en la entrada
            def on_entry_click_nombre(event):
                # Borra el texto de la entrada
                if bt_i_insertar_nuevo_producto.cget("text") != "Actualizar":
                    caja_i_nombre.delete(0, END)
            def on_entry_click_precio(event):
                if bt_i_insertar_nuevo_producto.cget("text") != "Actualizar":
                    # Borra el texto de la entrada
                     caja_i_presio.delete(0, END)
            def on_entry_click_cantidad(event):
                if bt_i_insertar_nuevo_producto.cget("text") != "Actualizar":
                    # Borra el texto de la entrada
                    caja_i_cantidad.delete(0, END)
            def on_entry_click_porsentage(event):
                if bt_i_insertar_nuevo_producto.cget("text") != "Actualizar":
                    # Borra el texto de la entrada
                    caja_i_porsentage.delete(0, END)
            def on_entry_click_descuento(event):
                if bt_i_insertar_nuevo_producto.cget("text") != "Actualizar":
                  # Borra el texto de la entrada
                  caja_i_descuento.delete(0, END)
            def on_entry_click_cantidad_descuento(event):
                if bt_i_insertar_nuevo_producto.cget("text") != "Actualizar":
                 # Borra el texto de la entrada
                 caja_i_cantidad_dar_descuento.delete(0, END)
            def on_entry_click_fecha_vencimiento(event):
                # Borra el texto de la entrada
                caja_i_fecha_vencimiento.delete(0, END)
            def on_entry_click_fecha_alerta_antes_devencer(event):
                if bt_i_insertar_nuevo_producto.cget("text") != "Actualizar":
                 # Borra el texto de la entrada
                 caja_i_fecha_alerta_antes_devencer.delete(0, END)

            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            labelframe1=LabelFrame(f2,bg="black")
            labelframe1.place(x=30, y=0)

            caja_i_nombre = ttk.Entry(labelframe1)
            caja_i_nombre.grid(row=0,column=0,padx=10,pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_nombre.bind("<FocusIn>",on_entry_click_nombre)

            caja_i_presio = ttk.Entry(labelframe1)
            caja_i_presio.grid(row=0, column=1,padx=10,pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_presio.bind("<FocusIn>", on_entry_click_precio)

            caja_i_cantidad = ttk.Entry(labelframe1)
            caja_i_cantidad.grid(row=0, column=2,padx=10,pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_cantidad.bind("<FocusIn>", on_entry_click_cantidad)

            caja_i_porsentage = ttk.Entry(labelframe1)
            caja_i_porsentage.grid(row=0, column=3,padx=10,pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_porsentage.bind("<FocusIn>", on_entry_click_porsentage)

            caja_i_fecha_vencimiento = ttk.Entry(labelframe1)
            caja_i_fecha_vencimiento.grid(row=1, column=0, padx=10, pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_fecha_vencimiento.bind("<FocusIn>", on_entry_click_fecha_vencimiento)

            caja_i_fecha_alerta_antes_devencer = ttk.Entry(labelframe1)
            caja_i_fecha_alerta_antes_devencer.grid(row=1, column=1, padx=10, pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_fecha_alerta_antes_devencer.bind("<FocusIn>", on_entry_click_fecha_alerta_antes_devencer)

            caja_i_descuento = ttk.Entry(labelframe1)
            caja_i_descuento.grid(row=1, column=2,padx=10,pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_descuento.bind("<FocusIn>", on_entry_click_descuento)


            caja_i_cantidad_dar_descuento = ttk.Entry(labelframe1)
            caja_i_cantidad_dar_descuento.grid(row=1, column=3,padx=10,pady=10)
            # Asigna la función al evento "FocusIn" de la entrada
            caja_i_cantidad_dar_descuento.bind("<FocusIn>", on_entry_click_cantidad_descuento)

            InsertandoDatosDeLasCajas()

            bt_i_insertar_nuevo_producto = Button(labelframe1,text="Insertar",bg="black",fg='green',width=17,command=CambiarEstadoBotonProduct)
            if permiso_usr == 'root':
                bt_i_insertar_nuevo_producto.grid(row=2,column=1,sticky="nsew")

            lista_todos_los_datos_productos=ttk.Treeview(f2, height=18, columns=("#0", "#1",'#2','#3','#4','#5','#6'))
            lista_todos_los_datos_productos.place(x=30,y=130)
            lista_todos_los_datos_productos.heading('#0', text='Nombre', anchor=CENTER)
            lista_todos_los_datos_productos.column('#0', width=600)
            lista_todos_los_datos_productos.heading('#1', text='Presio con ganacia', anchor=CENTER)
            lista_todos_los_datos_productos.column('#1', width=120)
            lista_todos_los_datos_productos.heading('#2', text='presio sin ganacia', anchor=CENTER)
            lista_todos_los_datos_productos.column("#2", width=110)
            lista_todos_los_datos_productos.heading('#3', text='Cantidad', anchor=CENTER)
            lista_todos_los_datos_productos.column("#3", width=100)
            lista_todos_los_datos_productos.heading('#4', text='Fecha vencimiento', anchor=CENTER)
            lista_todos_los_datos_productos.column("#4", width=100)
            lista_todos_los_datos_productos.heading('#5', text='Alerta antes del v', anchor=CENTER)
            lista_todos_los_datos_productos.column("#5", width=100)
            lista_todos_los_datos_productos.heading('#6', text='Descuento', anchor=CENTER)
            lista_todos_los_datos_productos.column("#6", width=100)
            lista_todos_los_datos_productos.heading('#7', text='cantidad aplicar d', anchor=CENTER)
            lista_todos_los_datos_productos.column("#7", width=100)
            octener_todos_los_productos()

            caja_buscar_todos_productos=ttk.Entry(f2,width=27,font=('bold'))
            caja_buscar_todos_productos.place(x=30,y=707)
            caja_buscar_todos_productos.bind("<KeyRelease>", BuscarTodosLosProductos)
            caja_buscar_todos_productos.focus()
            caja_buscar_todos_productos.config(font=("Arial", 20, "bold"))

            valor = IntVar()
            rd_p_agotados= ttk.Radiobutton(f2,text="Productos agotados",variable=valor, value=1,command=RadioButoonAdministrarProducto)
            rd_p_agotados.place(x=565,y=707)
            rd_p_apunto_de_vencer = ttk.Radiobutton(f2, text="Productos vencidos o apunto de vencer",variable=valor, value=2,command=RadioButoonAdministrarProducto)
            rd_p_apunto_de_vencer.place(x=728, y=707)
            rd_p_apunto_de_vencer = ttk.Radiobutton(f2, text="Todos los productos", variable=valor, value=3,command=RadioButoonAdministrarProducto)
            rd_p_apunto_de_vencer.place(x=1028, y=707)

            # Menu ppo____________________________________________
            if permiso_usr == 'root':
                popup = Menu(f2, tearoff=0)

                # Adding Menu Items
                popup.add_command(label="Actualizar", command=ActualizarProducto)
                popup.add_separator()
                popup.add_command(label="Borrar", command=BorrarProducto)

                def menu_popup(event):
                    # display the popup menu
                    try:
                        popup.tk_popup(event.x_root, event.y_root, 0)
                    finally:
                        # Release the grab
                        popup.grab_release()

                lista_todos_los_datos_productos.bind("<Button-3>", menu_popup)
            # END_Menu ppo____________________________________________



            toggle_win()


        def Clientes():
            def OctenerClientes():
                query="SELECT * FROM credito"
                dato=ConecionSql().run_query(query)
                recorer = tabla_clientes.get_children()
                # LIMPIAMOS TABLA CLIENTE
                for r in recorer:
                    tabla_clientes.delete(r)

                for row in dato:
                    tabla_clientes.insert('',0,text=row[1],values=(row[2],row[4]))



            def OctenerProductosFiados(event):
                c=tabla_clientes.selection()
                cc=tabla_clientes.item(c)['text']
                print(cc)
                query="SELECT * FROM credito where nombre= ?"
                parameters=(cc,)
                dato=ConecionSql().run_query(query,parameters).fetchall()[0][5]
                print(dato)

                query="SELECT * FROM product_en_creditos WHERE codigo_cliente = ?"
                parameters=(dato,)
                dato1=ConecionSql().run_query(query,parameters).fetchall()
                recorer= tabla_detalles_credito_clientes.get_children()

                for r in recorer:
                    tabla_detalles_credito_clientes.delete(recorer)

                for row in dato1:
                    tabla_detalles_credito_clientes.insert('',0,text=row[1],values=(row[2],row[5],row[3]))

                print(dato1)

            def BorrarCliente():
                c=tabla_clientes.selection()
                dato= tabla_clientes.item(c)['text']
                print(dato,'jjj')
                query="DELETE from credito where nombre= ?"
                parameters = (dato,)
                resultado= mb.askokcancel('Advertencia','Seguro que quieres borrar un cliente')
                if resultado:
                    ConecionSql().run_query(query,parameters)
                    OctenerClientes()
                else:print("Se a canselado la eliminacion")

            def SaldarDeuda():

                def Pago():
                    pg = float(ppago.get())
                    dud = float(deudor)
                    resta = dud - pg
                    if resta < 0:
                        resta = resta = 0
                    if dud == 0:
                        vte_pagar_deuda.destroy()
                        mb.showinfo('Error', 'El cliente no debe nada')
                        return
                    resta = '{0:.2f}'.format(resta)
                    print(resta, apellido)
                    query = "UPDATE credito SET deuda =? where nombre=? and apellido= ?"
                    parameters = (resta, nombre, apellido)
                    ConecionSql().run_query(query, parameters)
                    vte_pagar_deuda.destroy()
                    mb.showinfo("Exito✅", "Se a saldado la cuenta")
                    OctenerClientes()
                    query = "select codigo from credito where nombre =? and apellido= ?"
                    trallendo_nombre = ConecionSql().run_query(query, parameters=(nombre, apellido)).fetchall()[0][0]
                    query = "select nombre,precio from product_en_creditos where codigo_cliente = ?"
                    trallendo_datos = ConecionSql().run_query(query, parameters=(trallendo_nombre,)).fetchall()
                    usr = nombre_usr

                    hr().registroCredito(trallendo_datos, parametros=(nombre, apellido, usr, dud, pg, resta, trallendo_nombre))


                item=tabla_clientes.selection()
                try:
                   tabla_clientes.item(item)["values"][1]
                except IndexError as e:
                    mb.showinfo("Error🚫", "Selecione a un deudor")
                    return
                deudor=tabla_clientes.item(item)["values"][1]
                nombre=tabla_clientes.item(item)["text"]
                apellido=tabla_clientes.item(item)["values"][0]

                vte_pagar_deuda= Toplevel()
                print(apellido)
                vte_pagar_deuda.title("Pagar deuda")

                #DEUDA
                Label(vte_pagar_deuda,text="Nombre").grid(row=0,column=0,padx=10,pady=5)
                Entry(vte_pagar_deuda,textvariable=StringVar(vte_pagar_deuda,value=nombre),state="readonly").grid(row=0,column=1,padx=10)

                Label(vte_pagar_deuda,text="Deuda").grid(row=1,column=0,padx=10,pady=5)
                Entry(vte_pagar_deuda,textvariable=StringVar(vte_pagar_deuda,value=deudor),state="readonly").grid(row=1,column=1,padx=10)


                #PAGO
                Label(vte_pagar_deuda,text="Pagar$").grid(row=2,column=0,padx=10,pady=5)
                ppago=ttk.Entry(vte_pagar_deuda)
                ppago.grid(row=2,column=1,padx=10)
                ttk.Button(vte_pagar_deuda, text="Aceptar", command=Pago).grid(row=3, column=1, sticky=W,padx=5)
                vte_pagar_deuda.mainloop()
                print("fin")


            def InsertarNevouCliente():
                if caja_nombre_cliente.get() == "" or caja_apellido_cliente.get() == "" or caja_sexo_cliente.get() == "" or caja_cantidad_max_f_cliente.get() == "":
                    mb.showwarning("Error","Todos los datos son nesesarios")
                    return
                if caja_nombre_cliente.get() == "Nombre" or caja_apellido_cliente.get() == "Apellido" or caja_cantidad_max_f_cliente.get() == "Cantidad Max Credito":
                    mb.showwarning("Error","Todos los datos son nesesarios")
                    return
                if  caja_cantidad_max_f_cliente.get() != "Hombre" or caja_cantidad_max_f_cliente.get() !=  "Mujer" or caja_cantidad_max_f_cliente.get() != "Otros":
                    mb.showwarning("Error")
                def generate_code(name, lastname):
                    # Concatenar nombre, apellido y fecha de ingreso
                    string_to_hash = name + lastname + OctenerFecha()[1]
                    # Crear una función de hash SHA-256
                    hasher = hashlib.sha256()
                    # Actualizar la función de hash con la cadena concatenada
                    hasher.update(string_to_hash.encode('utf-8'))
                    # Obtener un valor numérico único
                    unique_value = hasher.hexdigest()
                    # Generar un número aleatorio entre 0 y 999
                    random_number = random.randint(0, 999)
                    # Concatenar el valor numérico único y el número aleatorio
                    code = unique_value[:10] + str(random_number).zfill(3)
                    return code

                name = caja_nombre_cliente.get()
                lastname = caja_apellido_cliente.get()
                codigo = generate_code(name, lastname)
                query= "INSERT INTO credito VALUES(NULL,?,?,?,?,?,NULL,?) "
                parameters=(caja_nombre_cliente.get(),caja_apellido_cliente.get(),caja_sexo_cliente.get(),0,codigo,caja_cantidad_max_f_cliente.get())
                ConecionSql().run_query(query,parameters)
                mb.showinfo("Exito","El cliente se inserto en la base de datos")
                OctenerClientes()
                InsertandoDatosDeLasCajasClientes()

            def InsertandoDatosDeLasCajasClientes():
                caja_nombre_cliente.insert(0,'Nombre')
                caja_apellido_cliente.insert(0,'Apellido')
                caja_cantidad_max_f_cliente.insert(0,'Cantidad Max Credito')

            # Define las función que se ejecutará al hacer clic en la entrada
            def on_entry_click_cliente_nombre(event):
                # Borra el texto de la entrada
                   caja_nombre_cliente.delete(0, END)
            def on_entry_click_cliente_apellido(event):
                # Borra el texto de la entrada
                   caja_apellido_cliente.delete(0, END)
            def on_entry_click_cliente_cantadadfiado(event):
                # Borra el texto de la entrada
                   caja_cantidad_max_f_cliente.delete(0, END)

            def Menuppo():
                # Menu ppo
                popup = Menu(f2, tearoff=0)
                var = BooleanVar()

                # Adding Menu Items
                popup.add_command(label="Actualizar", command='')
                popup.add_command(label="Borrar", command=BorrarCliente)
                popup.add_command(label="Mostrar detalles del credito")
                popup.add_command(label="Saldar deuda",command=SaldarDeuda)
                popup.add_separator()
                popup.add_checkbutton(label="Estado del cliente", variable=var)
                popup.config(bg='blue')


                def on_check(var_name, element_name, op):
                    if var.get():
                        print("Checkbutton activado")
                    else:
                        print("Checkbutton desactivado")

                var.trace("w", on_check)

                def menu_popup(event):
                    # display the popup menu
                    try:
                        popup.tk_popup(event.x_root, event.y_root, 0)
                    finally:
                        # Release the grab
                        popup.grab_release()

                tabla_clientes.bind("<Button-3>", menu_popup)





            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            toggle_win()

            labelframe1 = LabelFrame(f2, bg="black")
            labelframe1.place(x=30, y=20)

            caja_nombre_cliente= ttk.Entry(labelframe1)
            caja_nombre_cliente.grid(row=0,column=0,padx=10,pady=10)
            caja_nombre_cliente.bind("<FocusIn>", on_entry_click_cliente_nombre)

            caja_apellido_cliente = ttk.Entry(labelframe1)
            caja_apellido_cliente.grid(row=0, column=1,padx=10,pady=10)
            caja_apellido_cliente.bind("<FocusIn>", on_entry_click_cliente_apellido)

            valor=['Hombre','Mujer','Otros']
            caja_sexo_cliente = ttk.Combobox(labelframe1,values=valor)
            caja_sexo_cliente.grid(row=0, column=2,padx=10,pady=10)

            caja_cantidad_max_f_cliente = ttk.Entry(labelframe1)
            caja_cantidad_max_f_cliente.grid(row=0, column=3,padx=10,pady=10)
            caja_cantidad_max_f_cliente.bind("<FocusIn>", on_entry_click_cliente_cantadadfiado)

            bt_i_cliente= Button(labelframe1,text="Guardar cliente",command=InsertarNevouCliente).grid(row=1,column=2,padx=10,pady=10)

            tabla_clientes= ttk.Treeview(f2,height=18, columns=('#1', '#2'))
            tabla_clientes.place(x=10,y=150)
            tabla_clientes.heading('#0',text="nombre",anchor=CENTER)
            tabla_clientes.column('#0',width=190)
            tabla_clientes.heading('#1',text="Apellido",anchor=CENTER)
            tabla_clientes.column('#1',width=190)
            tabla_clientes.heading('#2', text="Deuda", anchor=CENTER)
            tabla_clientes.column('#2', width=100)
            OctenerClientes()
            tabla_clientes.bind('<Double-Button-1>', OctenerProductosFiados)

            InsertandoDatosDeLasCajasClientes()

            tabla_detalles_credito_clientes= ttk.Treeview(f2,height=18,columns=('#1', '#2', '#3','#4'))
            tabla_detalles_credito_clientes.place(x=493,y=150)
            tabla_detalles_credito_clientes.heading('#0',text="Productos", anchor=CENTER)
            tabla_detalles_credito_clientes.column('#0',width=375)
            tabla_detalles_credito_clientes.heading('#1',text='presio')
            tabla_detalles_credito_clientes.column('#1',width=80)
            tabla_detalles_credito_clientes.heading('#2',text='cantidad',anchor=CENTER)
            tabla_detalles_credito_clientes.column('#2',width=80)
            tabla_detalles_credito_clientes.heading('#3',text='Fecha',anchor=CENTER)
            tabla_detalles_credito_clientes.column('#3',width=80)
            tabla_detalles_credito_clientes.heading('#4', text='SubTotal', anchor=CENTER)
            tabla_detalles_credito_clientes.column('#4', width=80)

            Menuppo()

        def Registro():
            def OctenerRegistro():
                recorer = tree.get_children()
                for r in recorer:
                    tree.delete(r)
                query="SELECT * from registro_ventas fecha"
                datos=ConecionSql().run_query(query,)
                # Insertar los datos de la tabla en el TreeView
                for producto in datos:
                   tree.insert("", "end", text=producto[1],values=( producto[2], producto[3], producto[4],producto[5],producto[6]))





            def BuscarRegistro():
                recorer = tree.get_children()
                for r in recorer:
                    tree.delete(r)
                fecha=year_entry.get()+"-"+month_entry.get()+"-"+day_entry.get()+"-"+hour_entry.get()+"%"
                query="SELECT * FROM registro_ventas  WHERE fecha LIKE ?"
                parameters=(fecha,)
                datos=ConecionSql().run_query(query,parameters).fetchall()
                print(datos)
                for producto in datos:
                    tree.insert("", "end", text=producto[1],
                                values=( producto[2], producto[3], producto[4],producto[5],producto[6]))

                query="SELECT SUM(precio) FROM registro_ventas WHERE fecha LIKE ?"
                parameters=(fecha,)
                datos2=ConecionSql().run_query(query,parameters).fetchall()

                datos2=datos2[0]

                datos2=str(datos2[0])
                print(datos2)
                lb_total=Label(f2,text="Total: "+datos2,font=26).place(x=10,y=730)

            def DetallesVentas():
                def InDatosScrollText():
                    fecha=OctenerFecha()[1]
                    nombre_archivo= fecha+".txt"
                    with open("registro/facturas/"+nombre_archivo,"r",encoding='UTF-8') as ruta:
                        ruta=ruta.read()
                        scrolledtext1.delete("1.0", "20000.0")
                        scrolledtext1.insert("1.0",ruta)



                vte_detalles_ventas=Toplevel()
                vte_detalles_ventas.resizable(False, False)
                vte_detalles_ventas.title("Registro Factura")
                scrolledtext1=st.ScrolledText(vte_detalles_ventas, width=94, height=23)
                scrolledtext1.grid(row=0,column=1)
                InDatosScrollText()
                vte_detalles_ventas.mainloop()




            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            labelframe=ttk.LabelFrame(f2,text="Buscar registro", )

            labelframe.place(x=1120,y=50)

            # Crear un TreeView
            tree = ttk.Treeview(f2,height=23)

            # Establecer las columnas del TreeView
            tree["columns"] = ( "Precio", "Fecha_venta", "Vendedor","Cantidad","Identificador")

            # Establecer el encabezado de las columnas
            tree.heading("#0", text="Nombre")
            tree.heading("Precio", text="Precio")
            tree.heading("Fecha_venta", text="Fecha de Venta")
            tree.heading("Vendedor", text="Vendedor")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Identificador", text="Identificador")


            # Establecer el ancho de las columnas
            tree.column("#0", width=400)
            tree.column("Precio", width=80)
            tree.column("Fecha_venta", width=200)
            tree.column("Vendedor", width=200)
            tree.column("Cantidad", width=100)
            tree.column("Identificador", width=100)

            # Empaquetar el TreeView
            tree.place(x=10,y=10)

            #lb_total["text"]= "Total:  {}".format(datos2)

            OctenerRegistro()

            year_label = Label(labelframe, text="Año:")
            year_label.grid(row=0, column=0)

            year_entry = ttk.Entry(labelframe)
            year_entry.grid(row=0, column=1)

            month_label = Label(labelframe, text="Mes:")
            month_label.grid(row=1, column=0)

            month_entry = ttk.Entry(labelframe)
            month_entry.grid(row=1, column=1)

            day_label = Label(labelframe, text="Dia:")
            day_label.grid(row=2, column=0)

            day_entry = ttk.Entry(labelframe)
            day_entry.grid(row=2, column=1)

            hour_label = Label(labelframe, text="Hora:")
            hour_label.grid(row=3, column=0)

            hour_entry = Entry(labelframe)
            hour_entry.grid(row=3, column=1)

            submit_button = Button(labelframe, text="Buscar", command=BuscarRegistro)
            submit_button.grid(row=4, column=1)

            Detalles_Venta= Button(f2,text="Detalles de ventas",command=DetallesVentas).place(x=1120,y=250)


            toggle_win()

        def Notificaciones():
            def OctenerNotificaciones():
                query="SELECT * from notificaciones"
                dato=ConecionSql().run_query(query,).fetchall()
                records = tabla_notificaciones.get_children()
                for i in records:
                    tabla_notificaciones.delete(0,END)
                for r in dato:
                    s=r[0]+" "+r[1]
                    tabla_notificaciones.insert("",0,text=s)

            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            tabla_notificaciones= ttk.Treeview(f2,height=24)
            tabla_notificaciones.heading('#0',text='Notificaciones')
            tabla_notificaciones.column('#0',widt=1440)
            tabla_notificaciones.place(x=0,y=0)
            OctenerNotificaciones()
            toggle_win()



        def Ajustes():
            def Dollar():

                def ConsultandoPresioAPI():
                    import requests
                    headers = {"apikey": "82jpOtQTn58eKCJM4K1QB2SKT6RiiDG7"}
                    params = {"to": "NIO", "from": "USD", "amount": 1}

                    try:
                        response = requests.get("https://api.apilayer.com/exchangerates_data/convert", headers=headers,
                                                params=params)
                        if response.status_code != 200:
                            raise ValueError("Error al obtener el tipo de cambio: " + response.text)

                        data = response.json()

                        tipo_cambio = data["result"]

                        print(f"1 Dolar = {tipo_cambio} Cordobas")
                        return  tipo_cambio
                    except :
                        mb.showerror("Error","No se pudo octener el presio del dollar verifique su conexion")
                        conexion=" Error de conexion"
                        return conexion

                def ActualizandoDollar():
                    dll = str(caja_dollar.get())
                    query = "UPDATE configuraciones SET  atributos=? WHERE nombre_cf=?"
                    dollar = "dollar"
                    parameters = (dll, dollar)

                    ConecionSql().run_query(query, parameters)
                    vte_ajustar_dolar.destroy()
                    mb.showinfo("Exito", "El precio del dollar se a actualisado")

                cpd=ConsultandoPresioAPI()
                vte_ajustar_dolar = Toplevel()
                vte_ajustar_dolar.geometry("300x200")
                vte_ajustar_dolar.title("Ajustar presio del Dollar")
                lb_presio_actual=Label(vte_ajustar_dolar,text="Presio actual del dolar: "+str(cpd)).place(x=5,y=5)

                query = "SELECT atributos FROM configuraciones  WHERE nombre_cf='dollar'"
                precio_dollar =ConecionSql().run_query(query, ).fetchall()[0]
                lb_precio_anterior_dollar = Label(vte_ajustar_dolar, text='Precio anterior').place(x=5,y=25)

                caja_precio_anterior_dollar = ttk.Entry(vte_ajustar_dolar)
                caja_precio_anterior_dollar.insert('', precio_dollar)
                caja_precio_anterior_dollar['state'] = "readonly"
                caja_precio_anterior_dollar.place(x=100,y=25)

                lb_nuevo_precio_dollar = Label(vte_ajustar_dolar, text='Nuevo precio').place(x=5,y=45)
                caja_dollar = ttk.Entry(vte_ajustar_dolar)
                caja_dollar.place(x=100,y=45)
                Button(vte_ajustar_dolar, text="Actualizar", command=ActualizandoDollar).place(x=100,y=75)

                vte_ajustar_dolar.mainloop()

            def EditarInterfas():
                def CambiarColor(event):
                    dato1='color_menu'
                    query="UPDATE configuraciones SET  atributos=? WHERE nombre_cf=?"
                    dato=caja_color_menu.get()
                    print(dato)
                    parameters=(dato,dato1)
                    ConecionSql().run_query(query,parameters)
                    caja_color_menu.delete(0,END)

                vte_editar_programa=Toplevel()
                vte_editar_programa.title("Editar estilo del programa")
                vte_editar_programa.resizable(0,0)

                lb_color_fondo=Label(vte_editar_programa,text="Color del fondo").grid(row=0,column=0)
                caja_color_fondo=ttk.Entry(vte_editar_programa)
                caja_color_fondo.grid(row=0,column=1)

                lb_color_heder=Label(vte_editar_programa,text="Color de la barra de arriba").grid(row=1,column=0)
                caja_color_heder=ttk.Entry(vte_editar_programa)
                caja_color_heder.grid(row=1,column=1)

                lb_color_menu=Label(vte_editar_programa,text="Color del menu").grid(row=2,column=0)
                caja_color_menu=ttk.Entry(vte_editar_programa)
                caja_color_menu.grid(row=2,column=1)
                caja_color_menu.bind('<Return>', CambiarColor)

                vte_editar_programa.mainloop()


            def Usuarios():
                def OctenerUsuarios():
                    records = tabla_detalles_usuarios.get_children()
                    for elementos in records:
                        tabla_detalles_usuarios.delete(elementos)

                    query = "SELECT * from usuario"
                    usuarios = ConecionSql().run_query(query, ).fetchall()

                    for usr in usuarios:
                        tabla_detalles_usuarios.insert("", 0, text=usr[1], value=(usr[2], usr[3], usr[4], usr[5], usr[6]))

                def BorrarUsuario():
                    lista = tabla_detalles_usuarios.focus()
                    dato = tabla_detalles_usuarios.item(lista)
                    nombre_usr = dato['text']
                    apellido_usr = dato['values'][0]
                    print("BORRANO", apellido_usr, nombre_usr)
                    query = "DELETE from usuario WHERE nombre=? and apellido = ? "
                    parameters = (nombre_usr, apellido_usr)
                    ConecionSql().run_query(query, parameters)
                    OctenerUsuarios()



                def InsertarUsr():
                    # print(caja_nombre,caja_apellido,caja_numero_t,caja_numero_c,caja_contraseña,cbx_permiso)
                    query = "INSERT into usuario(nombre,apellido,numero_telefono,numero_cedula,contraseña,permisos) VALUES(?,?,?,?,?,?)"
                    parameters = (
                    caja_nombre.get(), caja_apellido.get(), caja_numero_t.get(), caja_numero_c.get(), caja_contraseña.get(), cbx_permiso.get())

                    ConecionSql().run_query(query, parameters)
                    OctenerUsuarios()





                vte_usuarios = Toplevel()
                labelframe1 = ttk.LabelFrame(vte_usuarios, text="Inserte Nuevo Usuario")
                labelframe1.grid(row=0, column=0, padx=20, pady=10)

                lb_nombre = Label(labelframe1, text="Inserte el nombre").grid(column=0, row=0)
                caja_nombre = ttk.Entry(labelframe1)
                caja_nombre.grid(row=0, column=1)

                lb_apellido = Label(labelframe1, text="Inserte el apellido").grid(column=2, row=0)
                caja_apellido = ttk.Entry(labelframe1)
                caja_apellido.grid(row=0, column=3)

                lb_numero_t = Label(labelframe1, text="Inserte el numero de telefono").grid(column=0, row=1)
                caja_numero_t = ttk.Entry(labelframe1)

                caja_numero_t.grid(row=1, column=1)

                lb_numero_c = Label(labelframe1, text="Inserte el numero de cedula").grid(column=2, row=1)
                caja_numero_c = ttk.Entry(labelframe1)
                caja_numero_c.grid(row=1, column=3)

                lb_contraseña = Label(labelframe1, text="Inserte la contraseña").grid(column=0, row=2)
                caja_contraseña = ttk.Entry(labelframe1)
                caja_contraseña.grid(row=2, column=1)

                lb_permiso = Label(labelframe1, text="Elija el tipo de permiso").grid(column=2, row=2)
                cbx_permiso = ttk.Combobox(labelframe1, values=['root', 'semi_root', 'usr_sinprevilegios'])
                cbx_permiso.grid(row=2, column=3)

                bt_agregar = ttk.Button(labelframe1, text="Agregar",
                                        command=InsertarUsr)
                bt_agregar.grid(row=3, column=1, pady=10, columnspan=2)

                # LABEL FRAME2 ////////////////////////

                labelframe2 = ttk.LabelFrame(vte_usuarios, text="Detalles de usuarios")
                labelframe2.grid(row=2, column=0)
                tabla_detalles_usuarios = ttk.Treeview(labelframe2, column=("#0", "#1", "#2", "#3", "#4"))
                tabla_detalles_usuarios.grid(row=0, column=0, columnspan=2)
                tabla_detalles_usuarios.column("#0", width=120)
                tabla_detalles_usuarios.column('#1', width=120)
                tabla_detalles_usuarios.column("#2", width=120)
                tabla_detalles_usuarios.column("#3", width=140)
                tabla_detalles_usuarios.column("#5", width=120)
                tabla_detalles_usuarios.heading("#0", text="Nombre", anchor=CENTER)
                tabla_detalles_usuarios.heading("#1", text="Apellido", anchor=CENTER)
                tabla_detalles_usuarios.heading("#2", text="Numero Telefono", anchor=CENTER)
                tabla_detalles_usuarios.heading("#3", text="Numero Cedula", anchor=CENTER)
                tabla_detalles_usuarios.heading("#4", text="Contraseña", anchor=CENTER)
                tabla_detalles_usuarios.heading("#5", text="Permiso", anchor=CENTER)
                OctenerUsuarios()




                # Menu ppo____________________________________________
                popup = Menu(f2, tearoff=0)

                # Adding Menu Items
                popup.add_command(label="Borrar", command=BorrarUsuario)
                popup.add_separator()
                popup.add_command(label="Actualizar", command='')

                def menu_popup(event):
                    # display the popup menu
                    try:
                        popup.tk_popup(event.x_root, event.y_root, 0)
                    finally:
                        # Release the grab
                        popup.grab_release()

                tabla_detalles_usuarios.bind("<Button-3>", menu_popup)
                # END_Menu ppo____________________________________________

            def NuevaContraseña(c):
                def cambiandoContra():

                        query = "UPDATE usuario SET contraseña=? WHERE contraseña=?"

                        parameters = (caja_contraseña_nueva.get(),c)
                        print(parameters)
                        ConecionSql().run_query(query, parameters)
                        mb.showinfo("Exito", "Se a cambiado la contraseña")
                        vt_cambiar_contra.destroy()

                vt_cambiar_contra = Toplevel()
                lb_nueva_contraseña = Label(vt_cambiar_contra, text="Nueva contraseña").grid(row=0, column=0,
                                                                                                      pady=5, padx=10)
                caja_contraseña_nueva = ttk.Entry(vt_cambiar_contra)
                caja_contraseña_nueva.grid(row=0, column=1, padx=10)
                bt_acectar = Button(vt_cambiar_contra, text="Acectar", command=cambiandoContra).grid(row=1, column=1, pady=5)
                vt_cambiar_contra.mainloop()

            def ContrsañaDelAdmin(dato):
                def Comprovando():
                    try:
                        query = "SELECT contraseña,permisos FROM usuario WHERE contraseña=?"
                        parameters = (caja_ingrese_contra.get(),)
                        octeniendo_contraseña = ConecionSql().run_query(query, parameters).fetchall()[0]
                        print(octeniendo_contraseña[1])
                        if octeniendo_contraseña[1] == 'root':
                            vte_comprovacion.destroy()
                            if dato == "usuario":
                               Usuarios()
                            elif dato == "cambiar":
                                NuevaContraseña(c=octeniendo_contraseña[0])
                            return True



                    except IndexError:
                        caja_ingrese_contra.delete(0, END)
                        vte_comprovacion.configure(background="red")
                        mb.showinfo("Error", "Contraseña incorrecta")
                        return False

                vte_comprovacion = Toplevel()
                vte_comprovacion.geometry("350x150")
                vte_comprovacion.resizable(0, 0)
                vte_comprovacion.title('Administrador')
                lb_ingrese_contraseña = Label(vte_comprovacion, text="Ingrese contraseña").grid(row=0, column=1, pady=0,
                                                                                                padx=10)
                lb_image_usuario = Label(vte_comprovacion, image=icon_seguridad).grid(row=1, column=0, padx=10)
                caja_ingrese_contra = ttk.Entry(vte_comprovacion, show="*")
                caja_ingrese_contra.grid(row=1, column=1, padx=20)
                caja_ingrese_contra.focus()

                bt_Acectar = Button(vte_comprovacion, text="Acectar", command=lambda: Comprovando()).grid(row=2, column=1,pady=5, padx=10)
                vte_comprovacion.mainloop()




            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            toggle_win()



            if permiso_usr == 'root':
                bt_dollar= Button(f2,text='Ajustar Presio del dollar',command=Dollar).place(x=350,y=200)
                bt_usuarios = Button(f2, text='Usuarios', command=lambda: ContrsañaDelAdmin(dato="usuario")).place(x=560, y=200)
            bt_cambiar_conytaseña = Button(f2, text="Cambiar contraseña", command=lambda :ContrsañaDelAdmin(dato="cambiar")).place(x=350,y=250)
            bt_estilos = Button(f2, text="Editar interfas", command=EditarInterfas).place(x=540, y=250)






        def toggle_win():
            global f1
            f1 = Frame(w, width=300, height=dimension_altura, bg=color_menu)
            f1.place(x=0, y=0)


            # buttons
            def bttn(x, y, text, bcolor, fcolor, cmd,icon_path):
                # Carga la imagen del ícono utilizando la clase PhotoImage de tkinter
                icon = ImageTk.PhotoImage(file=icon_path)
                def on_entera(e):
                    myButton1['background'] = bcolor  # ffcc66
                    myButton1['foreground'] = '#262626'  # 000d33

                def on_leavea(e):
                    myButton1['background'] = fcolor
                    myButton1['foreground'] = '#262626'

                myButton1 = Button(f1, text=text, width=180, height=50, fg='#262626',  highlightthickness=0,border=0, bg=fcolor, activeforeground='#262626', activebackground=bcolor, command=cmd, image=icon, compound=LEFT)
                myButton1.photo = icon
                myButton1.bind("<Enter>", on_entera)
                myButton1.bind("<Leave>", on_leavea)

                myButton1.place(x=x, y=y)

            bttn(0, 80 ,  'H O M E             ', color_menu, color_menu, home,"iconos/inicio.png")
            bttn(0, 132, 'FACTURAR             ', color_menu, color_menu, Facturar,"iconos/facturar.png")
            bttn(0, 184, 'PRODUCTO             ', color_menu, color_menu, AdministrarProduct,"iconos/database.png")
            bttn(0, 236, 'clientes             ', color_menu, color_menu, Clientes,"iconos/cliente.png")
            bttn(0, 288, 'REGISTRO             ', color_menu, color_menu, Registro,"iconos/facturar.png")
            bttn(0, 340, 'NOTIFICACIONES       ', color_menu, color_menu, Notificaciones, "iconos/notificacion.png")
            bttn(0, 392, 'AJUSTES              ', color_menu, color_menu, Ajustes, "iconos/ajuste.png")

            #
            def dele():
                f1.destroy()
                b2 = Button(w, image=img1,
                            command=toggle_win,
                            border=0,
                            bg='#262626',
                            activebackground='#262626')
                b2.place(x=0, y=0)

            global img2
            img2 = ImageTk.PhotoImage(Image.open("iconos/close.png"))

            Button(f1,
                   image=img2,
                   border=0,
                   highlightthickness=0,
                   command=dele,
                   bg=color_menu,
                   activebackground=color_menu).place(x=5, y=10)


        default_home()
        barra_superior=ttk.Frame(w).place(x=0,y=0)

        img1 = ImageTk.PhotoImage(Image.open("iconos/open.png"))

        global b2
        b2 = Button(barra_superior, image=img1,
                    command=toggle_win,
                    border=0,
                    highlightthickness=0,
                    bg='#262626',
                    activebackground='#262626')
        b2.place(x=0, y=0)

        lb_titulo= Label(barra_superior,text="Farmacia Soluciones",bd=0,font=20,bg=color_fondo,fg=color_fuente).place(x=70,y=12)
        lb_usuario = Label(barra_superior, text='Usuario: '+nombre_usr, bd=0, font=20, bg=color_fondo, fg=color_fuente).place(x=800, y=12)
        lb_usuario = Label(barra_superior, text="Total de hoy: ", bd=0, font=20, bg=color_fondo, fg=color_fuente).place(x=1100, y=12)
        w.protocol("WM_DELETE_WINDOW", on_closing)
        w.mainloop()








class verificar:

    def __init__(self):
        import ast
        import threading

        w = Tk()
        w.geometry('925x500')
        w.title('Login')
        w.configure(bg='#ff4f5a')
        w.minsize(925, 500)
        w.resizable(0, 0)


        def signin():
            signin_win = Frame(w, width=925, height=500, bg='white')
            signin_win.place(x=0, y=0)
            f1 = Frame(signin_win, width=350, height=350, bg='white')
            f1.place(x=480, y=100)

            global img1
            img1 = ImageTk.PhotoImage(Image.open("iconos_login/signin.png"))
            Label(signin_win, image=img1, border=0, bg='white').place(x=50, y=50)

            l2 = Label(signin_win, text="Farmasia Soluciones", fg='#ff4f5a', bg='white')
            l2.config(font=('Microsoft YaHei UI Light', 22, 'bold'))
            l2.place(x=500, y=100)

            """def on_enter(e):
                e1.delete(0,'end')    
            def on_leave(e):
                if e1.get()=='':   
                    e1.insert(0,'Username')"""

            """e1 =Entry(f1,width=25,fg='black',border=0,bg='white')
            e1.config(font=('Microsoft YaHei UI Light',11, ))
            e1.bind("<FocusIn>", on_enter)
            e1.bind("<FocusOut>", on_leave)
            e1.insert(0,'Username')
            e1.place(x=30,y=60)"""

            # Frame(f1,width=295,height=2,bg='black').place(x=25,y=87)

            # ------------------------------------------------------

            def on_enter(e):
                e2.delete(0, 'end')
                e2.config(show="*")

            def on_leave(e):
                if e2.get() == '':
                    e2.insert(0, 'Password')

            e2 = Entry(f1, width=21, fg='black', border=0, bg='white')
            e2.config(font=('Microsoft YaHei UI Light', 11,))
            e2.bind("<FocusIn>", on_enter)
            e2.bind("<FocusOut>", on_leave)
            e2.insert(0, 'Password')
            e2.place(x=30, y=130)

            Frame(f1, width=295, height=2, bg='black').place(x=25, y=157)

            # -mech------------------------------------------------

            def signin_cmd():

                """file=open('datasheet.txt','r')
                d=file.read()
                r=ast.literal_eval(d)
                file.close()"""

                from sql import Others as ConexionSql
                try:

                    query = "SELECT * FROM usuario where contraseña=?"
                    parameters = (e2.get(),)
                    datos = ConexionSql().run_query(query, parameters).fetchall()


                    if e2.get() == datos[0][5]:
                        nombre_usr=datos[0][1]
                        permiso_usr= datos[0][6]
                        mb.showinfo("", "     Bienvenida/o: "+nombre_usr)


                        w.destroy()
                        app = Inicio(nombre_usr,permiso_usr)

                except IndexError:
                    mb.showwarning("Error", "Contraseña incorrecta")




            # ------------------------------------------------------
            Button(f1, width=39, pady=7, text='Iniciar secion', bg='#ff4f5a', fg='white', border=0, command=signin_cmd).place(x=35,
                                                                                                                       y=204)
            """l1 = Label(f1, text="Don't have an account?", fg="black", bg='white')
            l1.config(font=('Microsoft YaHei UI Light', 9,))
            l1.place(x=75, y=250)"""

            """b2 = Button(f1, width=6, text='Sign up', border=0, bg='white', fg='#ff4f5a', command=signup)
            b2.place(x=215, y=250)"""

        def signup():
            signup_win = Frame(w, width=925, height=500, bg='white')
            signup_win.place(x=0, y=0)
            f1 = Frame(signup_win, width=350, height=350, bg='white')
            f1.place(x=480, y=70)

            global img2
            img2 = ImageTk.PhotoImage(Image.open("iconos/signup.png"))
            Label(signup_win, image=img2, border=0, bg='white').place(x=30, y=90)

            l2 = Label(signup_win, text="Sign up", fg='#ff4f5a', bg='white')
            l2.config(font=('Microsoft YaHei UI Light', 23, 'bold'))
            l2.place(x=600, y=60)

            def on_enter(e):
                e1.delete(0, 'end')

            def on_leave(e):
                if e1.get() == '':
                    e1.insert(0, 'Username')

            e1 = Entry(f1, width=25, fg='black', border=0, bg='white')
            e1.config(font=('Microsoft YaHei UI Light', 11,))
            e1.bind("<FocusIn>", on_enter)
            e1.bind("<FocusOut>", on_leave)
            e1.insert(0, 'Username')
            e1.place(x=30, y=60)

            Frame(f1, width=295, height=2, bg='black').place(x=25, y=87)

            # ------------------------------------------------------

            def on_enter(e):
                e2.delete(0, 'end')

            def on_leave(e):
                if e2.get() == '':
                    e2.insert(0, 'Password')

            e2 = Entry(f1, width=21, fg='black', border=0, bg='white')
            e2.config(font=('Microsoft YaHei UI Light', 11,))
            e2.bind("<FocusIn>", on_enter)
            e2.bind("<FocusOut>", on_leave)
            e2.insert(0, 'Password')
            e2.place(x=30, y=130)

            Frame(f1, width=295, height=2, bg='black').place(x=25, y=157)

            def on_enter(e):
                e3.delete(0, 'end')

            def on_leave(e):
                if e3.get() == '':
                    e3.insert(0, 'Confirm Password')

            e3 = Entry(f1, width=21, fg='black', border=0, bg='white')
            e3.config(font=('Microsoft YaHei UI Light', 11,))
            e3.bind("<FocusIn>", on_enter)
            e3.bind("<FocusOut>", on_leave)
            e3.insert(0, 'Confirm Password')
            e3.place(x=30, y=130 + 70)

            Frame(f1, width=295, height=2, bg='black').place(x=25, y=157 + 70)

            # Mechenism------------------------------------------------

            def signup_cmd():
                key = e1.get()
                value = e2.get()
                value2 = e3.get()

                if value == value2:
                    file = open('datasheet.txt', 'r+')
                    d = file.read()
                    r = ast.literal_eval(d)
                    print(r)

                    dict2 = {key: value}
                    print(dict2)
                    r.update(dict2)
                    print(r)
                    file.truncate(0)
                    file.close()
                    print(r)
                    file = open('datasheet.txt', 'w')
                    w = file.write(str(r))

                    mb.showinfo("", "     successfully signed up     ")

                else:
                    mb.showwarning('try again', 'password should match ')

            # -------------------------------------------------------
            Button(f1, width=39, pady=7, text='Sign up', bg='#ff4f5a', fg='white', border=0, command=signup_cmd).place(x=35,
                                                                                                                       y=204 + 60)
            l1 = Label(f1, text="Already have an account?", fg="black", bg='white')
            l1.config(font=('Microsoft YaHei UI Light', 9,))
            l1.place(x=70, y=250 + 63)

            b2 = Button(f1, width=6, text='Sign in', border=0, bg='white', fg='#ff4f5a', command=signin)
            b2.place(x=210, y=250 + 63)

        signin()  # default screen
        w.mainloop()




verificar()






