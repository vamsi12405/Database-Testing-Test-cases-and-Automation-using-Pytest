import pytest
import pymysql

@pytest.fixture
def db_connection():
    connection=pymysql.connect(host='localhost',port=3306,user='root',password='Universe123@#',database='classicmodels')
    yield connection
    connection.close()

def is_table_present(db_connection,db_name,table_name):
    cursor = db_connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM information_schema.TABLES WHERE 
    table_schema=%s AND table_name=%s
    """,
        (db_name,table_name))
    results=cursor.fetchone()
    return results[0] > 0

def get_table_data(db_connection,db_name,table_name,col_name,value):
    cursor = db_connection.cursor()
    cursor.execute(f"SELECT * FROM {db_name}.{table_name} WHERE {col_name}=%s",(value,))
    results=cursor.fetchall()
    return results

def test_query_with_condition(db_connection):
    db_name='classicmodels'
    table_name='customers'
    col_name='city'
    value='San Francisco'

    if not is_table_present(db_connection,db_name,table_name):
        print('table not found')
    else:
        data=get_table_data(db_connection, db_name, table_name, col_name, value)
        print(data)

