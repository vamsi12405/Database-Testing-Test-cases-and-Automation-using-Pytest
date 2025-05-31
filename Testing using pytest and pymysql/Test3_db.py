import pytest
import pymysql

@pytest.fixture
def db_connection():
    import pymysql
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Universe123@#',
        database='classicmodels'
    )
    yield connection
    connection.close()

def if_proc_exists(db_connection, db_name, proc_name):
    with db_connection.cursor() as cursor:
        cursor.execute("""
            SELECT ROUTINE_NAME FROM information_schema.ROUTINES
            WHERE ROUTINE_TYPE='PROCEDURE' AND ROUTINE_SCHEMA=%s AND ROUTINE_NAME=%s
        """, (db_name, proc_name))
        result = cursor.fetchone()
        return result[0] if result else None

def if_table_exists(db_connection,table_name,db_name):
    cursor=db_connection.cursor()
    sql = """
    SELECT COUNT(*) FROM information_schema.tables
    WHERE table_name=%s AND table_schema=%s
    """
    cursor.execute(sql,(table_name,db_name))
    results = cursor.fetchone()
    return results[0] > 0

def get_proc_data(db_connection,proc_name):
    cursor = db_connection.cursor()
    cursor.callproc(proc_name)
    results  =cursor.fetchall()
    return results

def get_table_data(db_connection,table_name):
    cursor=db_connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    results = cursor.fetchall()
    return results

if __name__ == "__main__":
    proc_name = 'SelectAllCustomers'
    db_name = 'classicmodels'
    table_name = 'customers'


    if not if_proc_exists(db_connection,proc_name,db_name):
        print(f"procedure {proc_name} does not exist")
    else:
        if not if_table_exists(db_connection,db_name,table_name):
            print(f"table {table_name} does not exist")
        else:
            if get_proc_data(db_connection, proc_name) == get_table_data(db_connection,table_name):
                print('The data displayed is equal')
            else:
                print('The data displayed is not equal')



