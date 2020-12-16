import psycopg2

conn = psycopg2.connect(host="localhost", user="postgres", password="H0meBase")

cur = conn.cursor()
sqlcommand = """INSERT INTO persontwo VALUES
(1, 
'LastName1', 
'FirstName2', 
'Address1', 
'City1');"""

cur.execute(sqlcommand)

conn.commit()
cur.close()
conn.close()