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

def get_function_body(db_connection,db_name,fn_name):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ROUTINE_DEFINITION FROM
            information_schema.ROUTINES WHERE
            ROUTINE_TYPE='FUNCTION' AND ROUTINE_SCHEMA=%s 
            AND ROUTINE_NAME=%s""",(db_name,fn_name)
        )
        results=cursor.fetchone()
        return results[0] if results else None

def is_Select_only(function_body):
    if function_body is None:
        return False
    else:
        body_lower=function_body.lower()
        forbidden=['update','delete','insert']
        for cmd in forbidden:
            if cmd in body_lower:
                return False
        return True

def test_function(db_connection):
    db_name='classicmodels'
    fn_name='CustomerLevel'


    function_body = get_function_body(db_connection, db_name, fn_name)
    if function_body is None:
        print('Function not present')
    else:
        if is_Select_only(function_body) is None:
            print('delete or update or insert commands are present')
        else:
            print('Only select statements are present')
