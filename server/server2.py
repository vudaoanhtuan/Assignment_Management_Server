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

            if (self._list.length > 0):
                self._list_lock.acquire()
                job = self._list.pop()
                self._list_lock.release()
                # process here
                print("Grading. submit_id = ", job.submit_id)

                conn = connect.getConnection()
                cursor = conn.cursor()

                sql = "UPDATE submit SET status = %s WHERE id = %s"
                query = cursor.execute(sql, ("g", job.submit_id))
                conn.commit()

                exitcode, score, log = runtest.run_test_on_submit_dir(job.ass_id, job.student_id, job.timestamp)
                eval_score = 0
                if not exitcode:
                    eval_score = str(10.0 * eval(score))

                # update database
                sql = "UPDATE submit SET status = %s, score = %s, log = %s, eval_score = %s WHERE id = %s"
                query = cursor.execute(sql, (exitcode, score, log, eval_score, job.submit_id))
                conn.commit()
                conn.close()

                print("Finished. submit_id = ", job.submit_id)




class Scan(threading.Thread):
    last_id = 0
    def __init__(self, list_student, list_lock):
        threading.Thread.__init__(self)
        self._list = list_student  # list of number from 2 to N
        self._list_lock = list_lock  # Lock for list_num


    def run(self):
        # request to access shared resource
        # if there are many threads acquiring Lock, only one thread get the Lock
        # and other threads will get blocked
        while True:
            time.sleep(3)
            conn = connect.getConnection()
            cursor = conn.cursor()
            # print("Scanning ", Scan.last_id)
            sql = "SELECT * FROM submit WHERE status=%s AND id>%s"
            query = cursor.execute(sql, ("w", Scan.last_id))
            # print(query)
            for i in range(query):
                res = cursor.fetchone()
                submit_id = res["id"]
                std_id = res["student_id"]
                ass_id = res["assignment_id"]
                time_stamp = res["time"]
                priority = connect.get_Student_Priority(std_id)
                job = heap_struct.Job(ass_id, std_id, time_stamp, priority, submit_id)
                self._list_lock.acquire()
                self._list.push(job)
                self._list_lock.release()
                Scan.last_id = max(int(Scan.last_id), int(submit_id))




