import pymysql
from database import connect

class config:
    def __init__(self, ass_id):
        # file = open(config_file, "r")
        # self.testcase_dir = file.readline().strip()
        # self.student_dir = file.readline().strip()
        # self.compiler_name = file.readline().strip()
        # self.limit_time = file.readline().strip()
        # file.close()
        connection = connect.getConnection()
        cursor = connection.cursor()
        sql = "SELECT * FROM assignment WHERE id = %s"
        cursor.execute(sql, (str(ass_id), ))
        info = cursor.fetchone()
        self.testcase_dir = str(info["testcase_dir"]).strip()
        self.student_dir = str(info["student_dir"]).strip()
        self.compiler_name = str(info["compiler"]).strip()
        self.limit_time = str(info["limit_time"]).strip()
        self.diff = str(info["diff"]).strip()
        connection.close()

    def getConfigFromDB(self, ass_id):
        connection = connect.getConnection()
        cursor = connection.cursor()
        sql = "SELECT * FROM assignment WHERE id = %s"
        cursor.execute(sql, (str(ass_id), ))
        info = cursor.fetchone()
        self.testcase_dir = str(info["testcase_dir"]).strip()
        self.student_dir = str(info["student_dir"]).strip()
        self.compiler_name = str(info["compiler"]).strip()
        self.limit_time = str(info["limit_time"]).strip()

