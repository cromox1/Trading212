import psycopg2

conn = psycopg2.connect(host="localhost", user="postgres", password="H0meBase")

cur = conn.cursor()

sqlcommand = """INSERT INTO persontwo
SELECT DISTINCT
3,
'LastName3',
'FirstName3',
'Address3',
'City3'
FROM persontwo
WHERE NOT EXISTS(SELECT DISTINCT PersonID FROM persontwo WHERE PersonID = 3);"""

# sqlcommand = """INSERT INTO persontwo
# SELECT
# 5,
# 'LastName5',
# 'FirstName5',
# 'Address5',
# 'City5'
# FROM persontwo
# WHERE NOT EXISTS(SELECT PersonID FROM persontwo WHERE PersonID = 5);"""

cur.execute(sqlcommand)

conn.commit()
cur.close()
conn.close()