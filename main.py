# config number of thread
num_threads = 2


# server

from server.server import *
print("Server is running")

list_student = heap_struct.Heap()
list_lock = threading.Lock()

print("Creating thread for scanning file")
thread_scan = Scan(list_student, list_lock)
thread_scan.start()
print("Creating %d thread for grading" % num_threads)
threads = []
for i in range(num_threads):
    thread_score = Score(list_student, list_lock)
    threads.append(thread_score)
    thread_score.start()
