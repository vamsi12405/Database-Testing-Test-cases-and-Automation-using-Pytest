import pytest
import pymysql

@pytest.fixture
def db_connection():
    connection=pymysql.connect(host='localhost',port=3306,user='root',password='Universe123@#',database='classicmodels')
    yield connection
    connection.close()

def is_proc_present(db_connection,db_name,proc_name):
    cursor=db_connection.cursor()
    cursor.execute("""
    SELECT ROUTINE_NAME FROM information_schema.ROUTINES
    WHERE ROUTINE_TYPE='PROCEDURE' AND ROUTINE_SCHEMA=%s AND
    ROUTINE_NAME=%s
    """,(db_name,proc_name))
    results=cursor.fetchone()
    return results[0] if results else None

def get_proc_data_with_condition(db_connection,db_name,proc_name,value):
    cursor=db_connection.cursor()
    cursor.execute(f"USE {db_name}")
    cursor.callproc(proc_name,(value,))
    results=cursor.fetchall()
    return results

def test_function(db_connection):
    db_name='classicmodels'
    proc_name='SelectAllCustomersByCity'
    value='San Francisco'

    assert is_proc_present(db_connection, db_name, proc_name), f"Procedure {proc_name} not present"
    data = get_proc_data_with_condition(db_connection, db_name, proc_name, value)
    assert isinstance(data,(list,tuple)),"Returned data is not list or tuple"
    print(data)
