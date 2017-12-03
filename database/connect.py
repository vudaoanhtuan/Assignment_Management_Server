import pymysql

def getConnection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='dsa',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection