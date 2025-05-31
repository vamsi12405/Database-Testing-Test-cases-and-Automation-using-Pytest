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

def is_primary_key(db_connection,db_name,table_name):
    with db_connection.cursor() as cursor:
        cursor.execute("""
        SELECT COLUMN_NAME FROM
        information_schema.KEY_COLUMN_USAGE WHERE
        CONSTRAINT_NAME='PRIMARY' AND table_schema=%s AND
        table_name=%s
        """,(db_name,table_name))
        results=cursor.fetchall()
        for row in results:
            return row[0]
        return None

def test_connection(db_connection):
    db_name='classicmodels'
    table_name='customers'

    assert is_table_present(db_connection, db_name, table_name)
    pk_key=is_primary_key(db_connection, db_name, table_name)
    if pk_key:
        print(f"primary key is {pk_key}")
    else:
        print("primary key not present")