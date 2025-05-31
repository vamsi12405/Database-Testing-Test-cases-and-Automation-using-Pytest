import pytest
import pymysql
import Test7_db as T7

@pytest.fixture
def db_connection():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Universe123@#',
        database='classicmodels'
    )
    yield connection
    connection.close()

def is_fn_present(db_connection,db_name,fn_name):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ROUTINE_NAME FROM
            information_schema.ROUTINES WHERE
            ROUTINE_TYPE='FUNCTION' AND ROUTINE_SCHEMA=%s
            AND ROUTINE_NAME=%s
            """,(db_name,fn_name))
        results=cursor.fetchone()
        return results[0] if results else None

def fn_data(db_connection,db_name,fn_name,value):
    with db_connection.cursor() as cursor:
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"SELECT {fn_name}(%s)",(value,))
        results=cursor.fetchall()
        return results

def test_fn(db_connection):
    db_name='classicmodels'
    fn_name='CustomerLevel'
    value=65000

    assert T7.is_fn_present(db_connection, db_name, fn_name),'Function is not present'
    data = fn_data(db_connection, db_name, fn_name, value)
    print(data)




