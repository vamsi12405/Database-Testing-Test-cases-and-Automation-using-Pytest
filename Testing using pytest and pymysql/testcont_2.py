import pytest
import pymysql

@pytest.fixture
def db_connection():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Universe234@#',
        database='classicmodels'
    )
    yield connection
    connection.close()

def is_view_present(db_connection,db_name,view_name):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT TABLE_NAME FROM 
            information_schema.VIEWS WHERE 
            table_schema=%s AND table_name = %s
            """,(db_name,view_name))
        results=cursor.fetchone()
        return results[0] if results else None

def print_view_data(db_connection,db_name,view_name):
    with db_connection.cursor() as cursor:
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"SELECT * FROM {view_name}")
        results=cursor.fetchall()
        return results

def test_connection(db_connection):
    db_name='classicmodels'
    view_name='view_2'

    assert is_view_present(db_connection,db_name,view_name)
    data = print_view_data(db_connection, db_name, view_name)
    if data:
        print(data)
    else:
        print("view exists but empty")


