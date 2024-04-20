from tkinter import *

from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from datetime import datetime, timedelta
import hashlib
import random
import sys
import os
import calendar
from sql import Others as ConecionSql
from hora import creando_a_hora as hr

#pantalla= "microp"
pantalla="pc 1440x900"
#---------------------------------------------
if pantalla == "pc 1440x900":
    dimension_ancho= 1440
    dimension_altura=900
    dimension_ancho_frame = 1440
    dimension_altura_frame = 800
    tablas_factura_tamaño=5
    tabla_registro_tamaño=5
    label_frame_buscar_registro_x=1440
    dimencion_altura_tabla_detalles_credito_clientes=18
    dimension_treeview_altura_administrar_producto=16
    eje_y_widget_producto =665

elif pantalla == "lapto":
    dimension_ancho = 1440
    dimension_altura = 900
    dimension_altura = 750
    dimension_ancho_frame = 1440
    dimension_altura_frame = 700
    tablas_factura_tamaño=20
    tabla_registro_tamaño =20
    label_frame_buscar_registro_x=1440

elif pantalla == "microp":
    dimension_ancho = 1000
    # dimension_altura = 900
    dimension_altura = 750
    dimension_ancho_frame = 1440
    dimension_altura_frame = 700
    tablas_factura_tamaño = 20
    tabla_registro_tamaño = 20
    label_frame_buscar_registro_x = 1440


    dimension_treeview_altura_administrar_producto= 14
    dimencion_altura_tabla_detalles_credito_clientes = 15
    eje_y_widget_producto =598
    #----------------------------------------
    treview_factura1_x= 450
    treview_factura1_y= 300



#____________TREEVIEW_______________________________
class Funciones():
    def GeneraContraseña():
        # necessary imports
        import secrets
        import string

        # define the alphabet
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation

        alphabet = letters + digits + special_chars

        # fix password length
        pwd_length = 12

        # generate a password string
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))

        # generate password meeting constraints
        while True:
            pwd = ''
            for i in range(pwd_length):
                pwd += ''.join(secrets.choice(alphabet))

            if (any(char in special_chars for char in pwd) and
                    sum(char in digits for char in pwd) >= 2):
                break
        return pwd







funcion= Funciones

class Inicio():

    def __init__(self,nombre_usr,permiso_usr,nombre_negocio):


        query="select * from configuraciones where  nombre_cf ='color_tabla';"
        color_tablas=ConecionSql().run_query(query,).fetchall()[0][2]

        color_fondo='#1e1d23'
        color_fuente='white'
        query="select * from configuraciones where  nombre_cf ='color_menu';"
        color_menu= ConecionSql().run_query(query,).fetchall()[0][2]
        '#a9dfbf'
        print(color_fondo)
        w = Tk()
        if pantalla == "pc 1440x900":
            w.geometry('1400x750')
        elif pantalla == "lapto":
            #en milapto poener en 700
            w.geometry('1370x750')

        elif pantalla == "microp":
            #en milapto poener en 700
            w.geometry('1000x530')

        w.configure(bg=color_fondo)  # 12c4c0')
        w.resizable(0, 0)
        w.title('Toggle Menu')
        imagen_guardar = PhotoImage(file="iconos/guardar.png")
        imagen_facturar = PhotoImage(file="iconos/facturar.png")
        iccliente = ImageTk.PhotoImage(Image.open("iconos/cliente.png"))
        icon_usuario_m = ImageTk.PhotoImage(Image.open("iconos/icons8-male-user-64.png"))
        icon_usuario_f=ImageTk.PhotoImage(Image.open("iconos/usuario_femenino.png"))
        icon_seguridad=ImageTk.PhotoImage(Image.open("iconos/seguridad.png"))

        total_hoy = StringVar()
        ganancia_hoy = StringVar()






        # Creamos un estilo para el widget Treeview
        style = ttk.Style()

        # Establecemos el color de fondo del Treeview en amarillo
        style.configure("Treeview", background=color_tablas)

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
            def ProductosApuntoDeVencer():
                # Obtener la fecha actual
                fecha_actual = datetime.now()

                # Consulta a la base de datos para obtener la información de los productos
                query = "SELECT name, fecha_vencimiento, mesProximoDevovlucion FROM product"
                datos = ConecionSql().run_query(query).fetchall()

                # Lista para almacenar los productos a punto de vencer
                productos_apunto_de_vencer = []

                # Iterar sobre los datos de la base de datos
                for producto in datos:
                    nombre_producto, fecha_vencimiento, meses_proximo_vencimiento = producto

                    # Verificar si las fechas no están vacías y no son None
                    if fecha_vencimiento and meses_proximo_vencimiento and meses_proximo_vencimiento != 'None':
                        # Convertir las fechas de texto a objetos datetime
                        try:
                            fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
                            meses_proximo_vencimiento = int(meses_proximo_vencimiento)
                        except ValueError as e:
                            # Manejar la excepción (puedes imprimir un mensaje o hacer algo más)
                            print(f"Error al convertir fechas para el producto {nombre_producto}: {e}")
                            continue  # Continuar con el siguiente producto

                        # Calcular la fecha de alerta basada en meses_proximo_vencimiento
                        fecha_alerta = fecha_vencimiento - timedelta(days=30 * meses_proximo_vencimiento)

                        # Verificar si el producto está a punto de vencer
                        if fecha_actual > fecha_alerta and fecha_actual <= fecha_vencimiento:
                            productos_apunto_de_vencer.append(nombre_producto)
                            mb.showwarning("Producto Apunto de venserce",nombre_producto +": "+ str(fecha_vencimiento))

            try:
                ProductosApuntoDeVencer()
            except:
                mb.showerror("Algo fallo")


            color_home="#262626"

            f2 = Frame(w, width=1400, height=dimension_altura, bg=color_home)
            f2.place(x=0, y=45)

            global portada
            portada = ImageTk.PhotoImage(Image.open("iconos/portada/portada2.png"))
            Label(f2, image=portada, border=0, bg='white').place(x=0, y=0)

            query="SELECT SUM(price * cantidad) AS total_capital FROM product;"
            capital=ConecionSql().run_query(query,).fetchall()[0][0]
            query = "SELECT SUM((price - cantidad_sin_ganansia) * cantidad) AS total_ganancias FROM product;"
            ganancias = ConecionSql().run_query(query, ).fetchall()[0][0]

            query="SELECT SUM(deuda) FROM credito "
            capital_en_credito=ConecionSql().run_query(query,).fetchall()[0][0]

            lb_capital_en_deuda=Label(f2,text="Capital en deuda: "+str(capital_en_credito),fg="white", font=("Arial", 16,"bold"),bg=color_home).place(x=600,y=120)

            lb_capital=Label(f2,text="Capital: "+str(capital),fg="white", font=("Arial", 16,"bold"),bg=color_home).place(x=600,y=40)
            lb_ganancia = Label(f2, text="Gananancia: "+str(ganancias), fg="white", font=("Arial", 16, "bold"), bg=color_home).place(x=600,y=80)
            print("Actualisacion desde github exitosa")








        def home():

            color_home="#262626"
            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            """l2 = Label(f2, image=, fg=color_fuente, bg=color_fondo)
            l2.config(font=('Comic Sans MS', 90))
            l2.place(x=290, y=150 - 45)"""
            global portada
            portada = ImageTk.PhotoImage(Image.open("iconos/portada/portada2.png"))
            Label(f2, image=portada, border=0, bg='white').place(x=0, y=0)


            query="SELECT SUM(price * cantidad) AS total_capital FROM product;"
            capital=ConecionSql().run_query(query,).fetchall()[0][0]
            query = "SELECT SUM((price - cantidad_sin_ganansia) * cantidad) AS total_ganancias FROM product;"
            ganancias = ConecionSql().run_query(query, ).fetchall()[0][0]

            query="SELECT SUM(deuda) FROM credito "
            capital_en_credito=ConecionSql().run_query(query,).fetchall()[0][0]


            lb_capital=Label(f2,text="Capital: "+str(capital),fg="white", font=("Arial", 16,"bold"),bg=color_home).place(x=600,y=40)
            lb_ganancia = Label(f2, text="Gananancia: "+str(ganancias), fg="white", font=("Arial", 16, "bold"), bg=color_home).place(x=600,y=80)
            lb_capital_en_deuda = Label(f2, text="Capital en deuda: " + str(capital_en_credito), fg="white",font=("Arial", 16, "bold"), bg=color_home).place(x=600, y=120)










            toggle_win()

        def OctenerFecha():
                import calendar
                dateTimeObj = datetime.now()
                #timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                #fecha=timestampStr.split[0]()[0]
                año_mes =dateTimeObj.strftime("%Y-%m-%d").split()[0]
                hora = dateTimeObj.strftime("%H-%M-%S")
                hora=hora.split()[0]
                timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S")
                fecha=timestampStr.split()[0]
                mes_año =dateTimeObj.strftime("%d-%m-%Y").split()[0]
                return fecha,año_mes,hora,mes_año

        def RegistrarEvento(accion, odgeto):
            query = "INSERT INTO notificaciones(nombre_n,fecha) values(?,?)"
            noti = f"El usuario: ({nombre_usr}): {accion} ({odgeto})"
            parameters = (noti, OctenerFecha()[0])
            ConecionSql().run_query(query, parameters)

        def OctenerTotalDeHoy():
            query = "SELECT SUM(precio*cantidad) FROM registro_ventas WHERE fecha LIKE ?"
            parameters = (OctenerFecha()[1] + '%',)
            total_ventas_hoy = ConecionSql().run_query(query, parameters).fetchall()[0][0]

            total_hoy.set("Total de hoy.: " + str(total_ventas_hoy))

        def calcular_ganancia_hoy():
            try:
                fecha_hoy = OctenerFecha()[1]
                print("Fecha de hoy.:", fecha_hoy)

                # Query para obtener los productos vendidos en el día con sus cantidades
                query_ventas = 'SELECT nombre, cantidad FROM registro_ventas WHERE fecha LIKE ?'
                productos_vendidos = ConecionSql().run_query(query_ventas, parameters=(fecha_hoy + '%',)).fetchall()

                # Inicializar la ganancia total del día
                ganancia_total = 0

                # Calcular la ganancia total del día sumando la diferencia entre precio con ganancia y sin ganancia
                for producto in productos_vendidos:
                    nombre, cantidad = producto

                    # Consultar la tabla 'product' para obtener el precio con y sin ganancia del producto
                    query_producto = 'SELECT price, cantidad_sin_ganansia FROM product WHERE name = ?'
                    resultado_producto = ConecionSql().run_query(query_producto, parameters=(nombre,)).fetchone()

                    if resultado_producto:
                        precio_con_ganancia, precio_sin_ganancia = resultado_producto
                        ganancia_producto = (precio_con_ganancia - precio_sin_ganancia) * cantidad
                        ganancia_total += ganancia_producto


                return ganancia_hoy.set("G: " + str(ganancia_total))
            except Exception as e:
                print("Error:", str(e))
                return ganancia_hoy.set("Error")


        def MirandoQueProductoSeEstanPorCaducar():
            def obtener_fecha_actual():
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S")
                return timestampStr.split()[0]

            def obtener_fecha_vencimiento(fecha_str):
                try:
                    fecha_vencimiento_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
                    return fecha_vencimiento_obj
                except ValueError:
                    print("Error: La fecha de vencimiento no tiene el formato esperado.")
                    return None

            def mostrar_alerta_producto(producto_nombre):
                mensaje = f"El Producto {producto_nombre} está por vencer."
                mb.showinfo("Estado de producto", mensaje)

            query = "SELECT name, fecha_vencimiento, mesProximoDevovlucion FROM product"
            datoss = ConecionSql().run_query(query).fetchall()
            fecha_actual = obtener_fecha_actual()

            for datos in datoss:
                fecha_alerta = datos[2]
                fecha_vencimiento = str(datos[1])

                if fecha_alerta is None:
                    continue

                try:
                    int(fecha_alerta)
                    fecha_vencimiento_obj = obtener_fecha_vencimiento(fecha_vencimiento)
                    if fecha_vencimiento_obj is None:
                        continue

                    if fecha_vencimiento_obj >= datetime.now():
                        dias_hasta_vencimiento = (fecha_vencimiento_obj - datetime.now()).days

                        if dias_hasta_vencimiento <= int(fecha_alerta):
                            mostrar_alerta_producto(datos[0])

                except ValueError:
                    print("Error: La fecha de alerta no es un número válido.")









        def Facturar():
            try:
              MirandoQueProductoSeEstanPorCaducar()
            except:
                mb.showinfo('','')

            def TotalFactura():
                total = 0.0

                for item in factura.get_children():
                    celda = float(factura.set(item, "#1"))
                    celda_cantidad = float(factura.set(item, "#2"))
                    sumas_de_celda = celda * celda_cantidad
                    total += sumas_de_celda

                    query = "SELECT * FROM configuraciones  WHERE nombre_cf='dollar'"
                    total_en_dollar = ConecionSql().run_query(query, ).fetchall()[0]
                    total_en_dollar = total_en_dollar[2]
                    r = total / total_en_dollar
                    dollar = "{0:.2f}".format(r)

                return total ,dollar

            def buscar(event):
                octener_datos= "%" + caja_buscar.get() + "%"
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
                #query = 'SELECT * FROM product ORDER BY name DESC'
                query = 'SELECT * FROM product ORDER BY rowid DESC LIMIT 100;'
                db_rows=ConecionSql().run_query(query,)
                for fila in db_rows:
                    lista_producto.insert('', 0, text=fila[1], value= (fila[2], fila[3]))

            def OctenerClientes(event):

                def DandoCredito(event):
                    p = cb.get()
                    p = p.split()
                    nombre = p[0]
                    apellido = p[1]
                    query = "SELECT * FROM credito where nombre=? and apellido=?"
                    trallendo_deuda1 = ConecionSql().run_query(query, parameters=(nombre, apellido)).fetchall()[0]


                    listap = ""
                    for item in factura.get_children():
                        c = factura.item(item)["text"]
                        b = factura.item(item)["values"][0]
                        g = factura.item(item)["values"][1]
                        hr().RestandoProductoVendido(c, g)
                        octener_productos()

                        d = OctenerFecha()[0]
                        e = trallendo_deuda1[4]
                        parameters = (c, b, d, e, g)
                        listap += c + ", "
                    print(listap, "====")





                    query = "SELECT deuda FROM credito where nombre=? and apellido=?"
                    trallendo_deuda = ConecionSql().run_query(query, parameters=(nombre, apellido))

                    tr = trallendo_deuda.fetchall()[0][0]
                    print(tr)

                    sumando_deuda = tr + TotalFactura()[0]
                    print(apellido)
                    parameters = (sumando_deuda, nombre, apellido)
                    # self.run_query(query,)
                    query = "UPDATE credito SET deuda =? where nombre=? and apellido= ?"
                    ConecionSql().run_query(query, parameters)





                    listap = ""

                    for item in factura.get_children():
                        nombre = factura.item(item)["text"]
                        precio = factura.item(item)["values"][0]
                        cantidad = str(factura.item(item)["values"][1])

                        while len(nombre) < 60:
                            nombre += " "
                        while len(precio) < 5:
                            precio += " "
                        while len(cantidad) < 7:
                            cantidad += " "
                        sud_total = float(precio) * float(cantidad)

                        listap += nombre + str(precio) + "     " + str(cantidad) + "     " + str(sud_total) + "\n"

                    hr().registroCredito(listap, datos=(p[0] + " " + apellido, nombre_usr,TotalFactura()[0],nombre_negocio))






                    vte.destroy()
                    mb.showinfo("Exito", "Sele a dado el cridito a: " + "(" + nombre + ")")
                    octener_productos()
                    limpiar()

                def on_combobox_select(event):
                    p = cb.get()
                    p = p.split()
                    nombre = p[0]
                    apellido = p[1]
                    query = "SELECT deuda FROM credito where nombre=? and apellido=?"
                    trallendo_deuda= ConecionSql().run_query(query, parameters=(nombre, apellido)).fetchall()[0][0]
                    dd="Deuda: "+ str(trallendo_deuda)
                    print(dd)
                    lb_deuda = ttk.Label(vte, text=dd).place(x=280,y=89)


                vte= Toplevel()
                vte.geometry('260x150')
                vte.resizable(0, 0)
                vte.geometry("630x230")
                vte.title("Confirmar credito")
                vte.attributes("-topmost", True)
                lb_selecione_cliente=Label(vte,text='Selecione cliente a darlr el credito')
                lb_selecione_cliente.place(x=20,y=10)

                query="SELECT nombre, apellido FROM credito WHERE deuda < cantidad_masima_f"
                dato=ConecionSql().run_query(query).fetchall()


                lb_icon_cliente=Label(vte,image=iccliente).place(x=20,y=80)
                cb = ttk.Combobox(vte,values=dato)
                cb.place(x=90, y=89)
                cb.bind('<Return>',DandoCredito)
                cb.bind("<<ComboboxSelected>>", on_combobox_select)
                cb.config(state='readonly')

                lb_total = Label(vte, text="Total Cordobas: "+str(TotalFactura()[0])).place(x=20,y=40)
                lb_total_dolar = Label(vte, text="Dollar : " + str(TotalFactura()[1])).place(x=180, y=40)
                bt_confirmar_credito_credito=ttk.Button(vte,text="Confirmar Credito",command=lambda :DandoCredito(""))
                bt_confirmar_credito_credito.place(x=500,y=200)




            def agregar(event):

                cur_id0 = lista_producto.focus()
                c_s = int(float(lista_producto.item(cur_id0)['values'][1]))
                if c_s <= 0:
                    mb.showwarning("Error", "Este producto se a agotado")
                    return

                vt_inPA = Toplevel()
                vt_inPA.resizable(False,False)
                vt_inPA.attributes("-topmost", True)
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

            def total(event):

                def convirtiendo_dollar(total):
                    query = "SELECT * FROM configuraciones  WHERE nombre_cf='dollar'"
                    total_en_dollar = ConecionSql().run_query(query, ).fetchall()[0]
                    total_en_dollar = total_en_dollar[2]
                    r = total / total_en_dollar
                    r = "{0:.2f}".format(r)
                    print(r)
                    return r



                def Confirmar_venta(event,total, cf_vt, lb_mb_e, caja_cambio, CheckVar1,t,caja_cambio_dollar):

                        query = "SELECT * FROM configuraciones  WHERE nombre_cf='dollar'"
                        total_en_dollar = ConecionSql().run_query(query, ).fetchall()[0]
                        total_en_dollar = total_en_dollar[2]

                        moneda_cordoba= caja_cambio.get()
                        moneda_dollar = caja_cambio_dollar.get()
                        if caja_cambio.get() == "" and caja_cambio_dollar.get() == "":
                            lb_mb_e['text'] = "{}".format("Se nesesita que ingrese el cambio")
                            return

                        if caja_cambio.get() == "":
                            moneda_cordoba =0
                        elif caja_cambio_dollar.get()  == "":
                            moneda_dollar =0


                        sumando_monedas= float(moneda_cordoba) + (float(moneda_dollar)*float(total_en_dollar))
                        pago="{0:.2f}".format(sumando_monedas)

                        print("valor del check ", CheckVar1.get())
                        clave_producto = OctenerFecha()[1] + nombre_usr + OctenerFecha()[2]
                        lista = ""



                        """if caja_cambio.get() == "" and caja_cambio_dollar.get() =="":
                            lb_mb_e['text'] = "{}".format("Se nesesita que ingrese el cambio")
                            return"""
                        try:



                            p_total = 0.0

                            if t > 0:
                                total = t
                            else: p_total = total
                            cambio = float(sumando_monedas) - float(p_total)
                            cambio = "{0:.2f}".format(cambio)
                            if CheckVar1.get() != 1:
                                if float(sumando_monedas < float(p_total) or sumando_monedas < t):
                                    lb_mb_e['text'] = "{}".format("Error el pago es menor al total de los productos")
                                    return
                        except Exception as e:
                            error_mensage=f"Se produjo un error:{e}"
                            lb_mb_e['text'] = "{}".format(error_mensage)
                            print(error_mensage)
                            caja_cambio.delete(0, END)
                            return


                        cf_vt.destroy()
                        if CheckVar1 == 1:
                            mb.showinfo("Exito", "El buelto del cambio del dollar es: " + str(cambio))
                        mb.showinfo("Exito", "El vuelto es: " + str(sumando_monedas-total))


                        print('esta es la contra: ' + clave_producto)

                        usr = nombre_usr
                        f=OctenerFecha()[0]
                        code=funcion.GeneraContraseña()
                        listap=""
                        for item in factura.get_children():
                            nombre = factura.item(item)["text"]
                            precio = factura.item(item)["values"][0]
                            cantidad = str(factura.item(item)["values"][1])
                            #parameters= (nombre,precio,f,usr,cantidad,code,)

                            hr().registro_ventas(nombre,precio,f,usr,cantidad,code,)

                            while len(nombre) < 60:
                                nombre+=" "
                            while len(precio) < 5:
                                precio+=" "
                            while len(cantidad) < 7:
                                cantidad+=" "
                            sud_total=float(precio)*float(cantidad)

                            listap += nombre+str(precio)+"     "+str(cantidad)+"     "+str(sud_total)+"\n"

                        #Restamos los productos en la base de datos
                        for item in factura.get_children():
                            c = factura.item(item)["text"]
                            d = factura.item(item)["values"][0]
                            g = factura.item(item)["values"][1]

                            hr().RestandoProductoVendido(c, g)



                        cambio= float(pago) - float(total)
                        cambio="{0:.2f}".format(cambio)
                        parametros= (listap,str(total),pago,str(cambio),cantidad)

                        hr().RegistroText(parametros,ur=usr)
                        OctenerTotalDeHoy()
                        calcular_ganancia_hoy()
                        octener_productos()
                        limpiar()
                        caja_buscar.delete(0, END)




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
                    cf_vt.attributes("-topmost", True)
                    cf_vt.geometry("680x230")


                    lb_total = ttk.Label(cf_vt, text="Total")
                    lb_total.grid(row=0, column=0, padx=10, pady=2)
                    lb_descuento = Label(cf_vt, text="Descuento",fg="red")
                    lb_descuento.grid(row=1, column=0, padx=10, pady=2)
                    lb_cambio = ttk.Label(cf_vt, text="Cabio de dinero")
                    lb_cambio.grid(row=2, column=0, pady=5)
                    lb_mb_e = Label(cf_vt, text="                                                     ", fg="red")
                    lb_mb_e.grid(row=5, column=1)
                    CheckVar1 = IntVar()

                    """C1 = Checkbutton(cf_vt, text="Dollares", variable=CheckVar1, \
                                     onvalue=1, offvalue=0, height=5, \
                                     width=20)
                    C1.grid(row=2, column=2)"""


                    lb_cordobas=Label(cf_vt,text="Cordobas").grid(row=2,column=1)
                    caja_cambio = ttk.Entry(cf_vt)
                    caja_cambio.grid(row=2, column=2)
                    lb_cordobas = Label(cf_vt, text="Dollar").grid(row=3, column=1)
                    caja_cambio_dollar = ttk.Entry(cf_vt)
                    caja_cambio_dollar.grid(row=3,column=2)

                    bt_canselar = ttk.Button(cf_vt, text="Canselar",
                                             command=lambda: (cf_vt.destroy(), limpiar(), caja_buscar.delete(0, END)))
                    bt_canselar.grid(row=4, column=0, padx=10, pady=15)
                    bt_confirmar = ttk.Button(cf_vt, text="Confirmar",
                                              command=lambda: Confirmar_venta("",total, cf_vt, lb_mb_e, caja_cambio, CheckVar1,t,caja_cambio_dollar))
                    bt_confirmar.grid(row=4, column=1, padx=10, pady=5)
                    caja_cambio.bind("<Return>", lambda event: Confirmar_venta("",total, cf_vt, lb_mb_e, caja_cambio, CheckVar1,t,caja_cambio_dollar))
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
            #cambiar en mi lapto
            lista_producto = ttk.Treeview(f2, height=21, columns=("#0", "#1"))
            lista_producto.heading('#0', text='Nombre', anchor=CENTER)
            lista_producto.heading('#1', text='Presio', anchor=CENTER)
            lista_producto.heading('#2', text='cantidad', anchor=CENTER)
            lista_producto.column("#0", width=540)
            lista_producto.column("#1", width=80)
            lista_producto.column("#2", width=80)
            lista_producto.place(x=0,y=10)
            lista_producto.bind('<Double-Button-1>', agregar)
            lista_producto.bind('<Return>', agregar)
            lista_producto.tag_configure("tagName", font=("TkDefaultFont", 20))



            caja_buscar = ttk.Entry(f2, width=37)
            caja_buscar.place(x=0,y=660)
            caja_buscar.bind("<KeyRelease>", buscar)
            caja_buscar.focus()
            caja_buscar.config(font=("Arial", 20, "bold"))



            # TABLA FACTURA
            factura = ttk.Treeview(f2, height=21, column=("#0", 2, 3))
            factura.heading('#0', text='Nombre', anchor=CENTER)
            factura.column('#0', width=450)
            factura.heading('#1', text='Presio', anchor=CENTER)
            factura.column('#1', width=80)
            factura.heading('#2', text='Cantidad', anchor=CENTER)
            factura.column("#2", width=80)
            factura.heading('#3', text='Sub total', anchor=CENTER)
            factura.column("#3", width=80)
            factura.place(x=705,y=10)
            octener_productos()

            bt_vender = Button(f2, text="Vender",width=37,command=lambda :total(""))
            bt_vender.place(x=706,y=668)

            bt_credito = Button(f2, text="Dar en credito",width=33,command=lambda:OctenerClientes(""))
            bt_credito.place(x=1070,y=668)

            lista_producto.bind("<Left>",total)
            factura.bind("<Left>",total)

            lista_producto.bind("<Right>",OctenerClientes)
            factura.bind("<Right>",OctenerClientes)


            # Establecer el valor de "takefocus" en 1 para ambos Treeview

            lista_producto.config(takefocus=1)
            factura.config(takefocus=1)





            factura.bind('<Tab>',total)



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
                octener_datos= "%" + caja_buscar_todos_productos.get() + "%"
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
                #query = 'SELECT * FROM product ORDER BY name DESC'
                query = 'SELECT * FROM product ORDER BY rowid DESC LIMIT 100;'
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
                RegistrarEvento('Borro el producto',name)



            def ActualizarProducto():

                try:
                    lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text'][0]
                except IndexError as e:
                    mb.showwarning("Error","Porfavor Selecione Un Producto")
                    return
                name=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text']
                datos=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['values']


                LimpiarCajasAdministrarProduct()
                caja_i_nombre.insert(0,name)
                caja_i_presio.insert(0,datos[1])
                caja_i_cantidad.insert(0,datos[2])
                caja_i_ganancia.insert(0,float(datos[0])- float(datos[1]))
                caja_i_fecha_vencimiento.insert(0, datos[3])
                caja_i_fecha_alerta_antes_devencer.insert(0, datos[4])
                caja_i_descuento.insert(0,datos[5])
                caja_i_cantidad_dar_descuento.insert(0,datos[6])



                bt_i_insertar_nuevo_producto.configure(text="Actualizar")



            def ActualizandoProducto():

                if caja_i_nombre.get() == "" or caja_i_presio.get() == "" or caja_i_cantidad.get() =="" or caja_i_ganancia.get() =="" or caja_i_descuento.get() =="" or caja_i_cantidad_dar_descuento.get() =="" or caja_i_fecha_vencimiento.get() == "" or caja_i_fecha_alerta_antes_devencer.get() =="":
                    mb.showerror("Error","Todos los datos son nesesarios")
                    return
                if len(caja_i_fecha_vencimiento.get()) != 10 :
                        mb.showwarning("Error","La caja de la fecha nesesita que se inserten 10 digitos use / para separar ejemplo: 01/06/2023   primero el dia despues el mes y despues el año")
                        return

                ganancia=float(caja_i_ganancia.get()) + float(caja_i_presio.get())

                name=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['text']
                parameters=(caja_i_nombre.get(),ganancia,caja_i_cantidad.get(),caja_i_presio.get(),caja_i_fecha_vencimiento.get(),caja_i_fecha_alerta_antes_devencer.get(),caja_i_descuento.get(),caja_i_cantidad_dar_descuento.get(),name)
                query= 'UPDATE product SET name = ?, price=?, cantidad=?,cantidad_sin_ganansia=?,fecha_vencimiento=?,mesProximoDevovlucion=?,descuento=?,cantidad_xmayor=? WHERE name = ?'
                ConecionSql().run_query(query,parameters)
                bt_i_insertar_nuevo_producto.configure(text="Insertar")

                query="INSERT INTO notificaciones(nombre_n,fecha) values(?,?)"
                presio_viejo=lista_todos_los_datos_productos.item(lista_todos_los_datos_productos.selection())['values'][1]
                noti= "El usuario: "+nombre_usr+" Actualizo el producto: "+name+" Nuevo precio: "+caja_i_presio.get()+" precio anterior: "+presio_viejo
                parameters=(noti,OctenerFecha()[0])
                ConecionSql().run_query(query,parameters)


                mb.showinfo("Exito", "EL producto se a actualizado")

                octener_todos_los_productos()
                LimpiarCajasAdministrarProduct()


            def CambiarEstadoBotonProduct():
                if bt_i_insertar_nuevo_producto.cget("text") == "Actualizar":
                    ActualizandoProducto()

                elif bt_i_insertar_nuevo_producto.cget("text") == "Insertar":
                    print("Entramos")
                    InsertarNuevoProducto()

            def LimpiarCajasAdministrarProduct():
                caja_i_nombre.delete(0,END)
                caja_i_presio.delete(0,END)
                caja_i_cantidad.delete(0,END)
                caja_i_ganancia.delete(0,END)
                caja_i_fecha_vencimiento.delete(0,END)
                caja_i_fecha_alerta_antes_devencer.delete(0,END)
                caja_i_descuento.delete(0,END)
                caja_i_cantidad_dar_descuento.delete(0,END)



            def InsertarNuevoProducto():

                if caja_i_nombre.get() == "" or caja_i_presio.get() == "" or caja_i_cantidad.get() =="" or caja_i_ganancia.get() =="" or caja_i_descuento.get() =="" or caja_i_cantidad_dar_descuento.get() =="" or caja_i_fecha_vencimiento.get() == "" or caja_i_fecha_alerta_antes_devencer.get() =="":
                    mb.showerror("Error","Todos los datos son nesesarios")
                    return

                if len(caja_i_fecha_vencimiento.get()) != 10:
                    mb.showwarning("Error","La caja de la fecha nesesita que se inserten 10 digitos use / para separar ejemplo: 01/06/2023   primero el dia despues el mes y despues el año")
                    return

                ganancia=float(caja_i_ganancia.get()) + float(caja_i_presio.get())
                parameters = (caja_i_nombre.get(), ganancia, caja_i_cantidad.get(), caja_i_fecha_vencimiento.get(),caja_i_presio.get(),
                               caja_i_fecha_alerta_antes_devencer.get(), caja_i_descuento.get(),
                              caja_i_cantidad_dar_descuento.get())
                query="insert into product values(NULL, ?, ?, ?, ?, ?, ?,?,?)"
                ConecionSql().run_query(query,parameters)

                mb.showinfo("Exito","El producto se a guardado en la base de dato")
                LimpiarCajasAdministrarProduct()
                octener_todos_los_productos()

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

            def LimpiarTabla():
                recoriendo = lista_todos_los_datos_productos.get_children()
                for r in recoriendo:
                  # Elimina cada elemento de la tabla
                  lista_todos_los_datos_productos.delete(r)

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

                        try:
                            print(farl[2])
                            print(fvrl[2])
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

            def obtener_productos_vencidos():
                LimpiarTabla()
                # Obtener la fecha actual
                fecha_actual = datetime.now()

                # Consulta a la base de datos para obtener la información de los productos
                query = "SELECT name, fecha_vencimiento, mesProximoDevovlucion FROM product"
                datos = ConecionSql().run_query(query).fetchall()

                # Lista para almacenar los productos vencidos
                productos_vencidos = []

                # Iterar sobre los datos de la base de datos
                for producto in datos:
                    nombre_producto, fecha_vencimiento, fecha_alerta = producto

                    # Verificar si las fechas no están vacías y no son None
                    if fecha_vencimiento and fecha_alerta and fecha_alerta != 'None':
                        # Convertir las fechas de texto a objetos datetime
                        try:
                            fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
                            # Verificar si fecha_alerta es una cadena antes de intentar convertirla
                            if isinstance(fecha_alerta, str):
                                fecha_alerta = datetime.strptime(fecha_alerta, "%d/%m/%Y")
                            else:
                                raise ValueError("Fecha de alerta no es una cadena")
                        except ValueError as e:
                            # Manejar la excepción (puedes imprimir un mensaje o hacer algo más)
                            print(f"Error al convertir fechas para el producto {nombre_producto}: {e}")
                            continue  # Continuar con el siguiente producto

                        # Verificar si el producto está vencido
                        if fecha_actual > fecha_vencimiento:
                            productos_vencidos.append(nombre_producto)
                            lista_todos_los_datos_productos.insert("", END, text=nombre_producto, values=('', '','', fecha_vencimiento,))


            def ProductosApuntoDeVencer():
                LimpiarTabla()  # Limpiar la tabla antes de agregar nuevos productos

                # Obtener la fecha actual
                fecha_actual = datetime.now()

                # Consulta a la base de datos para obtener la información de los productos
                query = "SELECT name, fecha_vencimiento, mesProximoDevovlucion FROM product"
                datos = ConecionSql().run_query(query).fetchall()

                # Lista para almacenar los productos a punto de vencer
                productos_apunto_de_vencer = []

                # Iterar sobre los datos de la base de datos
                for producto in datos:
                    nombre_producto, fecha_vencimiento, meses_proximo_vencimiento = producto

                    # Verificar si las fechas no están vacías y no son None
                    if fecha_vencimiento and meses_proximo_vencimiento and meses_proximo_vencimiento != 'None':
                        # Convertir las fechas de texto a objetos datetime
                        try:
                            fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
                            meses_proximo_vencimiento = int(meses_proximo_vencimiento)
                        except ValueError as e:
                            # Manejar la excepción (puedes imprimir un mensaje o hacer algo más)
                            print(f"Error al convertir fechas para el producto {nombre_producto}: {e}")
                            continue  # Continuar con el siguiente producto

                        # Calcular la fecha de alerta basada en meses_proximo_vencimiento
                        fecha_alerta = fecha_vencimiento - timedelta(days=30 * meses_proximo_vencimiento)

                        # Verificar si el producto está a punto de vencer
                        if fecha_actual > fecha_alerta and fecha_actual <= fecha_vencimiento:
                            productos_apunto_de_vencer.append(nombre_producto)
                            lista_todos_los_datos_productos.insert("", END, text=nombre_producto, values=('', '', '', fecha_vencimiento,))














            def RadioButoonAdministrarProducto():
                if valor.get() == 3:
                    ProductosApuntoDeVencer()
                elif valor.get() == 2:
                    obtener_productos_vencidos()
                elif valor.get() == 4:
                    octener_todos_los_productos()
                else: octener_todos_los_productos()






            f1.destroy()
            f2 = Frame(w, width=dimension_ancho, height=dimension_altura, bg=color_fondo)
            f2.place(x=0, y=45)
            labelframe1=LabelFrame(f2,bg="black")
            labelframe1.place(x=30, y=0)



            #-----------------------------------------------------------------------

            label_nombre = ttk.Label(labelframe1, text="Nombre:")
            label_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="W")
            caja_i_nombre = ttk.Entry(labelframe1)
            caja_i_nombre.grid(row=0, column=1, padx=10, pady=10)

            label_precio = ttk.Label(labelframe1, text="Precio:")
            label_precio.grid(row=0, column=2, padx=10, pady=10, sticky="W")
            caja_i_presio = ttk.Entry(labelframe1)
            caja_i_presio.grid(row=0, column=3, padx=10, pady=10)

            label_cantidad = ttk.Label(labelframe1, text="Cantidad:")
            label_cantidad.grid(row=0, column=4, padx=10, pady=10, sticky="W")
            caja_i_cantidad = ttk.Entry(labelframe1)
            caja_i_cantidad.grid(row=0, column=5, padx=10, pady=10)

            label_ganancia = ttk.Label(labelframe1, text="Ganancia: ")
            label_ganancia.grid(row=1, column=0, padx=10, pady=10, sticky="W")
            caja_i_ganancia = ttk.Entry(labelframe1)
            caja_i_ganancia.grid(row=1, column=1, padx=10, pady=10)

            label_fecha_vencimiento = ttk.Label(labelframe1, text="Fecha de vencimiento:")
            label_fecha_vencimiento.grid(row=1, column=2, padx=10, pady=10, sticky="W")
            caja_i_fecha_vencimiento = ttk.Entry(labelframe1)
            caja_i_fecha_vencimiento.grid(row=1, column=3, padx=10, pady=10)

            label_fecha_alerta_antes_devencer = ttk.Label(labelframe1, text="Meses de alerta antes de vencer:")
            label_fecha_alerta_antes_devencer.grid(row=1, column=4, padx=10, pady=10, sticky="W")
            caja_i_fecha_alerta_antes_devencer = ttk.Entry(labelframe1)
            caja_i_fecha_alerta_antes_devencer.grid(row=1, column=5, padx=10, pady=10)

            label_descuento = ttk.Label(labelframe1, text="Descuento (%):")
            label_descuento.grid(row=2, column=0, padx=10, pady=10, sticky="W")
            caja_i_descuento = ttk.Entry(labelframe1)
            caja_i_descuento.grid(row=2, column=1, padx=10, pady=10)

            label_cantidad_dar_descuento=ttk.Label(labelframe1, text="Cantidad dar descuento")
            label_cantidad_dar_descuento.grid(row=2, column=2, padx=10, pady=10, sticky="W")
            caja_i_cantidad_dar_descuento = ttk.Entry(labelframe1)
            caja_i_cantidad_dar_descuento.grid(row=2, column=3, padx=10, pady=10)


            bt_i_insertar_nuevo_producto = Button(labelframe1,text="Insertar",bg="black",fg='green',width=17,command=CambiarEstadoBotonProduct)
            if permiso_usr == 'root':
                bt_i_insertar_nuevo_producto.grid(row=2,column=4,pady=10)

            lista_todos_los_datos_productos=ttk.Treeview(f2, height=dimension_treeview_altura_administrar_producto, columns=("#0", "#1",'#2','#3','#4','#5','#6'))
            lista_todos_los_datos_productos.place(x=30,y=146)
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
            caja_buscar_todos_productos.place(x=30,y=eje_y_widget_producto)
            caja_buscar_todos_productos.bind("<KeyRelease>", BuscarTodosLosProductos)
            caja_buscar_todos_productos.focus()
            caja_buscar_todos_productos.config(font=("Arial", 20, "bold"))

            valor = IntVar()
            rd_p_agotados= ttk.Radiobutton(f2,text="Productos agotados",variable=valor, value=1,command=RadioButoonAdministrarProducto)
            rd_p_agotados.place(x=565,y=eje_y_widget_producto)
            rd_p_apunto_de_vencer = ttk.Radiobutton(f2, text="Productos vencidos",variable=valor, value=2,command=RadioButoonAdministrarProducto)
            rd_p_apunto_de_vencer.place(x=728, y=eje_y_widget_producto)
            rd_p_apunto_de_vencer = ttk.Radiobutton(f2, text="Productos apunto de vencer", variable=valor, value=3,command=RadioButoonAdministrarProducto)
            rd_p_apunto_de_vencer.place(x=890, y=eje_y_widget_producto)

            rd_p_apunto_de_vencer = ttk.Radiobutton(f2, text="Todos los productos", variable=valor, value=4,command=RadioButoonAdministrarProducto)
            rd_p_apunto_de_vencer.place(x=1120, y=eje_y_widget_producto)

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
                query = "SELECT * FROM credito"
                dato = ConecionSql().run_query(query)
                recorer = tabla_clientes.get_children()
                # LIMPIAMOS TABLA CLIENTE
                for r in recorer:
                    tabla_clientes.delete(r)

                for row in dato:
                    tabla_clientes.insert('', 0, text=row[1], values=(row[2], row[4]))



            def BorrarCliente():
                c = tabla_clientes.selection()
                dato = tabla_clientes.item(c)['text']
                print(dato, 'jjj')
                query = "DELETE from credito where nombre= ?"
                parameters = (dato,)
                resultado = mb.askokcancel('Advertencia', 'Seguro que quieres borrar un cliente')
                if resultado:
                    ConecionSql().run_query(query, parameters)
                    OctenerClientes()
                else:
                    print("Se a canselado la eliminacion")

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

                    #hr().registroCredito(nombre_negocio,trallendo_datos,parametros=(nombre, apellido, usr, dud, pg, resta, trallendo_nombre))
                    hr().RegistroPagoDeDeuda(nombre+" "+apellido,str(pg),nombre_usr)

                item = tabla_clientes.selection()
                try:
                    tabla_clientes.item(item)["values"][1]
                except IndexError as e:
                    mb.showinfo("Error🚫", "Selecione a un deudor")
                    return
                deudor = tabla_clientes.item(item)["values"][1]
                nombre = tabla_clientes.item(item)["text"]
                apellido = tabla_clientes.item(item)["values"][0]

                vte_pagar_deuda = Toplevel()
                print(apellido)
                vte_pagar_deuda.title("Pagar deuda")
                vte_pagar_deuda.attributes("-topmost", True)

                # DEUDA
                Label(vte_pagar_deuda, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
                Entry(vte_pagar_deuda, textvariable=StringVar(vte_pagar_deuda, value=nombre), state="readonly").grid(
                    row=0, column=1, padx=10)

                Label(vte_pagar_deuda, text="Deuda").grid(row=1, column=0, padx=10, pady=5)
                Entry(vte_pagar_deuda, textvariable=StringVar(vte_pagar_deuda, value=deudor), state="readonly").grid(
                    row=1, column=1, padx=10)

                # PAGO
                Label(vte_pagar_deuda, text="Pagar$").grid(row=2, column=0, padx=10, pady=5)
                ppago = ttk.Entry(vte_pagar_deuda)
                ppago.grid(row=2, column=1, padx=10)
                ttk.Button(vte_pagar_deuda, text="Aceptar", command=Pago).grid(row=3, column=1, sticky=W, padx=5)
                vte_pagar_deuda.mainloop()
                print("fin")

            def VaciarCajasClientes():
                caja_nombre_cliente.delete(0,END)
                caja_apellido_cliente.delete(0,END)
                caja_sexo_cliente.delete(0,END)
                caja_cantidad_max_f_cliente.delete(0,END)

            def InsertarNevouCliente():
                if caja_nombre_cliente.get() == "" or caja_apellido_cliente.get() == "" or caja_sexo_cliente.get() == "" or caja_cantidad_max_f_cliente.get() == "":
                    mb.showwarning("Error", "Todos los datos son nesesarios")
                    return
                if caja_nombre_cliente.get() == "Nombre" or caja_apellido_cliente.get() == "Apellido" or caja_cantidad_max_f_cliente.get() == "Cantidad Max Credito":
                    mb.showwarning("Error", "Todos los datos son nesesarios")
                    return
                if caja_sexo_cliente.get() == "Hombre" or caja_sexo_cliente.get() == "Mujer" or caja_sexo_cliente.get() == "Otros":
                    pass
                else:
                    return mb.showwarning("Error", "Selecione una de las tres opiones dela caja sexo")

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
                query = "INSERT INTO credito VALUES(NULL,?,?,?,?,?,?) "
                parameters = (
                caja_nombre_cliente.get(), caja_apellido_cliente.get(), caja_sexo_cliente.get(), 0, codigo,
                caja_cantidad_max_f_cliente.get())
                ConecionSql().run_query(query, parameters)
                mb.showinfo("Exito", "El cliente se inserto en la base de datos")
                OctenerClientes()
                VaciarCajasClientes()







            def DetallesDeCredito():
                def InDatosScrollText():

                    nombre_archivo= nombre_cliente+".txt"
                    try:
                        with open("registro/credito/"+nombre_archivo,"r",encoding='UTF-8') as ruta:
                            ruta=ruta.read()
                            scrolledtext1.delete("1.0", "20000.0")
                            scrolledtext1.insert("1.0",ruta)
                    except :scrolledtext1.insert("1.0","No tiene registro de credito todavia")



                consiguiendo_nombre = tabla_clientes.selection()
                nombre_cliente =tabla_clientes.item(consiguiendo_nombre)['text']
                apellido_cliente=tabla_clientes.item(consiguiendo_nombre)["values"][0]
                nombre_cliente=nombre_cliente +" "+apellido_cliente
                vte_detalles_ventas=Toplevel()
                vte_detalles_ventas.attributes("-topmost", True)
                vte_detalles_ventas.resizable(False, False)
                vte_detalles_ventas.title("Detalles de credito de: "+nombre_cliente)
                scrolledtext1=st.ScrolledText(vte_detalles_ventas, width=94, height=23)
                scrolledtext1.grid(row=0,column=0,columnspan=10)


                InDatosScrollText()
                vte_detalles_ventas.mainloop()


            def Menuppo():
                # Menu ppo
                """def ConsultarEstado():
                    consiguiendo_nombre = tabla_clientes.selection()
                    nombre_cliente = tabla_clientes.item(consiguiendo_nombre)['text']
                    apellido_cliente = tabla_clientes.item(consiguiendo_nombre)["values"][1]
                    query = "SELECT estado FROM credito WHERE nombre=? AND apellido=?"
                    ddd = ConecionSql().run_query(query, parameters=(nombre_cliente, apellido_cliente)).fetchall()
                    return ddd"""



                popup = Menu(f2, tearoff=0)
                var = BooleanVar()


                # Adding Menu Items
                popup.add_command(label="Actualizar", command='')
                popup.add_command(label="Borrar", command=BorrarCliente)
                popup.add_command(label="Mostrar detalles del credito",command=DetallesDeCredito)
                popup.add_command(label="Saldar deuda", command=SaldarDeuda)
                #popup.add_separator()
                #popup.add_checkbutton(label="Estado del cliente", variable=ConsultarEstado())
                #popup.config(bg='blue')

                def on_check(var_name, element_name, op):



                    query = "UPDATE credito SET estado = ? WHERE nombre = ? AND apellido = ?;"

                    ConecionSql().run_query(query, parameters=(var.get(),nombre_cliente,apellido_cliente))
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

            labelframe1 = LabelFrame(f2, bg="white",text="Insertar nuevo cliente")
            labelframe1.place(x=800, y=20)

            lb_nombre_cliente=ttk.Label(labelframe1,text="Nombre")
            lb_nombre_cliente.grid(row=0,column=0, padx=10, pady=5)
            caja_nombre_cliente = ttk.Entry(labelframe1)
            caja_nombre_cliente.grid(row=0, column=1)

            lb_apellido_cliente = ttk.Label(labelframe1, text="Apellido")
            lb_apellido_cliente.grid(row=1, column=0, padx=10, pady=5)
            caja_apellido_cliente = ttk.Entry(labelframe1)
            caja_apellido_cliente.grid(row=1, column=1)

            lb_sexo_cliente = ttk.Label(labelframe1, text="Sexo")
            lb_sexo_cliente.grid(row=2, column=0, padx=10, pady=5)
            valor = ['Hombre', 'Mujer', 'Otros']
            caja_sexo_cliente = ttk.Combobox(labelframe1, values=valor)
            caja_sexo_cliente.grid(row=2, column=1)
            caja_sexo_cliente.config(state='readonly')

            lb_cantidad_maxima = ttk.Label(labelframe1, text="Cantidad Mx de crdt")
            lb_cantidad_maxima.grid(row=3, column=0, padx=10, pady=5)
            caja_cantidad_max_f_cliente = ttk.Entry(labelframe1)
            caja_cantidad_max_f_cliente.grid(row=3, column=1)


            bt_i_cliente = Button(labelframe1, text="Guardar cliente", command=InsertarNevouCliente).grid(row=4,
                                                                                                          column=1,
                                                                                                          padx=10,
                                                                                                          pady=5)

            tabla_clientes = ttk.Treeview(f2, height=dimencion_altura_tabla_detalles_credito_clientes,
                                          columns=('#1', '#2'))
            tabla_clientes.place(x=30, y=20)
            tabla_clientes.heading('#0', text="nombre", anchor=CENTER)
            tabla_clientes.column('#0', width=300)
            tabla_clientes.heading('#1', text="Apellido", anchor=CENTER)
            tabla_clientes.column('#1', width=250)
            tabla_clientes.heading('#2', text="Deuda", anchor=CENTER)
            tabla_clientes.column('#2', width=200)


            OctenerClientes()






            Menuppo()

        def Registro():

            def BusquedaRegistroUsuarioAvanzada():
                # Obtener los valores de la fecha
                year = year_entry2.get()
                month = month_entry2.get()
                day = day_entry2.get()

                # Construir la fecha en el formato adecuado para la consulta
                if day:
                    fecha = f"{year}-{month}-{day}%"
                else:
                    fecha = f"{year}-{month}-%"

                # Consulta SQL para buscar registros de ventas
                query = "SELECT * FROM registro_ventas WHERE fecha LIKE ? AND usuario LIKE ?"
                parameters = (fecha, cb_usearios.get())

                # Realizar la consulta y obtener los resultados
                try:

                    datos = ConecionSql().run_query(query, parameters).fetchall()
                except ConecionSql.Error as e:
                    mb.showerror("Error de Base de Datos", f"Error al ejecutar la consulta: {e}")
                    return


                # Limpiar el Treeview
                for item in treeview.get_children():
                    treeview.delete(item)

                # Mostrar los resultados en el Treeview
                if not datos:
                    mb.showinfo("Sin Resultados", "No se encontraron registros.")
                else:
                    for producto in datos:
                        treeview.insert("", "end", text=producto[1],
                                        values=(producto[2], producto[3], producto[4], producto[5], producto[7],producto[6]))

                # Consulta SQL para obtener el total de ventas


                try:

                    query = "SELECT SUM((precio * cantidad)  * (descuento / 100)) AS total FROM registro_ventas WHERE fecha LIKE ? AND usuario LIKE ?;"
                    descuento_result = ConecionSql().run_query(query, parameters).fetchone()
                    descuento = descuento_result[0] if descuento_result is not None else 0
                    print('------/',str(descuento))
                    total_query = "SELECT SUM(precio * cantidad) FROM registro_ventas WHERE fecha LIKE ? AND usuario LIKE ?;"
                    total_final = ConecionSql().run_query(total_query, parameters).fetchone()
                    total = total_final[0] if total_final is not None else 0

                    total_result = total - descuento



                except ConecionSql.Error as e:
                    mb.showerror("Error de Base de Datos", f"Error al obtener el total: {e}")
                    return


                #if total_result[0] is not None:
                total_text = "Total: " + str(total_result)

                label_text.set(total_text)

            def BusquedaUsuarios(event):
                datt =cb_usearios.get()+"%"
                datos = ConecionSql().run_query(query="SELECT * FROM registro_ventas WHERE usuario LIKE ?",parameters=(datt,)).fetchall()
                recorer = treeview.get_children()
                for r in recorer:
                    treeview.delete(r)

                for producto in datos:
                    treeview.insert("", "end", text=producto[1], values=(producto[2], producto[3], producto[4], producto[5], producto[7],producto[6]))

                query = "SELECT SUM(precio*cantidad) FROM registro_ventas WHERE usuario LIKE ?"
                parameters = (cb_usearios.get()+"%",)
                datos2 = ConecionSql().run_query(query, parameters).fetchone()
                dato3 = "Total Usuario: "+ str(datos2[0])
                print(datos2)
                label_text.set(dato3)

            def BuscarRegistro():
                recorer = treeview.get_children()


                fecha = year_entry.get() + "-" + month_entry.get() + "-" + day_entry.get() + "-" + hour_entry.get() + "%"
                if day_entry.get() == "":
                    fecha = year_entry.get() + "-" + month_entry.get() + "-" + '%'

                query = "SELECT * FROM registro_ventas  WHERE fecha LIKE ?"
                parameters = (fecha,)
                datos = ConecionSql().run_query(query, parameters).fetchall()
                print(datos)

                for r in recorer:
                    treeview.delete(r)
                for producto in datos:
                    treeview.insert("", "end", text=producto[1], values=(producto[2], producto[3], producto[4], producto[5], producto[7],producto[6]))

                query = "SELECT SUM(precio*cantidad) FROM registro_ventas WHERE fecha LIKE ?"
                parameters = (fecha,)
                datos2 = ConecionSql().run_query(query, parameters).fetchall()

                datos2 = datos2[0]

                datos2 = str(datos2[0])
                print(datos2)
                pp="Total: "+datos2
                label_text.set(pp)



            def DetallesVentas():
                def InDatosScrollText():

                    fecha= day_entry.get()+'-'+month_entry.get()+'-'+year_entry.get()
                    print(fecha+"jksqjkasjk")
                    if fecha == "--":
                        print("Erorrrrr")
                        fecha = OctenerFecha()[3]


                    nombre_archivo= fecha+".txt"
                    try:
                        with open("registro/facturas/"+nombre_archivo,"r",encoding='UTF-8') as ruta:
                            ruta=ruta.read()
                            scrolledtext1.delete("1.0", "20000.0")
                            scrolledtext1.insert("1.0",ruta)
                            text_var.set("")

                    except:
                        text_var.set("Error no se encontro ningun registro con esa fecha")

                text_var = StringVar()
                text_var.set("")

                vte_detalles_ventas=Toplevel()
                vte_detalles_ventas.attributes("-topmost", True)
                vte_detalles_ventas.resizable(False, False)
                vte_detalles_ventas.title("Registro Factura")
                scrolledtext1=st.ScrolledText(vte_detalles_ventas, width=94, height=23)
                scrolledtext1.grid(row=0,column=0,columnspan=10)



                InDatosScrollText()
                vte_detalles_ventas.mainloop()




            def create_treeview(parent):


                def OctenerRegistro():
                    recorer = tree.get_children()
                    for r in recorer:
                        tree.delete(r)
                    #query = "SELECT * from registro_ventas fecha"
                    query = 'SELECT * FROM registro_ventas WHERE fecha LIKE ?'
                    datos = ConecionSql().run_query(query,parameters=(str(OctenerFecha()[1])+'%',))
                    # Insertar los datos de la tabla en el TreeView
                    for producto in datos:
                        tree.insert("", "end", text=producto[1],
                                    values=(producto[2], producto[3], producto[4], producto[5], producto[6],producto[7]))

                def Devolver():
                    producto, cantidad, codigo, fecha = "",0,"",""
                    seleccion = tree.focus()

                    # Obtener los valores de la fila seleccionada
                    producto = tree.item(seleccion)["text"]
                    cantidad = tree.item(seleccion)["values"][3]
                    codigo = tree.item(seleccion)["values"][4]
                    fecha = tree.item(seleccion)["values"][1]
                    valores_fila = tree.item(seleccion)["values"]

                    fecha_actual = OctenerFecha()[1]

                    fecha = fecha.split('-')
                    fecha = fecha[0]+fecha[1]+fecha[2]

                    fecha_actual = fecha_actual.split('-')
                    fecha_actual = fecha_actual[0]+fecha_actual[1]+fecha_actual[2]

                    if fecha != fecha_actual:
                        mb.showwarning("Error","Este producto ya no se puede devolver")
                        return

                    # Imprimir los valores de la fila seleccionada
                    print("Datos seleccionados:", producto,' ',cantidad,' ',codigo,' ',fecha)

                    resultado = mb.askyesno("Confirmacion","Estas seguro que deseas devolver este producto")

                    if resultado:


                        query="SELECT cantidad FROM product WHERE name =?"
                        dato= ConecionSql().run_query(query,parameters=(producto,)).fetchall()[0][0]
                        print('repuesta de consulta: ',dato)

                        cantidad = cantidad + dato

                        query = '''UPDATE product
                                 SET cantidad = ?
                                 WHERE name = ?'''
                        try:
                            ConecionSql().run_query(query,parameters=(cantidad,producto))
                            mb.showinfo("Exito",f"Devolucion exitosa el stock del producto ahora es ({cantidad})")

                            query='''DELETE FROM registro_ventas
                            WHERE nombre = ? and identificador = ?
                            '''
                            ConecionSql().run_query(query,parameters=(producto,codigo))

                        except Exception as e:
                            mb.showerror("Error: "+ e)

                        RegistrarEvento("Hizo devolucion",producto)
                        OctenerRegistro()

                    else:
                        print("Accion cancelada")
                        return







                tree = ttk.Treeview(parent, columns=("Column1", "Column2", "Column3", "Column4", "Column5","Column6"))
                tree.heading("#0", text="Nombre del producto")
                tree.heading("Column1", text="Precio")
                tree.heading("Column2", text="Fecha ventas")
                tree.heading("Column3", text="Vendedor")
                tree.heading("Column4", text="Cantidad")
                tree.heading("Column5", text="Descuento")
                tree.heading("Column6", text="Identificador")

                # Establecer el ancho de las columnas
                tree.column("#0", width=500)
                tree.column("Column1", width=150)
                tree.column("Column2", width=200)
                tree.column("Column3", width=350)
                tree.column("Column4", width=100)
                tree.column("Column5", width=100)
                tree.column("Column6", width=150)


                # Configurar el Scrollbar horizontal
                scrollbar_x = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
                tree.configure(xscrollcommand=scrollbar_x.set)


                # Menu ppo____________________________________________


                popup = Menu(parent, tearoff=0)

                # Adding Menu Items
                popup.add_command(label="Devolver", command=Devolver)
                popup.add_separator()
                popup.add_command(label="Abrir en venta detallada", command= DetallesVentas)

                def menu_popup(event):
                    # display the popup menu
                    try:
                        popup.tk_popup(event.x_root, event.y_root, 0)
                    finally:
                        # Release the grab
                        popup.grab_release()

                tree.bind("<Button-3>", menu_popup)
                # END_Menu ppo____________________________________________

                tree.pack(fill="both", expand=True)
                scrollbar_x.pack(fill="x")

                OctenerRegistro()

                return tree

            f1.destroy()
            # Crear un Frame principal usando place
            main_frame = Frame(w, width=dimension_ancho, height=700,bg=color_fondo)
            main_frame.place(x=0, y=45)

            # Crear el LabelFrame con cajas y etiquetas dentro del Frame principal
            label_frame_left = ttk.LabelFrame(main_frame, text="Filtrar registros", padding=10)
            label_frame_left.place(x=20, y=10, width=400, height=650)






            # Agregar cajas y etiquetas dentro del LabelFrame
            label_text = StringVar()
            label_text.set("Total:           ")
            lb_total = ttk.Label(label_frame_left, textvariable=label_text , font=26).grid(row=0, column=0)

            year_label = Label(label_frame_left, text="Año:")
            year_label.grid(row=1, column=0)

            year_entry = ttk.Entry(label_frame_left)
            year_entry.grid(row=1, column=1)

            month_label = Label(label_frame_left, text="Mes:")
            month_label.grid(row=2, column=0)

            month_entry = ttk.Entry(label_frame_left)
            month_entry.grid(row=2, column=1)

            day_label = Label(label_frame_left, text="Dia:")
            day_label.grid(row=3, column=0)

            day_entry = ttk.Entry(label_frame_left)
            day_entry.grid(row=3, column=1)

            hour_label = Label(label_frame_left, text="Hora:")
            hour_label.grid(row=4, column=0)

            hour_entry = Entry(label_frame_left)
            hour_entry.grid(row=4, column=1)

            submit_button = Button(label_frame_left, text="Buscar", command=BuscarRegistro).grid(row=5, column=1)

            separator_vertical = ttk.Separator(label_frame_left, orient='horizontal')
            separator_vertical.grid(row=6,column=0, sticky='ew', padx=0,pady=20)
            separator_vertical2 = ttk.Separator(label_frame_left, orient='horizontal')
            separator_vertical2.grid(row=6, column=1, sticky='ew', padx=0, pady=20)
            separator_vertical3 = ttk.Separator(label_frame_left, orient='horizontal')
            separator_vertical3.grid(row=6, column=0, sticky='ew', padx=0, pady=20)



            lista_usuarios=ConecionSql().run_query(query="SELECT  nombre from usuario").fetchall()
            nombres_usuarios = [usuario[0] for usuario in lista_usuarios]

            lb_selecione_usuario= Label(label_frame_left,text="Usuario")
            lb_selecione_usuario.grid(row=8,column=0)
            cb_usearios= ttk.Combobox(label_frame_left,values=nombres_usuarios)
            cb_usearios.grid(row=8,column=1,pady=10)
            #cb_usearios.bind("<<ComboboxSelected>>",BusquedaUsuarios)

            year_label2 = Label(label_frame_left, text="Año:")
            year_label2.grid(row=9, column=0)

            year_entry2 = ttk.Entry(label_frame_left)
            year_entry2.grid(row=9, column=1)

            month_label2 = Label(label_frame_left, text="Mes:")
            month_label2.grid(row=10, column=0)

            month_entry2 = ttk.Entry(label_frame_left)
            month_entry2.grid(row=10, column=1)

            day_label2 = Label(label_frame_left, text="Dia:")
            day_label2.grid(row=11, column=0)

            day_entry2 = ttk.Entry(label_frame_left)
            day_entry2.grid(row=11, column=1)

            hour_label2 = Label(label_frame_left, text="Hora:")
            hour_label2.grid(row=12, column=0)

            hour_entry2 = Entry(label_frame_left)
            hour_entry2.grid(row=12, column=1)

            submit_button2 = Button(label_frame_left, text="Buscar", command=BusquedaRegistroUsuarioAvanzada).grid(row=13, column=1)



            separator_vertical = ttk.Separator(label_frame_left, orient='horizontal')
            separator_vertical.grid(row=14, column=0, sticky='ew', padx=0, pady=20)
            separator_vertical2 = ttk.Separator(label_frame_left, orient='horizontal')
            separator_vertical2.grid(row=14, column=1, sticky='ew', padx=0, pady=20)
            separator_vertical3 = ttk.Separator(label_frame_left, orient='horizontal')
            separator_vertical3.grid(row=14, column=0, sticky='ew', padx=0, pady=20)

            Detalles_Venta = Button(label_frame_left, text="Detalles de ventas", command=DetallesVentas,width=35).grid(row=15,column=0,columnspan=2)

            # Crear el LabelFrame con el TreeView y el Scrollbar dentro del Frame principal
            label_frame_right = ttk.LabelFrame(main_frame, text="Detalles de registros", padding=10)
            label_frame_right.place(x=430, y=10, width=950, height=650)

            # Agregar el TreeView dentro del LabelFrame con Scrollbar
            treeview = create_treeview(label_frame_right)















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
                vte_ajustar_dolar.attributes("-topmost", True)
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
                    dato1 = 'color_menu'
                    query = "UPDATE configuraciones SET  atributos=? WHERE nombre_cf=?"
                    dato = caja_color_menu.get()

                    try:
                        # Obtiene el valor RGB del nombre de color
                        r, g, b = vte_editar_programa.winfo_rgb(dato)
                        # Actualiza la base de datos con el valor RGB
                        parameters = (dato, dato1)
                        ConecionSql().run_query(query, parameters)
                        caja_color_menu.delete(0, END)
                        reiniciar= mb.askokcancel("Alerta","Para aplicar los cambios es nesesario reiniciar ")
                        if reiniciar:
                            python = sys.executable
                            os.execl(python, python, *sys.argv)

                    except TclError:
                        # Si el color no es válido, muestra un mensaje de error
                        mb.showerror("Error", "El color ingresado no es válido")





                def CambiarColorTabla(event):
                    dato1 = 'color_tabla'
                    query = "UPDATE configuraciones SET  atributos=? WHERE nombre_cf=?"
                    dato = caja_color_tabla.get()

                    try:
                        # Obtiene el valor RGB del nombre de color
                        r, g, b = vte_editar_programa.winfo_rgb(dato)
                        # Actualiza la base de datos con el valor RGB
                        parameters = (dato, dato1)
                        ConecionSql().run_query(query, parameters)
                        caja_color_tabla.delete(0, END)
                        reiniciar= mb.askokcancel("Alerta","Para aplicar los cambios es nesesario reiniciar ")
                        if reiniciar:
                            python = sys.executable
                            os.execl(python, python, *sys.argv)

                    except TclError:
                        # Si el color no es válido, muestra un mensaje de error
                        mb.showerror("Error", "El color ingresado no es válido")

                vte_editar_programa=Toplevel()
                vte_editar_programa.attributes("-topmost", True)
                vte_editar_programa.title("Editar estilo del programa")
                vte_editar_programa.resizable(0,0)


                lb_color_fondo=Label(vte_editar_programa,text="Color del fondo").grid(row=0,column=0)
                caja_color_fondo=ttk.Entry(vte_editar_programa)
                caja_color_fondo.grid(row=0,column=1)

                lb_color_tabla=Label(vte_editar_programa,text="color de tablas").grid(row=1,column=0)
                caja_color_tabla=ttk.Entry(vte_editar_programa)
                caja_color_tabla.grid(row=1,column=1)
                caja_color_tabla.bind('<Return>', CambiarColorTabla)

                lb_color_menu=Label(vte_editar_programa,text="Color del menu").grid(row=2,column=0)
                caja_color_menu=ttk.Entry(vte_editar_programa)
                caja_color_menu.grid(row=2,column=1)
                caja_color_menu.bind('<Return>', CambiarColor)

                vte_editar_programa.mainloop()

            def Actualizar():
                try:
                    resultado = os.system("git pull")
                    if resultado == 0:
                        mb.showinfo("Actualización", "¡El programa ha sido actualizado exitosamente!")
                    elif resultado == 256:
                        mb.showinfo("Actualización", "El programa ya está actualizado.")
                    else:
                        mb.showerror("Error", "Hubo un problema al intentar actualizar el programa.")
                except Exception as e:
                    mb.showerror("Error", f"No se pudo actualizar el programa: {str(e)}")


            def Servidor():
                from flask import Flask, render_template, request
                import cv2
                import pyzbar

                app = Flask(__name__)

                @app.route('/')
                def index():
                    return render_template('index.html')

                @app.route('/procesar_codigo', methods=['POST'])
                def procesar_codigo():
                    codigo = request.form['codigo']
                    # Aquí puedes procesar el código escaneado
                    return 'Código escaneado: {}'.format(codigo)

                if __name__ == '__main__':
                    app.run(host='192.168.0.101', port=5001, debug=True)


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
                vte_usuarios.attributes("-topmost", True)
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
                lb_nueva_contraseña = Label(vt_cambiar_contra, text="Nueva contraseña").grid(row=0, column=0, pady=5, padx=10)
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
                vte_comprovacion.attributes("-topmost", True)
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
            bt_actualizar = Button(text="Actualizar Programa",command=Actualizar).place(x=350,y=350)
            bt_servidor = Button(text="Activar Servidor",command=Servidor).place(x=550,y=350)






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
            bttn(0, 340, 'EVENTOS       ', color_menu, color_menu, Notificaciones, "iconos/notificacion.png")
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

        estilo_barra = ttk.Style()
        estilo_barra.configure("My.TFrame", background="#CCFFFF")
        #barra_superior.configure(style="My.TFrame")


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



        lb_titulo= Label(barra_superior,text=nombre_negocio,bd=0,font=20,bg=color_fondo,fg=color_fuente).place(x=70,y=12)
        lb_ganancia_hoy = Label(barra_superior, textvariable=ganancia_hoy, bd=0, font=20, bg=color_fondo,fg=color_fuente).place(x=480, y=12)
        lb_usuario = Label(barra_superior, text='Usuario: '+nombre_usr, bd=0, font=20, bg=color_fondo, fg=color_fuente).place(x=850, y=12)
        lb_total_ventas_hoy = Label(barra_superior, textvariable=total_hoy, bd=0, font=20, bg=color_fondo, fg=color_fuente).place(x=1150, y=12)
        OctenerTotalDeHoy()
        calcular_ganancia_hoy()
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

            query="SELECT atributos FROM configuraciones WHERE nombre_cf= 'nombre_negocio'"
            nombre_negocio=ConecionSql().run_query(query,).fetchall()[0][0]
            l2 = Label(signin_win, text=nombre_negocio, fg='#ff4f5a', bg='white')
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

            def signin_cmd(event):

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
                        app = Inicio(nombre_usr,permiso_usr,nombre_negocio)

                except IndexError:
                    mb.showwarning("Error", "Contraseña incorrecta")




            # ------------------------------------------------------
            e2.bind("<Return>", signin_cmd)

            Button(f1, width=39, pady=7, text='Iniciar secion', bg='#ff4f5a', fg='white', border=0, command=lambda :signin_cmd("")).place(x=35,
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







class PedirHora:
    def __int__(self):
        import subprocess

        def cambiar_hora():
            # Desactivar la sincronización automática de tiempo
            subprocess.run(["sudo", "timedatectl", "set-ntp", "off"])

            # Obtener los valores de las cajas de texto
            año = entry_año.get()
            mes = entry_mes.get()
            dia = entry_dia.get()
            hora = entry_hora.get()
            minuto = entry_minuto.get()

            # Formatear la fecha y hora
            fecha_hora = f"{año}-{mes}-{dia} {hora}:{minuto}:00"

            # Construir el comando
            comando = f"timedatectl set-time '{fecha_hora}'"

            # Ejecutar el comando
            subprocess.run(["pkexec", "bash", "-c", comando])

            # Volver a activar la sincronización automática de tiempo
            subprocess.run(["sudo", "timedatectl", "set-ntp", "on"])

            ventana.destroy()
            verificar()

        # Crear la ventana principal
        ventana =   Tk()
        ventana.title("Cambiar Hora")

        # Crear y colocar las etiquetas y cajas de texto
        ttk.Label(ventana, text="Año:").grid(row=0, column=0, padx=5, pady=5)
        entry_año = ttk.Entry(ventana)
        entry_año.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(ventana, text="Mes:").grid(row=1, column=0, padx=5, pady=5)
        entry_mes = ttk.Entry(ventana)
        entry_mes.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(ventana, text="Día:").grid(row=2, column=0, padx=5, pady=5)
        entry_dia = ttk.Entry(ventana)
        entry_dia.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(ventana, text="Hora:").grid(row=3, column=0, padx=5, pady=5)
        entry_hora = ttk.Entry(ventana)
        entry_hora.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(ventana, text="Minuto:").grid(row=4, column=0, padx=5, pady=5)
        entry_minuto = ttk.Entry(ventana)
        entry_minuto.grid(row=4, column=1, padx=5, pady=5)

        # Botón para cambiar la hora
        btn_cambiar_hora = ttk.Button(ventana, text="Cambiar Hora", command=cambiar_hora)
        btn_cambiar_hora.grid(row=5, column=0, columnspan=2, pady=10)

        # Iniciar el bucle principal de Tkinter
        ventana.mainloop()


if __name__ == '__main__':

        verificar()




