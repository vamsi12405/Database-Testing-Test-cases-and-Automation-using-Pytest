import pytest
import pymysql

@pytest.fixture
def db_connection():
    connection=pymysql.connect(host='localhost',port=3306,user='root',password='Universe123@#',database='classicmodels')
    yield connection
    connection.close()

def test_select_data(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT customerNumber,customerName,city FROM customers WHERE customerNumber=112")
    print('About to fetch one row')
    result = cursor.fetchone()
    print('print the result')
    print(result)
    assert result == (112,'Signal Gift Stores','Las Vegas')


