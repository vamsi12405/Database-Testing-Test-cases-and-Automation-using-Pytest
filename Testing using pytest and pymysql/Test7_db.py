import pytest
import pymysql

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

def test_function(db_connection):
    db_name='classicmodels'
    fn_name='CustomerLevel'

    assert is_fn_present(db_connection, db_name, fn_name),'Function is not present'
