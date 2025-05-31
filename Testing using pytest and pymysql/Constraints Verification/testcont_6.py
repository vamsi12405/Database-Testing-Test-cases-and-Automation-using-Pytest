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

def is_foreign_key(db_connection,db_name,table_name,column_name):
    with db_connection.cursor() as cursor:
        cursor.execute("""
        SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE
        WHERE table_schema=%s AND table_name=%s AND column_name=%s
        AND referenced_table_name IS NOT NULL
        """,(db_name,table_name,column_name))
        results=cursor.fetchall()
        for row in results:
            return row[0]
        return None

def test_connection(db_connection):
    db_name='classicmodels'
    table_name='orders'
    column_name='customerNumber'

    assert is_table_present(db_connection, db_name, table_name)
    fk_key=is_foreign_key(db_connection, db_name, table_name, column_name)
    if fk_key:
        print(f"Table {table_name} has {''.join(fk_key)}")
    else:
        print("No foreign keys that is present")