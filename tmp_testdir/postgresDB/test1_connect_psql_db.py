import psycopg2

conn = psycopg2.connect(host="localhost", user="postgres", password="H0meBase")

cur = conn.cursor()
sqlcommand = 'SELECT table_name,table_schema FROM INFORMATION_SCHEMA.TABLES;'
cur.execute(sqlcommand)

rows = cur.fetchall()
if len(rows) >= 1:
    i = 1
    for row in rows:
        print(str(i) + ') ' + str(row))
        i = i+1
else:
    print('SQLTABLE EMPTY - NO DATA')

cur.close()
conn.close()
