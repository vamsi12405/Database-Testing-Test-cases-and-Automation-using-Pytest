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

def is_table_present(db_connection,db_name,table_name):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*) FROM 
            information_schema.TABLES WHERE table_schema=%s AND
            table_name=%s
            """,(db_name,table_name)
        )
        results=cursor.fetchone()
        return results[0]>0

def is_default(db_connection,db_name,table_name,col_name):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COLUMN_DEFAULT FROM
            information_schema.columns WHERE 
            table_schema=%s AND table_name=%s AND column_name=%s
            """,(db_name,table_name,col_name)
        )
        results=cursor.fetchall()
        for row in results:
            return row[0]
        return None

def test_connection(db_connection):
    db_name = 'classicmodels'
    table_name = 'customers'
    col_name='customerLevel'

    assert is_table_present(db_connection, db_name, table_name)
    default = is_default(db_connection,db_name,table_name,col_name)
    if default:
        print(f"Table {table_name} has {','.join(default)}")
    else:
        print('No column with default constrainat present')
