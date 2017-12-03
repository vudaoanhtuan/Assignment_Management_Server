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
                exitcode, score, log = runtest.run_test_on_submit_dir(job.ass_id, job.student_id, job.timestamp)

                # update database
                conn = connect.getConnection()
                cursor = conn.cursor()
                sql = "UPDATE submit SET status = %s, score = %s, log = %s WHERE assignment_id = %s AND student_id = %s AND time = %s"
                query = cursor.execute(sql, (exitcode, score, log, job.ass_id, job.student_id, job.timestamp))
                conn.commit()
                conn.close()

                print("OK: ")
            self._list_lock.release()


class Scan(threading.Thread):
    def __init__(self, list_student, list_lock):
        threading.Thread.__init__(self)
        self._list = list_student  # list of number from 2 to N
        self._list_lock = list_lock  # Lock for list_num
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 10000))
        self.server.listen(1)

    def run(self):
        # request to access shared resource
        # if there are many threads acquiring Lock, only one thread get the Lock
        # and other threads will get blocked
        while True:
            conn, client = self.server.accept()
            try:
                # print ("Connection from", client)
                data = conn.recv(1024)
                # print ("Receive from client:", data)
                conn.sendall(data)
                s = data.decode('utf-8')
                info = str(s).split("|")
                job = heap_struct.Job(info[0], info[1], info[2], info[3])
                print(s)
                self._list_lock.acquire()
                self._list.push(job)
                self._list_lock.release()
            finally:
                conn.close()


list_student = heap_struct.Heap()
list_lock = threading.Lock()

thread_score = Score(list_student, list_lock)
thread_score.start()

thread_scan = Scan(list_student, list_lock)
thread_scan.start()
