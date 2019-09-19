import pymysql


def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='12345678',
        database='python_mysql',
        charset='utf8'
    )


def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def insert_or_update_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    sql = "insert user (name, sex, age, email) values('daming', 'man', 30, 'daming@qq.com')"
    insert_or_update_data(sql)

    sql = "select * from user"
    datas = query_data(sql)
    import pprint

    pprint.pprint(datas)
