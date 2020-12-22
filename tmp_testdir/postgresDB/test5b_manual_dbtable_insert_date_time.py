import psycopg2
import datetime

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
    CurrentValue numeric(9,5),
    CurrentMin numeric(9,5),
    CurrentMax numeric(9,5),
    CurrentAverage numeric(9,5),
    Date date);"""
    conn_db = connect_db("localhost", "postgres", "H0meBase")
    cur = conn_db[0]
    conn = conn_db[1]
    print(sqlcommand)
    cur.execute(sqlcommand)
    connect_db_commit_close(cur, conn)

def put_values_to_dbtable(dbtable, values):
    id = values[0]
    currency = values[1]
    valuex = values[2]
    valuemin = values[3]
    valuemax = values[4]
    valueaverage = values[5]
    date1 = values[6]
    time1 = values[7]
    date2 = datetime.datetime.strptime(date1 + ' ' + time1, '%Y-%m-%d %H:%M:%S')
    print('date2 = ', type(date2))
    # print('time = ', type(time))

    sqlcommand = "INSERT INTO " + str(dbtable) \
                + '\n' + "SELECT DISTINCT " + '\n' + str(id) + ", \n'" + str(currency) + "', \n" + str(valuex) \
                + ", \n" + str(valuemin) + ", \n" + str(valuemax) + ", \n" + str(valueaverage) + ", \n" \
                + str(date2) \
                + "\nFROM " + str(dbtable) \
                + '\n' + "WHERE NOT EXISTS(SELECT DISTINCT currencyID FROM " + str(dbtable) \
                + " WHERE currencyID = " + str(id) + ");"
    # + str(date) + ", \n'" + str(time) \

    # sqlcommand = """INSERT INTO """ + str(dbtable) + """
    #     SELECT DISTINCT """ + str(id) + ',' + str(currency) + ',' + str(valuex) + ',' + str(valuemin) + ',' + \
    #              str( valuemax) + ',' + str(valueaverage) + ',' + str(date) \
    #              + ' FROM ' + str(dbtable) + """
    #     WHERE NOT EXISTS(SELECT DISTINCT PersonID FROM dailyfxcurrency WHERE id = """ + str(id) + """);"""

    conn_db = connect_db("localhost", "postgres", "H0meBase")
    cur = conn_db[0]
    conn = conn_db[1]
    print(sqlcommand)
    cur.execute(sqlcommand)
    connect_db_commit_close(cur, conn)

# TEST
dbtouse = 'dbtesttwo'
create_table_if_noexist(dbtouse)
# DATE =  2020-12-16 / 14:56
# GBP-USD  =  1.354775  / min  1.336765  / max  1.354775  / avg  1.3462247916666668
# datatext = (20201216145600, 'GBP-USD' , 1.354775 , 1.336765 , 1.354775 , 1.3462247916666668 , "2020-12-16\n14:56:00")
datatext = (20201216145600, 'GBP-USD' , 1.35477 , 1.33676 , 1.35477 , 1.34622 , "2020-12-16", "14:56:00")
put_values_to_dbtable(dbtouse, datatext)
