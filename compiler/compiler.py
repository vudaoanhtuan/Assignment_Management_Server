import os
import xml.etree.ElementTree as ET


def compile(compiler_name, source_file_list, exe_file, log_file):
    cm = compiler_name + " "
    for filename in list(source_file_list):
        cm = cm + filename + " "
    cm = cm + " -o " + exe_file + " > " + log_file + " 2>&1"
    res = os.system(cm)
    return res


def getListFile(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    header = []
    source = []
    for h in root.findall("./header/*"):
        header.append(h.text)

    for s in root.findall("./source/*"):
        source.append(s.text)

    return header, source

