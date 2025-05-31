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

# checks if user exists
def if_user_exist(db_connection, user, host):
    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM mysql.user WHERE user=%s AND host=%s",
            (user, host)
        )
        results = cursor.fetchone()
        return results[0] if results else None

# checks if role exists
def is_role_exist(db_connection, rolename):
    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM mysql.user WHERE user=%s AND Field='Y'",
            (rolename,)
        )
        results = cursor.fetchone()
        return results[0] > 0 if results else False

# checks if privilege is present for user@host
def is_privilege(db_connection, user, host, privilege):
    with db_connection.cursor() as cursor:
        cursor.execute(f"SHOW GRANTS FOR '{user}'@'{host}'")
        results = cursor.fetchall()
        privilege_upper = privilege.upper()
        for grant in results:
            if privilege_upper in grant[0].upper():
                return True
        return False

# prints list of all users
def print_users(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT user, host FROM mysql.user")
        results = cursor.fetchall()
        return results

# prints all the roles for the user at a particular host
def print_roles(db_connection, user, host):
    with db_connection.cursor() as cursor:
        cursor.execute(f"SHOW GRANTS FOR '{user}'@'{host}'")
        results = cursor.fetchall()
        return results

# prints privileges for the grantee
def print_privileges(db_connection, user, host):
    grantee = f"'{user}'@'{host}'"
    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM information_schema.USER_PRIVILEGES WHERE GRANTEE=%s",
            (grantee,)
        )
        results = cursor.fetchall()
        return results

def test_function(db_connection):
    db_name = 'classicmodels'
    user = 'mysql.sys'
    host = 'localhost'
    rolename = 'readonly'
    privilege = 'SELECT'

    assert if_user_exist(db_connection, user, host)
    data1 = print_users(db_connection)
    print("Users:", data1)

    assert is_role_exist(db_connection, rolename)
    data2 = print_roles(db_connection, user, host)
    print("Roles:", data2)

    assert is_privilege(db_connection, user, host, privilege)
    data3 = print_privileges(db_connection, user, host)
    print("Privileges:", data3)



