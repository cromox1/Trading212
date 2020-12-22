import psycopg2
import datetime

def connect_db(host, user, pswd):
    conn = psycopg2.connect(host=host, user=user, password=pswd)
    cur = conn.cursor()
    return cur, conn

def connect_db_close(cur, conn):
    cur.close()
    conn.close()

def create_table_if_noexist(dbtable, cur, conn):
    sqlcommand = """CREATE TABLE IF NOT EXISTS """ + dbtable + """ 
    (ID int, 
    Currency varchar(10),
    CurrencyValue numeric(10,6),
    CurrencyMin numeric(10,6),
    CurrencyMax numeric(10,6),
    CurrencyAve numeric(10,6),
    DateTime timestamp);"""

    print()
    print(sqlcommand)
    print()
    cur.execute(sqlcommand)
    conn.commit()
    return cur, conn

def put_values_to_dbtable(dbtable, values, cur, conn):
    id = values[0]
    currency = values[1]
    valuex = values[2]
    valuemin = values[3]
    valuemax = values[4]
    valueaverage = values[5]
    date1 = values[6]

    sqlcommand = "INSERT INTO " + str(dbtable) \
                + '\n' + "SELECT DISTINCT " \
                + str(id) + ", '" \
                + str(currency) + "', " \
                + str(valuex) + ", " \
                + str(valuemin) + ", " \
                + str(valuemax) + ", " \
                + str(valueaverage) + ", " \
                + "TO_TIMESTAMP('" + str(date1) + "', 'YYYY-MM-DD HH24:MI:SS')" \
                + '\n' + "WHERE NOT EXISTS" \
                + "\n" + "(SELECT * FROM " + str(dbtable) + " WHERE ID = " + str(id) + ");"
    # + str(date) + ", \n'" + str(time) \

    # sqlcommand = """INSERT INTO """ + str(dbtable) + """
    #     SELECT DISTINCT """ + str(id) + ',' + str(currency) + ',' + str(valuex) + ',' + str(valuemin) + ',' + \
    #              str( valuemax) + ',' + str(valueaverage) + ',' + str(date) \
    #              + ' FROM ' + str(dbtable) + """
    #     WHERE NOT EXISTS(SELECT DISTINCT PersonID FROM dailyfxcurrency WHERE id = """ + str(id) + """);"""

    print()
    print(sqlcommand)
    print()

    cur.execute(sqlcommand)
    conn.commit()
    return cur, conn


# TEST
conn_db = connect_db("localhost", "postgres", "H0meBase")
cur = conn_db[0]
conn = conn_db[1]

dbtouse = 'dbtestsixx'
create_table_if_noexist(dbtouse, cur, conn)
# DATE =  2020-12-16 / 14:56
# GBP-USD  =  1.354775  / min  1.336765  / max  1.354775  / avg  1.3462247916666668
# datatext = (20201216145600, 'GBP-USD' , 1.354775 , 1.336765 , 1.354775 , 1.3462247916666668 , "2020-12-16\n14:56:00")

datex = '2020-12-17 12:35:07'
id = int(datetime.datetime.strptime(datex, '%Y-%m-%d %H:%M:%S').timestamp())
datatext = (id, 'GBP-USD' , 1.35477 , 1.33676 , 1.35477 , 1.346221234567 , datex)

put_values_to_dbtable(dbtouse, datatext, cur, conn)

connect_db_close(cur, conn)
