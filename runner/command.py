import subprocess, threading
import os, signal


class Command(object):
    def __init__(self, cmd, infile="input", outfile="output"):
        self.cmd = cmd
        self.process = None
        self.input_file = open(infile, "r")
        self.output_file = open(outfile, "w")

    def run(self, timeout):
        def target():
            # print('Thread started')

            self.process = subprocess.Popen(self.cmd, stdin=self.input_file, stdout=self.output_file, shell=False)

            self.process.communicate()
            # print('Thread finished')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(int(timeout))
        if thread.is_alive():
            # print('Terminating process')
            # print(self.process.pid)

            self.process.kill()
            if not self.input_file.closed:
                self.input_file.close()
            if not self.output_file.closed:
                self.output_file.close()
            thread.join()
        return self.process.returncode