from flask import Flask, jsonify
from flask import request
import sqlite3
import requests
import openpyxl
import urllib.request
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/data')
def get_data():
    well = request.args.get("well")
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT oil, gas, brine FROM table1 WHERE API_WELL_NUMBER = ?', (well,))
    result = cursor.fetchone()
    conn.close()

    if result:
        data = {'oil': result[0], 
                'gas': result[1], 
                'brine': result[2]}
        return jsonify(data)
    else:
        return 'Data not found for the specified well.'

if __name__ == '__main__':
    app.run(port=8080)

data = pd.read_excel('abc.xls')
annual_data = data.groupby('API WELL  NUMBER').sum()
annual_data.to_excel('data.xls',engine='openpyxl')

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS table1 (
                    API_WELL_NUMBER TEXT,
                    oil INTEGER,
                    gas INTEGER,
                    brine INTEGER
                  )''')
data = pd.read_excel('data.xls',usecols=[0,8,9,10])
data.to_csv("data.csv",index=None,header=True)
data_csv=pd.read_csv('data.csv')

sql ='INSERT INTO table1 (API_WELL_NUMBER, oil, gas, brine) VALUES (?,?,?,?)'
for row in data_csv.itertuples(index=False):
    cursor.execute(sql,row)
conn.commit()
conn.close()
