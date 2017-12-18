class Job:
    def __init__(self, ass_id, student_id, timestamp, priority, submit_id):
        self.priority = priority
        self.timestamp = timestamp
        self.student_id = student_id
        self.ass_id = ass_id
        self.submit_id = submit_id

    def isLessThan(self, job):
        job.__class__ = Job
        if int(self.priority) < int(job.priority):
            return True
        if int(self.priority) == int(job.priority) and str(self.timestamp) < str(job.timestamp):
            return True
        return False






class Heap:
    def __init__(self):
        self.length = 0
        self.maxsize = 1000000
        self.heap = [Job] * self.maxsize
        self.last = -1

    def upHeap(self, con):
        cha = (con - 1) // 2
        if con > 0:
            conH = self.heap[con]
            chaH = self.heap[cha]
            if chaH.isLessThan(conH):
                self.heap[con], self.heap[cha] = chaH, conH
                self.upHeap(cha)

    def downHeap(self, cha):
        con = cha * 2 + 1
        conH = self.heap[con]
        conH1 = self.heap[con+1]
        chaH = self.heap[cha]
        if con <= self.last and conH.isLessThan(conH1):
            conH = conH1
            con = con + 1

        if con <= self.last and chaH.isLessThan(conH):
            self.heap[con], self.heap[cha] = chaH, conH
            self.downHeap(con)

    def push(self, job):
        self.length = self.length + 1
        self.last = self.last + 1
        self.heap[self.last] = job
        self.upHeap(self.last)

    def pop(self):
        self.length = self.length - 1
        t = self.heap[0]
        self.heap[0] = self.heap[self.last]
        self.last = self.last - 1
        self.downHeap(0)
        return t

    def find(self, submit_id):
        for i in range(self.length):
            if self.heap[i].submit_id == submit_id:
                return True
        return False
