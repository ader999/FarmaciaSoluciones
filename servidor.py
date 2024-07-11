import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import sqlite3
import webbrowser
from datetime import date, datetime
import matplotlib.pyplot as plt
import io
import base64


class ConecionSql:
    def run_query(self, query, parameters=()):
        with sqlite3.connect('basededatos.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

class Funciones:
    def GeneraContraseña(self):
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



class MetricsQueries:
    def __init__(self, conexion):
        self.conexion = conexion

    def get_top_5_products(self):
        query = """
        SELECT nombre, SUM(cantidad) as total_vendido
        FROM registro_ventas
        GROUP BY nombre
        ORDER BY total_vendido DESC
        LIMIT 8
        """
        result = self.conexion.run_query(query)
        return result.fetchall()

    def get_sales_per_hour(self):
        query = """
        SELECT 
            SUBSTR(fecha, 12, 2) as hora, 
            SUM(precio * cantidad) as total_por_hora
        FROM registro_ventas
        WHERE CAST(SUBSTR(fecha, 12, 2) AS INTEGER) BETWEEN 5 AND 22
        GROUP BY hora
        ORDER BY hora
        """
        result = self.conexion.run_query(query)
        return result.fetchall()

    def get_sales_per_hour_today(self):
        query = """
            SELECT 
                SUBSTR(fecha, 12, 2) as hora, 
                SUM(precio * cantidad) as total_por_hora
            FROM registro_ventas
            WHERE SUBSTR(fecha, 1, 10) = DATE('now', 'localtime')  -- Filtrar por el día actual (extraer YYYY-MM-DD)
              AND CAST(SUBSTR(fecha, 12, 2) AS INTEGER) BETWEEN 5 AND 22  -- Filtrar por el rango de horas
            GROUP BY hora
            ORDER BY hora
            """
        result = self.conexion.run_query(query)
        return result.fetchall()

    def get_average_sales_per_user(self):
        query = """
        SELECT usuario, AVG(precio * cantidad) as promedio_ventas
        FROM registro_ventas
        GROUP BY usuario
        ORDER BY promedio_ventas DESC
        """
        result = self.conexion.run_query(query)
        return result.fetchall()

    def get_sales_summary_today(self):
        query = """
        SELECT 
            SUM(precio * cantidad) as total_ventas,
            SUM((precio - descuento) * cantidad) as total_ganancias
        FROM registro_ventas
        WHERE SUBSTR(fecha, 1, 10) = DATE('now', 'localtime')  -- Filtrar por el día actual (extraer YYYY-MM-DD)
        """
        result = self.conexion.run_query(query)
        return result.fetchone()


    def calcular_ganancia_hoy(self):
        try:
            # Obtener la fecha de hoy en formato YYYY-MM-DD
            fecha_hoy= datetime.now()
            fecha_hoy = fecha_hoy.today().strftime('%Y-%m-%d')

            # Query para obtener los productos vendidos en el día con sus cantidades
            query_ventas = 'SELECT nombre, cantidad FROM registro_ventas WHERE fecha LIKE ?'

            # Crear una instancia de ConecionSql
            conexion_sql = ConecionSql()

            # Ejecutar la consulta para obtener los productos vendidos hoy
            productos_vendidos = conexion_sql.run_query(query_ventas, (fecha_hoy + '%',)).fetchall()

            # Inicializar la ganancia total del día
            ganancia_total = 0

            # Calcular la ganancia total del día sumando la diferencia entre precio con ganancia y sin ganancia
            for producto in productos_vendidos:
                nombre, cantidad = producto

                # Consultar la tabla 'product' para obtener el precio con y sin ganancia del producto
                query_producto = 'SELECT price, cantidad_sin_ganansia FROM product WHERE name = ?'
                resultado_producto = conexion_sql.run_query(query_producto, (nombre,)).fetchone()

                if resultado_producto:
                    precio_con_ganancia, precio_sin_ganancia = resultado_producto
                    ganancia_producto = (precio_con_ganancia - precio_sin_ganancia) * cantidad
                    ganancia_total += ganancia_producto

            # Retornar la ganancia total del día como un string formateado
            return f'Total de Ganancias Hoy: {ganancia_total}'

        except Exception as e:
            print("Error:", str(e))
            return "Error al calcular ganancia hoy"


        except Exception as e:
            print("Error:", str(e))
            return "Error al calcular ganancia hoy"

    def get_sales_per_day_of_week(self):
        query = """
        SELECT 
            STRFTIME('%w', SUBSTR(fecha, 1, 10)) as dia_semana, 
            SUM(precio * cantidad) as total_ventas
        FROM 
            registro_ventas
        GROUP BY 
            dia_semana
        ORDER BY 
            dia_semana

        """
        result = self.conexion.run_query(query)
        return result.fetchall()

    def get_sales_last_7_days(self):
        query = """
        SELECT 
            CASE 
                WHEN STRFTIME('%w', SUBSTR(fecha, 1, 10)) = '0' THEN 'Domingo'
                WHEN STRFTIME('%w', SUBSTR(fecha, 1, 10)) = '1' THEN 'Lunes'
                WHEN STRFTIME('%w', SUBSTR(fecha, 1, 10)) = '2' THEN 'Martes'
                WHEN STRFTIME('%w', SUBSTR(fecha, 1, 10)) = '3' THEN 'Miércoles'
                WHEN STRFTIME('%w', SUBSTR(fecha, 1, 10)) = '4' THEN 'Jueves'
                WHEN STRFTIME('%w', SUBSTR(fecha, 1, 10)) = '5' THEN 'Viernes'
                WHEN STRFTIME('%w', SUBSTR(fecha, 1, 10)) = '6' THEN 'Sábado'
            END as dia_semana, 
            SUM(precio * cantidad) as total_ventas
        FROM 
            registro_ventas
        WHERE 
            DATE(SUBSTR(fecha, 1, 10)) >= DATE('now', '-7 days')
        GROUP BY 
            dia_semana
        ORDER BY 
            STRFTIME('%w', SUBSTR(fecha, 1, 10))
        """
        result = self.conexion.run_query(query)
        return result.fetchall()

    def get_sales_last_30_days(self):
        query = """
                SELECT 
                    STRFTIME('%d', SUBSTR(fecha, 1, 10)) as dia_mes, 
                    SUM(precio * cantidad) as total_ventas,
                    SUBSTR(fecha, 1, 10) as fecha_completa
                FROM 
                    registro_ventas
                WHERE 
                    DATE(SUBSTR(fecha, 1, 10)) >= DATE('now', '-30 days')
                GROUP BY 
                    fecha_completa
                ORDER BY 
                    fecha_completa DESC
                """
        result = self.conexion.run_query(query)
        return result.fetchall()

    def get_sales_per_month(self):
        query = """
        SELECT 
            SUBSTR(fecha, 1, 4) AS year, 
            SUBSTR(fecha, 6, 2) AS month, 
            SUM(precio) AS total_ventas
        FROM 
            registro_ventas
        GROUP BY 
            year, month
        ORDER BY 
            year, month;
        """
        result = self.conexion.run_query(query)
        return result.fetchall()






app = Flask(__name__)
app.config['SECRET_KEY'] = '052020202024897nxndxnuuhuhssdhBBFVCXDFFGGHGHJJGH_:=======&&&&%%%$$$##"DSXD$$'


#--------------------------------login-------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicie sesión primero', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(required_permisos):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'permisos' not in session or session['permisos'] != required_permisos:
                flash('No tiene permisos para acceder a esta parte de la aplicació web', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


#--------------------------------------------------------





@app.route('/')
@login_required
def index():
    queries = MetricsQueries(ConecionSql())

    # Obtener datos de las ventas por hora del día actual
    hourly_sales_data_today = queries.get_sales_per_hour_today()
    if not hourly_sales_data_today:
        print("No se encontraron datos de ventas para hoy.")
    else:
        print(f"Datos de ventas por hora para hoy: {hourly_sales_data_today}")

    hours_today = [row[0] for row in hourly_sales_data_today]
    sales_today = [row[1] for row in hourly_sales_data_today]

    # Obtener resumen de ventas y ganancias del día actual
    sales_summary_today = queries.get_sales_summary_today()
    total_ventas = sales_summary_today[0] if sales_summary_today[0] else 0


    # Generar gráfico de ventas totales por hora del día actual
    hourly_sales_plot_url_today = generate_line_chart(hours_today, sales_today,
                                                      'Ventas Totales por Hora - Día Actual',
                                                      'Hora', 'Ventas Totales')

    # Obtener datos de ventas de los últimos 7 días
    sales_last_7_days_data = queries.get_sales_last_7_days()
    last_7_days = [row[0] for row in sales_last_7_days_data]
    sales_last_7_days = [row[1] if row[1] is not None else 0 for row in sales_last_7_days_data]

    # Generar gráfico de ventas de los últimos 7 días
    sales_last_7_days_plot_url = generate_bar_chart(last_7_days, sales_last_7_days,
                                                    'Ventas de los Últimos 7 Días',
                                                    'Día de la Semana', 'Ventas Totales')


    return render_template('index.html',
                           hourly_sales_plot_url_today=hourly_sales_plot_url_today,
                           sales_last_7_days_plot_url=sales_last_7_days_plot_url,
                           total_ventas=total_ventas,
                           total_ganancias=queries.calcular_ganancia_hoy()
                           )

@app.route('/nuevo_producto', methods=['GET', 'POST'])
@login_required
@permission_required('root')
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        price = float(request.form['price'])
        cantidad = float(request.form['cantidad'])
        fecha_vencimiento = request.form.get('fecha_vencimiento', None)
        cantidad_sin_ganansia = float(request.form.get('cantidad_sin_ganansia', 0))
        mesProximoDevovlucion = int(request.form.get('mesProximoDevovlucion', 0))
        descuento = int(request.form.get('descuento', 0))
        cantidad_xmayor = int(request.form.get('cantidad_xmayor', 0))

        query = '''INSERT INTO product (name, price, cantidad, fecha_vencimiento, cantidad_sin_ganansia,
                    mesProximoDevovlucion, descuento, cantidad_xmayor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        parameters = (nombre, price, cantidad, fecha_vencimiento, cantidad_sin_ganansia, mesProximoDevovlucion, descuento, cantidad_xmayor)
        ConecionSql().run_query(query, parameters)

        return redirect(url_for('index'))

    return render_template('nuevo_producto.html')

def get_today_date_string():
    today = datetime.today()
    return today.strftime('%Y-%m-%d')

def convirtiendo_dollar():
    query = "SELECT * FROM configuraciones WHERE nombre_cf='dollar'"
    total_en_dollar = ConecionSql().run_query(query).fetchall()[0]
    total_en_dollar = total_en_dollar[2]
    return total_en_dollar

@app.route('/get_dollar_rate', methods=['GET'])
def get_dollar_rate():
    dollar_rate = convirtiendo_dollar()
    return jsonify({'dollar_rate': dollar_rate})


@app.route('/registros', methods=['GET', 'POST'])
@login_required
def ver_registros():
    conexion = ConecionSql()

    if request.method == 'POST':
        fecha = request.form['fecha']
        usuario = request.form['usuario']
        if fecha and usuario:
            query = "SELECT * FROM registro_ventas WHERE substr(fecha, 1, 10) = ? AND usuario = ?"
            parametros = (fecha, usuario)
        elif fecha:
            query = "SELECT * FROM registro_ventas WHERE substr(fecha, 1, 10) = ?"
            parametros = (fecha,)
        elif usuario:
            query = "SELECT * FROM registro_ventas WHERE usuario = ?"
            parametros = (usuario,)
        else:
            query = "SELECT * FROM registro_ventas WHERE substr(fecha, 1, 10) = ?"
            parametros = (get_today_date_string(),)  # Mostrar registros de la fecha actual si no se especifica ningún filtro

        registros = conexion.run_query(query, parametros)
    else:
        query = "SELECT * FROM registro_ventas WHERE substr(fecha, 1, 10) = ?"
        parametros = (get_today_date_string(),)  # Mostrar registros de la fecha actual si no se especifica ningún filtro
        registros = conexion.run_query(query, parametros)

    return render_template('ver_registros.html', registros=registros)


# Ruta para obtener el contenido del archivo .txt basado en la fecha
@app.route('/ver_registro_txt/<fecha>', methods=['GET'])
def ver_registro_txt(fecha):
    try:
        file_path = os.path.join('registro', 'facturas', fecha)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                contenido = file.read()
            return jsonify({"success": True, "contenido": contenido})
        else:
            return jsonify({"success": False, "error": "Archivo no encontrado"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



@app.route('/notificaciones', methods=['GET', 'POST'])
@login_required
def ver_notificaciones():
    conexion = ConecionSql()

    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        if fecha_inicio and fecha_fin:
            query = "SELECT * FROM notificaciones WHERE substr(fecha, 1, 10) BETWEEN ? AND ?"
            parametros = (fecha_inicio, fecha_fin)
        elif fecha_inicio:
            query = "SELECT * FROM notificaciones WHERE substr(fecha, 1, 10) >= ?"
            parametros = (fecha_inicio,)
        elif fecha_fin:
            query = "SELECT * FROM notificaciones WHERE substr(fecha, 1, 10) <= ?"
            parametros = (fecha_fin,)
        else:
            query = "SELECT * FROM notificaciones"
            parametros = ()

        notificaciones = conexion.run_query(query, parametros)
    else:
        query = "SELECT * FROM notificaciones"
        notificaciones = conexion.run_query(query)

    return render_template('ver_notificaciones.html', notificaciones=notificaciones)


@app.route('/facturar', methods=['GET'])
@login_required
def facturar():

    return render_template('facturar.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    term = request.form['term']
    print(f"Buscando término: {term}")  # Agregar print para debug
    query = "SELECT * FROM product WHERE name LIKE ? LIMIT 10"
    parameters = ('%' + term + '%',)
    results = ConecionSql().run_query(query, parameters).fetchall()
    print(f"Resultados encontrados: {results}")  # Agregar print para debug
    return jsonify(results)


@app.route('/confirmar_venta', methods=['GET', 'POST'])
def confirmar_venta():
    identificador_venta = Funciones().GeneraContraseña()
    if request.method == 'POST':
        data = request.get_json()
        cordobas = float(data['totalCordobas'])
        dolares = float(data['totalDolares'])
        productos = data['productos']
        total = sum([p['subtotal'] for p in productos])

        # Calcular el total pagado y el total restante
        total_pagado = cordobas + (dolares * convirtiendo_dollar())
        total_restante = total - total_pagado
        now = datetime.now()
        formato_de_fecha = now.strftime('%Y-%m-%d-%H-%M-%S')

        # Insertar el registro de la venta en la base de datos
        for producto in productos:
            query = "INSERT INTO registro_ventas (nombre, precio, fecha, usuario, cantidad, identificador, descuento) VALUES (?, ?, ?, ?, ?, ?, ?)"
            parameters = (
                producto['nombre'],
                producto['precio'],
                formato_de_fecha,
                'navegador',
                producto['cantidad'],
                identificador_venta,
                0  # Descuento puede ser calculado si es necesario
            )
            ConecionSql().run_query(query, parameters)

            # Actualizar la cantidad de productos en la tabla product
            query_get_quantity = "SELECT cantidad FROM product WHERE name = ?"
            current_quantity = ConecionSql().run_query(query_get_quantity, (producto['nombre'],)).fetchone()

            if current_quantity is not None:
                if current_quantity[0] is not None:
                    new_quantity = current_quantity[0] - producto['cantidad']
                    if new_quantity < 0:
                        new_quantity = 0  # Ajusta a 0 si la cantidad es negativa

                    query_update = "UPDATE product SET cantidad = ? WHERE name = ?"
                    parameters_update = (new_quantity, producto['nombre'])
                    print(f"Actualizando {producto['nombre']} con nueva cantidad: {new_quantity}")  # Depuración
                    ConecionSql().run_query(query_update, parameters_update)
                else:
                    print(f"Producto {producto['nombre']} tiene cantidad NULL en la base de datos.")  # Depuración
            else:
                print(f"Producto {producto['nombre']} no encontrado en la base de datos.")  # Depuración

        return jsonify({
            'success': True,
            'vuelto': round(total_restante, 2)  # Redondear el vuelto a 2 decimales
        })

    total = request.args.get('total', 0)
    return render_template('confirmar_venta.html', total=total)


@app.route('/imprimir_venta', methods=['POST'])
def imprimir_venta():
    if request.method == 'POST':
        data = request.get_json()

        # Aquí procesas los datos recibidos para imprimirlos
        totalCordobas = data.get('totalCordobas')
        totalDolares = data.get('totalDolares')
        vuelto = data.get('vuelto')
        productos = data.get('productos')

        # Aquí puedes implementar la lógica para enviar los datos a tu sistema de impresión

        # Ejemplo de respuesta de confirmación (puedes adaptarlo según tu implementación)
        return jsonify({'success': True}), 200

    # En caso de método incorrecto o solicitud incorrecta, puedes manejarlo aquí
    return jsonify({'success': False}), 400

# METRICAS------------------------------------------------------------------------------
@app.route('/metricas')
@login_required
@permission_required('root')
def metricas():
    conexion = ConecionSql()
    queries = MetricsQueries(conexion)

    # Obtener datos de los productos más vendidos
    top_products_data = queries.get_top_5_products()
    products = [row[0] for row in top_products_data]
    quantities = [row[1] if row[1] is not None else 0 for row in top_products_data]

    # Generar gráfico de top 5 productos más vendidos
    top_products_plot_url = generate_bar_chart2(products, quantities,
                                               'Top 8 Productos Más Vendidos',
                                               'Productos', 'Cantidad Vendida')

    # Obtener datos de las ventas por hora
    hourly_sales_data = queries.get_sales_per_hour()
    hours = [row[0] for row in hourly_sales_data]
    sales = [row[1] if row[1] is not None else 0 for row in hourly_sales_data]

    # Generar gráfico de ventas totales por hora
    hourly_sales_plot_url = generate_line_chart(hours, sales,
                                                'Ventas Totales por Hora',
                                                'Hora', 'Ventas Totales')

    # Obtener datos del promedio de ventas por usuario
    average_sales_data = queries.get_average_sales_per_user()
    users = [row[0] for row in average_sales_data]
    average_sales = [row[1] if row[1] is not None else 0 for row in average_sales_data]

    # Generar gráfico de promedio de ventas por usuario
    average_sales_plot_url = generate_horizontal_bar_chart(users, average_sales,
                                                           'Promedio de Ventas por Usuario',
                                                           'Promedio de Ventas', 'Usuarios')



    # Obtener datos de ventas por día de la semana
    sales_per_day_data = queries.get_sales_per_day_of_week()
    days_of_week = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    sales_per_day = [row[1] if row[1] is not None else 0 for row in sales_per_day_data]

    # Generar gráfico de ventas por día de la semana
    sales_per_day_plot_url = generate_bar_chart(days_of_week, sales_per_day,
                                                'Ventas por Día de la Semana',
                                                'Día de la Semana', 'Ventas Totales')

    # Obtener datos de ventas de los últimos 30 días
    sales_last_30_days_data = queries.get_sales_last_30_days()
    last_30_days = [f"{row[2]} ({row[0]})" for row in sales_last_30_days_data]
    sales_last_30_days = [row[1] if row[1] is not None else 0 for row in sales_last_30_days_data]

    # Generar gráfico de ventas de los últimos 30 días
    sales_last_30_days_plot_url = generate_bar_chart2(last_30_days, sales_last_30_days,
                                                     'Ventas de los Últimos 30 Días',
                                                     'Día del Mes', 'Ventas Totales')

    # Obtener datos de ventas por mes
    sales_per_month_data = queries.get_sales_per_month()
    months = [f"{int(row[1])}/{int(row[0])}" for row in sales_per_month_data]
    sales_per_month = [row[2] if row[2] is not None else 0 for row in sales_per_month_data]

    # Generar gráfico de ventas por mes
    sales_per_month_plot_url = generate_bar_chart2(months, sales_per_month,
                                                  'Ventas por Mes',
                                                  'Mes del Año', 'Ventas Totales')

    # Obtener datos del promedio de ventas por mes


    return render_template('metricas.html',
                           top_products_plot_url=top_products_plot_url,
                           hourly_sales_plot_url=hourly_sales_plot_url,
                           average_sales_plot_url=average_sales_plot_url,
                           sales_per_day_plot_url=sales_per_day_plot_url,
                           sales_last_30_days_plot_url=sales_last_30_days_plot_url,
                           sales_per_month_plot_url=sales_per_month_plot_url)


def generate_bar_chart(labels, values, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color='blue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    for bar in bars:
        bar.set_color('blue')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url


def generate_bar_chart2(x_data, y_data, title, x_label, y_label):
    fig, ax = plt.subplots()

    cleaned_x_data = []
    cleaned_y_data = []
    for i in range(len(x_data)):
        if y_data[i] is not None:
            cleaned_x_data.append(x_data[i])
            cleaned_y_data.append(y_data[i])

    ax.bar(range(len(x_data)), y_data,
           color='blue')  # Usar rango de la longitud de x_data para las posiciones de las barras

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Establecer los ticks en el eje X
    ax.set_xticks(range(len(x_data)))

    # Formatear las etiquetas del eje X para mostrar solo el día del mes
    ax.set_xticklabels([label.split(' ')[0].split('-')[-1] for label in x_data], rotation=45, fontsize=8)

    # Ajustar el espaciado para que las etiquetas no se corten
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return 'data:image/png;base64,{}'.format(image_base64)


def generate_line_chart(x_data, y_data, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, marker='o', linestyle='-', color='b')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

def generate_line_chart2(data):
    plt.figure(figsize=(10, 6))
    for year, group_data in data.items():
        x_data = [f"{row['month']}-{year}" for row in group_data]
        y_data = [row['average_sales'] for row in group_data]
        plt.plot(x_data, y_data, marker='o', linestyle='-', label=f'Year {year}')

    plt.xlabel('Month-Year')
    plt.ylabel('Average Sales')
    plt.title('Comparison of Average Sales per Month for Different Years')
    plt.xticks(rotation=45)
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

def generate_horizontal_bar_chart(labels, values, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    bars = plt.barh(labels, values, color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gca().invert_yaxis()  # Invertir el eje Y para que los usuarios con mayor promedio aparezcan arriba

    for bar in bars:
        bar.set_color('skyblue')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url


def octener_fecha():
    now = datetime.now()
    fecha_formateada = now.strftime("%Y-%m-%d-%H-%M-%S")
    archivo_fecha = now.strftime("%d-%m-%Y") + ".txt"
    return fecha_formateada, archivo_fecha


@app.route('/registrar_venta', methods=['POST'])
def registrar_venta():
    data = request.json
    ur = data.get('usuario')
    parametros = data.get('parametros')

    fecha_formateada, archivo_fecha = octener_fecha()
    file_name = os.path.join('registro', 'facturas', archivo_fecha)

    if not os.path.exists(file_name):
        with open(file_name, 'x') as file:
            print("The file does not exist, creating a new file.")
    else:
        print("The file already exists, appending to it.")

    # Crear una lista de líneas de productos formateados
    productos = parametros[0].split('\n')
    productos_formateados = []
    for producto in productos:
        nombre, precio, cantidad, subtotal = producto.split()
        productos_formateados.append(f"{nombre:<60}{precio:<10}{cantidad:<10}{subtotal:<10}")

    # Unir las líneas formateadas en una sola cadena
    productos_str = "\n".join(productos_formateados)

    factura = (
        "\n\n                                     FARMACIA SOLUCIONES\n"
        "----------------------------------------------------------------------------------------------\n"
        f"Fecha= {fecha_formateada}\n"
        f"Atendido por= {ur}\n"
        "----------------------------------------------------------------------------------------------\n"
        "Articulos                                                   Precio    Cantidad    SubTotal\n"
        "----------------------------------------------------------------------------------------------\n"
        f"{productos_str}\n"
        "----------------------------------------------------------------------------------------------\n"
        f"Total    =         {parametros[1]}\n"
        f"Pago con =         {parametros[2]}\n"
        f"Vuelto   =         {parametros[3]}\n"
        "----------------------------------------------------------------------------------------------\n"
    )

    with open(file_name, 'a') as file:
        file.write(factura)

    return jsonify({"success": True})

@app.route('/administrar_producto')
@login_required
@permission_required('root')
def administrar_producto():
    products = ConecionSql().run_query("SELECT * FROM product LIMIT 50").fetchall()
    return render_template('administrar_producto.html', products=products)


@app.route('/actualizar_producto', methods=['POST'])
@login_required
@permission_required('root')
def actualizar_producto():
    if request.method == 'POST':
        # Recuperar los datos del producto actualizado desde la solicitud POST
        product_id = request.form['id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        fecha_vencimiento = request.form['fecha_vencimiento']
        descuento = request.form['descuento']
        cantidad_xmayor = request.form['cantidad_xmayor']

        # Ejemplo de actualización en la base de datos (debes ajustar según tu implementación)
        update_query = """
            UPDATE product 
            SET name=?, price=?, cantidad=?, fecha_vencimiento=?, descuento=?, cantidad_xmayor=? 
            WHERE id=?
        """
        parameters = (nombre, precio, cantidad, fecha_vencimiento, descuento, cantidad_xmayor, product_id)

        # Ejecutar la consulta SQL para actualizar el producto
        ConecionSql().run_query(update_query, parameters)

        # Retornar una respuesta de éxito
        return jsonify({'message': 'Producto actualizado correctamente.'})

    # Manejo para otros casos (aunque no debería alcanzarse aquí en este contexto)
    return jsonify({'error': 'Método no permitido'}), 405


@app.route('/buscar_producto', methods=['POST'])
def buscar_producto():
    term = request.form['term']
    query = "SELECT * FROM product WHERE name LIKE ?"
    parameters = ('%' + term + '%',)
    results = ConecionSql().run_query(query, parameters).fetchall()
    print(f"Resultados encontrados: {results}")  # Agregar print para debug
    return jsonify(results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = ConecionSql()
    if request.method == 'POST':
        password = request.form['password']  # Obtener la contraseña del formulario
        user = db.run_query('SELECT * FROM usuario WHERE contraseña = ?', (password,)).fetchone()  # Consulta para verificar la contraseña

        if user:
            session['user_id'] = user[0]  # Asumiendo que el idusr es el primer campo
            session['user_name'] = user[1]  # Asumiendo que el nombre es el segundo campo
            session['permisos'] = user[6]  # Asumiendo que los permisos son el séptimo campo
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Contraseña incorrecta', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('permisos', None)
    flash('Sesión cerrada', 'success')
    return redirect(url_for('login'))




def run_server():
    def Obtener_ip():
        import psutil
        import socket

        # Obtener todas las interfaces de red
        interfaces = psutil.net_if_addrs()

        # Variable para almacenar la dirección IP
        mi_ip = None

        # Buscar la interfaz que tiene una dirección IP en el rango 192.168.x.x
        for interface_name, interface_addresses in interfaces.items():
            for address in interface_addresses:
                if address.family == socket.AF_INET and address.address.startswith('192.168.'):
                    mi_ip = address.address
                    break
            if mi_ip:
                break

        print("La dirección IP es:", mi_ip)
        if mi_ip == None:
            mi_ip = "localhost"

        return mi_ip

    # Obtener la dirección IP
    ip = Obtener_ip()
    abrir_navegador = False
    if abrir_navegador == True:
        webbrowser.open(f"http://{ip}:5002")

    # Ejecutar el servidor Flask
    app.run(host=ip, port=5002, debug=False)

run_server()