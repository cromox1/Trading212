import psycopg2

conn = psycopg2.connect(host="localhost", user="postgres", password="H0meBase")

cur = conn.cursor()
dbtable = 'persontwo'

# sqlcommand = """CREATE TABLE IF NOT EXISTS persontwo
# (PersonID int,
# LastName varchar(255),
# FirstName varchar(255),
# Address varchar(255),
# City varchar(255) );"""

sqlcommand = "CREATE TABLE IF NOT EXISTS " + str(dbtable) \
+ " (PersonID int," \
+ " LastName varchar(255)," \
+ " FirstName varchar(255)," \
+ " Address varchar(255), "\
+ " City varchar(255) );"

print(sqlcommand)

cur.execute(sqlcommand)
conn.commit()
cur.close()
conn.close()