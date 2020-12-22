import psycopg2

def list_all_tables(cursor):
    choice = {}
    sqllistalltable = """SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public';"""
    print(sqllistalltable)
    cursor.execute(sqllistalltable)
    ## print table header
    column_names = [i[0] for i in cursor.description]
    print(' ,  '.join(column_names))
    ## print table columns
    rows = cursor.fetchall()
    if len(rows) >= 1:
        i = 1
        for row in rows:
            print(str(i) + ') ' + str(row))
            choice[i] = str(row).split(',')[1].split("'")[1]
            i = i + 1
    else:
        print('[SQLTABLE EMPTY - NO DATA]')
    return choice

conn = psycopg2.connect(host="localhost", user="postgres", password="H0meBase")
curr = conn.cursor()

print()
choice = list_all_tables(curr)

print()
checkordelete = input('CHECK OR DELETE : ') + 'X'
if checkordelete[0].lower() == 'd':
    work = 'DELETE'
else:
    work = 'CHECK'
inputone = input('TABLE TO ' + work + ' = ')
if len(inputone) > 0:
    try:
        dbtable = choice[int(inputone)]
    except:
        dbtable = str(inputone)
else:
    dbtable = 'pg_catalog.pg_tables'
print('\n -- > TABLE TO USE = ' + dbtable)
print()
if work == 'CHECK':
    sqlcommand = 'SELECT * FROM ' + dbtable + ';'
    print(sqlcommand)
    print()
    curr.execute(sqlcommand)
    ## print table header
    column_names = [i[0] for i in curr.description]
    print(' ,  '.join(column_names))
    ## print table columns/values
    rows = curr.fetchall()
    if len(rows) >= 1:
        i = 1
        for row in rows:
            print(str(i) + ') ' + str(row))
            i = i+1
    else:
        print('SQLTABLE EMPTY - NO DATA')
else:
    sqlcommand = "DROP TABLE IF EXISTS " + dbtable + ";"
    print(sqlcommand)
    confirm = input('DELETE ' + dbtable + ' TABLE - [ YES / NO ] = ') + 'X'
    if confirm[0].lower() == 'y':
        print()
        curr.execute(sqlcommand)
        conn.commit()
        list_all_tables(curr)
    else:
        print('\nCHANGE MIND :-) ')

curr.close()
conn.close()