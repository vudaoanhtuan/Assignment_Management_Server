import pymysql

def getConnection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='dsa',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_Student_Priority(std_id):
    conn = getConnection()
    cursor = conn.cursor()
    sql = "SELECT priority FROM student WHERE id=%s"
    query = cursor.execute(sql, (str(std_id)))
    res = cursor.fetchone()
    return res["priority"]