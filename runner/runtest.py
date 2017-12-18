from config import config
from compiler import compiler
from checker import checkfile
from runner import command
import datetime
import os
import shutil


def runtest(student_id):
    con = config.config("0")

    student_dir = con.student_dir
    testcase_dir = con.testcase_dir
    compiler_name = con.compiler_name
    limit_time = con.limit_time
    # diff = con.diff

    current_student_dir = student_dir + "/" + student_id
    submit_dir = current_student_dir + "/submit"
    time_dir = current_student_dir + "/" + datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    if not os.path.isdir(time_dir):
        os.makedirs(time_dir)

    files = os.listdir(submit_dir)

    for f in files:
        shutil.move(submit_dir + "/" + f, time_dir)

    xmlpath = time_dir + "/pro.xml"

    h, s = compiler.getListFile(xmlpath)
    source = h + s
    for i in range(len(source)):
        source[i] = time_dir + "/" + source[i]

    exe_file = time_dir + "/main"

    log_file = time_dir + "/pro.log"

    compile_error = compiler.compile(compiler_name, source, exe_file, log_file)

    if not compile_error:  # khong co loi
        # test testcase
        list_testcase = os.listdir(testcase_dir)

        student_output_dir = time_dir + "/output"
        os.mkdir(student_output_dir)

        list_score = []
        score = 0

        for current_testcase in list_testcase:
            input_file = testcase_dir + "/" + current_testcase + "/input"
            output_file = testcase_dir + "/" + current_testcase + "/output"

            student_output_file = student_output_dir + "/" + current_testcase
            cml = exe_file + " < " + input_file + " > " + student_output_file
            command_line = command.Command(cml, input_file, student_output_file)
            run_error = command_line.run(timeout=limit_time)

            if not run_error:
                if checkfile.isSameFile(output_file, student_output_file):
                    list_score.append((current_testcase, 1))
                    score = score + 1
                else:
                    list_score.append((current_testcase, 0))
            else:
                list_score.append((current_testcase, 0))

        score_file = open(time_dir + "/score.log", "w")
        score_file.write(str(score) + "/" + str(len(list_score)) + "\n")

        for i in list_score:
            score_file.write(str(i[0]) + " " + str(i[1]) + "\n")
        score_file.close()
        return 0
    # co loi, return 1
    else:
        return 1


def run_test_on_submit_dir(ass_id, student_id, submit_dir_name):

    con = config.config(str(ass_id))

    modecheck = con.diff

    time_dir = con.student_dir + "/" + str(student_id) + "/" + str(submit_dir_name)

    xmlpath = time_dir + "/pro.xml"

    h, s = compiler.getListFile(xmlpath)
    source = h + s
    for i in range(len(source)):
        source[i] = time_dir + "/" + source[i]

    exe_file = time_dir + "/main"

    log_file = time_dir + "/pro.log"

    compile_error = compiler.compile(con.compiler_name, source, exe_file, log_file)

    if not compile_error:  # khong co loi
        # test testcase
        list_testcase = os.listdir(con.testcase_dir)

        student_output_dir = time_dir + "/output"
        os.mkdir(student_output_dir)

        list_score = []
        score = 0

        for current_testcase in list_testcase:
            input_file = con.testcase_dir + "/" + current_testcase + "/input"
            output_file = con.testcase_dir + "/" + current_testcase + "/output"

            student_output_file = student_output_dir + "/" + current_testcase
            student_output_log = student_output_file + ".log"

            cml = exe_file + " < " + input_file + " > " + student_output_file
            command_line = command.Command(cml, input_file, student_output_file)
            run_error = command_line.run(timeout=con.limit_time)

            chard = (modecheck[0] == "1")
            ccase = (modecheck[1] == "1")
            cfloat = (modecheck[2] == "1")
            precision = int(modecheck[4:])

            if run_error:
                error_log = open(student_output_log, "w")
                error_log.write("Time Limit Error")
                error_log.close()
                list_score.append((current_testcase, 0))

            elif checkfile.isSameFile(output_file, student_output_file, student_output_log, chard, ccase, cfloat, precision):
                list_score.append((current_testcase, 1))
                score = score + 1
            else:
                list_score.append((current_testcase, 0))



        score_file = open(time_dir + "/score.log", "w")
        percen = str(score) + "/" + str(len(list_testcase))
        score_file.write(percen + "\n")
        for i in list_score:
            score_file.write(str(i[0]) + " " + str(i[1]) + "\n")
        score_file.close()
        return 0, percen, ""
    # co loi, return 1
    else:
        file = open(log_file, "r")
        log = file.read()
        file.close()
        return 1, 0, log
