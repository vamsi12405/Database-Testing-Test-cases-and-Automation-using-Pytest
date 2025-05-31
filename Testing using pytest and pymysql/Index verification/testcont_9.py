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

def if_index_present(db_connection,db_name,table_name,index_name):
    with db_connection.cursor() as cursor:
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"SHOW INDEX FROM {table_name} WHERE key_name=%s",(index_name,))
        results=cursor.fetchall()
        return results

def test_connection(db_connection):
    db_name='classicmodels'
    table_name='orders'
    index_name='index_1'

    assert is_table_present(db_connection, db_name, table_name),"Table not present"

    assert if_index_present(db_connection, db_name, table_name, index_name),"no index found"
    print("index is present")

