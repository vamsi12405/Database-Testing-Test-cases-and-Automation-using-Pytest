import pytest
import pymysql

@pytest.fixture
def db_connection():
    connection=pymysql.connect(host='localhost',port=3306,user='root',password='Universe123@#',database='classicmodels')
    yield connection
    connection.close()

def is_proc_present(db_connection,db_name,proc_name):
    with db_connection.cursor() as cursor:
        cursor.execute("""
        SELECT ROUTINE_NAME FROM information_schema.ROUTINES
        WHERE ROUTINE_TYPE='PROCEDURE' AND ROUTINE_SCHEMA=%s AND
        ROUTINE_NAME=%s
        """,(db_name,proc_name))
        results=cursor.fetchone()
        return results[0] if results else None

def get_data_with_output_variable(db_connection, db_name, proc_name, value):
    with db_connection.cursor() as cursor:
        cursor.execute(f"USE `{db_name}`")
        cursor.execute("SET @shipped = ''")
        # Call the procedure, passing @shipped as OUT variable
        cursor.callproc(proc_name, (value, '@shipped'))
        cursor.execute("SELECT @shipped")
        result = cursor.fetchone()  # Not fetchall
        return result[0] if result else None

def test_function(db_connection):
    db_name='classicmodels'
    proc_name='get_customer_shipping'
    value=112

    assert is_proc_present(db_connection,db_name, proc_name),'procedure is not present'
    data = get_data_with_output_variable(db_connection, db_name, proc_name, value)
    print(data)  # Should print '2 day shipping'