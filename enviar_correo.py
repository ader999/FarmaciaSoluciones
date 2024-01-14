import re
import smtplib, ssl
from sql import Others as sql
def fecha():
        import time
        timestr = time.strftime("%Y-%m-%d")
        return timestr
query="select * from registro_ventas where fecha LIKE ?"
print(fecha())
parameters=(fecha()+'%',)
datos=str(sql().run_query(query,parameters).fetchall())
limpiando_datos=datos.replace(')','\n')
l=re.sub("[(]","",limpiando_datos)

print(l)
query="select sum(precio) from registro_ventas where fecha LIKE ?"
total="total= "+str(sql().run_query(query,parameters).fetchall())
# on rentre les renseignements pris sur le site du fournisseur

