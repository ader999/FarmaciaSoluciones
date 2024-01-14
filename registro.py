from datetime import datetime
from sql import Others as sql


class Registro:
    def eliminar_t(self):
        with open("totalHoy", "r")as f:

          try:
            ree=f.read().split()[0]
            characters = "'[',"
            ree="".join( x for x in ree if x not in characters)

            ree=str(ree)

            print(ree)
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            fecha=str(timestampStr.split()[0])
            k=[ree,fecha]
            if k[1] != k[0]:
                query="DELETE FROM ventas"
                sql().run_query(query,)
                print("Exito al borrar registro")
            else:print("no pasa nada")

          except:print("Error registro")


