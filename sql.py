import sqlite3
import tkinter as tk
from tkinter import ttk, scrolledtext

class Others:

    def run_query(self,query,parameters=()):


                self.nombre_db="basededatos.db"
                with sqlite3.connect(self.nombre_db) as conn:
                    cursor= conn.cursor()
                    resultado= cursor.execute(query,parameters)
                    conn.commit()



                return resultado




