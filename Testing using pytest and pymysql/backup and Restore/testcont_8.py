import pytest
import pymysql
import subprocess
import datetime

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

def is_backup(backup_file):
    cmd = [
        "mysqldump"
        "",
        "-hlocalhost"
        'uroot',
        "-pUniverse234@#",
        "classicmodels"
    ]
    with open(backup_file,"w") as f:
        result = subprocess.run(cmd,stdout=f,stderr=subprocess.PIPE)
    return result.returncode == 0

def is_restore(backup_file):
    cmd = [
        "mysqldump",
        "-hlocalhost",
        "uroot",
        "-pUniverse234@#",
        "classicmodels"
    ]
    with open(backup_file, "r") as f:
        result = subprocess.run(cmd, stdin=f, stderr=subprocess.PIPE)
    return result.returncode ==0

def is_table_exists(db_connection,db_name,table_name):
     with db_connection.cursor() as cursor:
         cursor.execute(
             """
             SELECT COUNT(*) FROM
             information_schema.tables WHERE table_schema=%s AND table_name=%s
             """,(db_name,table_name)
         )
         results=cursor.fetchone()
         return results[0]

def test_connection(db_connection):
    db_name='classicmodels'
    table_name='customers'

    backup_file=f"./classicmodels_backup_{datetime.datetime.now():%Y%m%d_%H%M%S}.sql"

    assert is_backup(backup_file),"backup failed"

    with db_connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    assert not is_table_exists(db_connection, db_name, table_name),"table was not dropped"

    assert is_restore(backup_file),"restore failed"

    assert is_table_exists(db_connection, db_name, table_name,"table restoration failed")

    print("backup and restore passed")
