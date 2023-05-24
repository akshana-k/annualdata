import requests
import openpyxl
import urllib.request
url = 'https://ohiodnr.gov/static/documents/oil-gas/production/20110309_2020_1%20-%204.xls'
filename = 'production_data.xls'

response = requests.get(url)
with open(filename, 'wb') as file:
    file.write(response.content)
import pandas as pd

data = pd.read_excel('abc.xls')


annual_data = data.groupby('API WELL  NUMBER').sum()

annual_data.to_excel('data.xls',engine='openpyxl')



import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Create a table for the data
cursor.execute('''CREATE TABLE IF NOT EXISTS table1 (
                    API_WELL_NUMBER TEXT,
                    oil INTEGER,
                    gas INTEGER,
                    brine INTEGER
                  )''')

# Read the annual data from the Excel file
data = pd.read_excel('data.xls',usecols=[0,8,9,10])
data.to_csv("data.csv",index=None,header=True)
data_csv=pd.read_csv('data.csv')






# Insert the data into the table
sql ='INSERT INTO table1 (API_WELL_NUMBER, oil, gas, brine) VALUES (?,?,?,?)'
for row in data_csv.itertuples(index=False):
    cursor.execute(sql,row)

# Commit the changes and close the connection
conn.commit()
conn.close()



from flask import Flask, jsonify
from flask import request
import sqlite3

app = Flask(__name__)

@app.route('/data')
def get_data():
    well = request.args.get("well")

    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Retrieve the data for the specified well
    cursor.execute('SELECT oil, gas, brine FROM table1 WHERE API_WELL_NUMBER = ?', (well,))
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    if result:
        # Create a dictionary from the database result
        data = {'oil': result[0], 
                'gas': result[1], 
                'brine': result[2]}
        return jsonify(data)
    else:
        return 'Data not found for the specified well.'

if __name__ == '__main__':
    app.run(port=8080)