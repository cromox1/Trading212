import requests
import datetime
import psycopg2

def currency_date_value(baseurl, currency):
    url = baseurl + currency
    out1 = requests.get(url = url)
    data = []
    hari = ''
    for line in out1.text.split('\n'):
        if 'data-value=' in line:
            if 'data-value="--' not in line:
                data = data + [line]
        if 'data-type="date"' in line:
            hari = line
    tarikh = hari.split('content=')[-1].split('"')[1].replace('T', ' ') + ':01'
    datalast = data[-1]
    data_list = [float(x) for x in datalast.split('=')[1].split('"')[1].split(',')]
    avg = sum(data_list)/len(data_list)
    id = int(datetime.datetime.strptime(tarikh, '%Y-%m-%d %H:%M:%S').timestamp())
    return id, currency.upper(), data_list[-3], min(data_list), max(data_list), avg, tarikh

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

    print()
    print(sqlcommand)
    print()

    cur.execute(sqlcommand)
    conn.commit()
    return cur, conn

# TEST

def collectdata_from_dailyfx():
    base_url = 'https://www.dailyfx.com/'
    list_currency = ['eur-usd', 'gbp-usd', 'usd-jpy', 'usd-chf', 'aud-usd', 'usd-cad', 'nzd-usd']

    conn_db = connect_db("localhost", "postgres", "H0meBase")
    cur = conn_db[0]
    conn = conn_db[1]

    for currncy in list_currency:
        data = currency_date_value(base_url, currncy)
        print()
        print('DATE = ', data[0])
        print(data)
        dbtouse = 'DB_' + currncy.lower().replace('-','_')
        create_table_if_noexist(dbtouse, cur, conn)
        # datatext = (20201216145600, 'GBP-USD' , 1.354775 , 1.336765 , 1.354775 , 1.3462247916666668 , "2020-12-16 14:56:00")
        datatext = data
        put_values_to_dbtable(dbtouse, datatext, cur, conn)

    connect_db_close(cur, conn)

### LOOPING
import time
t_end = time.time() + 5*60
while time.time() < t_end:
    collectdata_from_dailyfx()
    time.sleep(5*60)

# print(time.time())
# print(t_end)
