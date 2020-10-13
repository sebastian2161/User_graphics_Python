from flask import *
from functools import wraps
import sqlite3
import pandas as pd
import requests


DATABASE = 'dataweb.db'

app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config.from_object(__name__)

def connect_db():
    con = sqlite3.connect('dataweb.db')
    cursor = con.cursor()
    print('La base funcionò bien')

def run_query(query='',parameters=()):
    conn = sqlite3.connect('dataweb.db')
    cursor = conn.cursor()                 # Crear un cursor
    cursor.execute(query, parameters)                  # Ejecutar una consulta
    if query.upper().startswith('SELECT'):
       data= cursor.fetchall()               # Traer los resultados de un select
       
    else:
        conn.commit()                          # Hacer efectiva la escritura de datos
        data = None
         
    #cursor.close()                         # Cerrar el cursor
    #conn.close()                           # Cerrar la conexión
    #conn.close()                           # Cerrar la conexión
    
    return data




@app.route('/')
def index():

    query = "SELECT id,substr(date,0,8) as date,count(*) as 'cantidad' from User_Grafics  group by id,substr(date,0,8)"
    curs  = run_query(query)

    dates = []
    prices = []

    for x in curs:
        dates.append(x[1])
        prices.append(x[2])

    #print (dates)
    #print (prices)

    return render_template('index.html', title='Inicio', dates=dates, prices=prices)

@app.route('/filtro')
def filtro():

    user = request.args.get('user', 'all')
    
    if user != 'all':

         #query = "SELECT id,substr(date,0,8) as date,count(*) as 'cantidad' from PRICE_HISTORY   where substr(date,0,5) = '%s' and substr(date,6,2) = '%s' group by id,substr(date,0,8) " % (user)
         query = "SELECT id,substr(date,0,8) as date,count(*) as 'cantidad' from User_Grafics   where id = '%s' group by id,substr(date,0,8)" % (user)
         curs  = run_query(query)

    else:
    
         query = "SELECT id,substr(date,0,8) as date,count(*) as 'cantidad' from User_Grafics  group by id,substr(date,0,8)"
         curs  = run_query(query)


    dates = []
    prices = []

    for x in curs:
        dates.append(x[1])
        prices.append(x[2])

    print (dates)
    print (prices)

    return render_template('index.html', title='Inicio', dates=dates, prices=prices)


    #print(year)
    #print(month)

if __name__ == '__main__':
    app.run(port = 3000, debug=True)



