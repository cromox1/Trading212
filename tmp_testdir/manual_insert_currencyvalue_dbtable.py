import psycopg2

def connect_db(host, user, pswd):
    conn = psycopg2.connect(host=host, user=user, password=pswd)
    cur = conn.cursor()
    return cur, conn

def connect_db_commit_close(cur, conn):
    conn.commit()
    cur.close()
    conn.close()

def create_table_if_noexist(dbtable):
    sqlcommand = """CREATE TABLE IF NOT EXISTS """ + dbtable + """ 
    (currencyID int, 
    Currency varchar(10),
    CurrentValue numeric(5,6),
    CurrentMin numeric(5,6),
    CurrentMax numeric(5,6),
    CurrentAverage numeric(5,6),
    Date date );"""
    conn_db = connect_db("localhost", "postgres", "H0meBase")
    cur = conn_db[0]
    conn = conn_db[1]
    cur.execute(sqlcommand)
    connect_db_commit_close(cur, conn)

def put_values_to_dbtable(dbtable, values):
    id = values[0]
    currency = values[1]
    valuex = values[2]
    valuemin = values[3]
    valuemax = values[4]
    valueaverage = values[5]
    date = values[6]
    sqlcommand = """INSERT INTO """ + str(dbtable) + """   
    SELECT DISTINCT """ + id + ',' + currency + ',' + valuex + ',' + valuemin + ',' + valuemax + ','
    + valueaverage + ',' + str(date) + 'FROM ' + str(dbtable) + """
    WHERE NOT EXISTS(SELECT DISTINCT PersonID FROM dailyfxcurrency WHERE id = """ + id + """);"""

    conn_db = connect_db("localhost", "postgres", "H0meBase")
    cur = conn_db[0]
    conn = conn_db[1]
    cur.execute(sqlcommand)
    connect_db_commit_close(cur, conn)