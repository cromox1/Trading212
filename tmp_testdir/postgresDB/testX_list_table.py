import psycopg2

conn = psycopg2.connect(host="localhost", user="postgres", password="H0meBase")

cur = conn.cursor()
# sqlcommand = 'SELECT * FROM persons;'
sqlcommand = 'SELECT * FROM persontwo;'
cur.execute(sqlcommand)
## print table header
column_names = [i[0] for i in cur.description]
print(' ,  '.join(column_names))

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