import socket
import threading
import time
from runner import runtest
from database import connect
from database import heap_struct

class Score(threading.Thread):
    def __init__(self, list_student, list_lock):
        threading.Thread.__init__(self)

        self._list = list_student
        self._list.__class__ = heap_struct.Heap
        self._list_lock = list_lock

    def run(self):

        while True:
            self._list_lock.acquire()
            if (self._list.length > 0):
                job = self._list.pop()
                # process here
                print("Dang xu li. Student id = " + str(job.student_id))

                conn = connect.getConnection()
                cursor = conn.cursor()

                sql = "UPDATE submit SET status = %s WHERE assignment_id = %s AND student_id = %s AND time = %s"
                query = cursor.execute(sql, ("g", job.ass_id, job.student_id, job.timestamp))
                conn.commit()

                exitcode, score, log = runtest.run_test_on_submit_dir(job.ass_id, job.student_id, job.timestamp)
                eval_score = 0
                if not exitcode:
                    eval_score = str(10.0 * eval(score))

                # update database
                sql = "UPDATE submit SET status = %s, score = %s, log = %s, eval_score = %s WHERE assignment_id = %s AND student_id = %s AND time = %s"
                query = cursor.execute(sql, (exitcode, score, log, eval_score, job.ass_id, job.student_id, job.timestamp))
                conn.commit()
                conn.close()

                print("OK: ")
                time.sleep(10)
            self._list_lock.release()


class Scan(threading.Thread):
    def __init__(self, list_student, list_lock):
        threading.Thread.__init__(self)
        self._list = list_student  # list of number from 2 to N
        self._list_lock = list_lock  # Lock for list_num

        # self._conn =  connect.getConnection()
        # self._cursor = self._conn.cursor()
        # use socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 10000))
        self.server.listen(1)

        # use database



    def run(self):
        # request to access shared resource
        # if there are many threads acquiring Lock, only one thread get the Lock
        # and other threads will get blocked
        while True:
            conn, client = self.server.accept()
            try:
                print ("Connection from", client)
                data = conn.recv(1024)
                print ("Receive from client:", data)
                conn.sendall(data)
                s = data.decode('utf-8')
                info = str(s).split("|")

                # sql = "SELECT * FROM submit WHERE status=%s"
                # query = self._cursor.execute(sql, ("w"))
                # for i in range(query):
                #     res = self._cursor.fetchone()
                #     id = res["id"]
                #     std_id = res["student_id"]


                job = heap_struct.Job(info[0], info[1], info[2], info[3])
                print(s)
                self._list_lock.acquire()
                self._list.push(job)
                self._list_lock.release()
            finally:
                conn.close()


