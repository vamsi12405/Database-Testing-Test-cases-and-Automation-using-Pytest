import pytest
import pymysql
from lxml.html.builder import SELECT

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
        cursor.execute(f"SELECT `{fn_name}`(%s)", (value,))
        results=cursor.fetchall()
        return results

def is_table_present(db_connection,db_name,table_name):
    with db_connection.cursor() as cursor:
        cursor.execute(
        """
        SELECT COUNT(*) FROM information_schema.TABLES WHERE
        table_schema=%s AND table_name=%s
        """,(db_name,table_name))
        results = cursor.fetchone()
        return results[0]

def table_data(db_connection, db_name, table_name, col_name_1, col_name_2, table_value, value):
    with db_connection.cursor() as cursor:
        cursor.execute(f"USE {db_name}")
        # Table values must be quoted
        cursor.execute(
            f"""SELECT CASE
                     WHEN {col_name_1} > 50000 THEN '{table_value[0]}'
                     WHEN {col_name_1} < 50000 AND {col_name_1} > 10000 THEN '{table_value[1]}'
                     ELSE '{table_value[2]}'
                 END
                 FROM {table_name}
                 WHERE {col_name_2}=%s""", (value,)
        )
        results = cursor.fetchall()
        return results

def test_data(db_connection):
    db_name='classicmodels'
    fn_name='CustomerLevel'
    table_name='customers'


def test_fn(db_connection):
    db_name='classicmodels'
    fn_name='CustomerLevel'
    value=65000
    table_name='customers'
    table_value=['PLATINUM','GOLD','SILVER']
    col_name_1='creditLimit'
    col_name_2='customerNumber'

    assert is_fn_present(db_connection, db_name, fn_name),'function is not present'
    assert is_table_present(db_connection, db_name, table_name),'table is not present'
    function_data = fn_data(db_connection, db_name, fn_name, value)
    tab_data = table_data(db_connection,db_name,table_name,col_name_1,col_name_2,table_value,value)

