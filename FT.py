import os.path
from os import path
import os
import distutils.spawn
import subprocess
from termcolor import colored
  
def write_in_file(pathname, content):
    f = open(pathname, "a")
    f.write(content)
    f.close()

def do_c(isAdvanced):
    print("\n=== Creating test ===")
    if path.exists("tests") == False:
        os.system("mkdir tests/")
    binaryName = raw_input("Enter the binary name of the project for this test\n>>> ")
    if path.exists("tests/" + binaryName) == False:
        os.system("mkdir tests/" + binaryName)
    newFileName = raw_input("Enter a filename for your test\n>>> ")
    while path.isfile("tests/" + binaryName + "/" + newFileName):
        print("/!\ Error: " + newFileName + " already exists! (tests/" + binaryName + "/" + newFileName + ") /!\ ")
        newFileName = raw_input("Enter a filename for your test\n>>> ")
    pathFile = "tests/" + binaryName + "/" + newFileName
    os.system("touch " + pathFile)
    parameters = raw_input("Enter parameter(s) separated by space (ex: exParam1 exParam2)\n>>> ")
    write_in_file(pathFile, parameters + '\n')
    output = raw_input("Enter output expected\n>>> ")
    write_in_file(pathFile, output + '\n')
    if isAdvanced == True:
        content = raw_input("Enter content for game's loop (EOF to end)\n>>> ")
        while content != "EOF":
            write_in_file(pathFile + ".a", content + '\n')
            content = raw_input(">>> ")
        write_in_file(pathFile, pathFile + ".a")
    print("=== Test created (" + pathFile + ") ===")
    start_ask()

def do_s():
    print("\n=== Showing test ===")
    if path.exists("tests") == False:
        print("No test.")
        start_ask()
        return
    binaryName = raw_input("Enter the binary name of the project\n>>> ")
    if path.exists("tests/" + binaryName) == False:
        print("No test.")
        start_ask()
        return
    path_dir = "tests/" + binaryName + "/"
    in_dir_list = os.listdir(path_dir)
    print("")
    for i in in_dir_list:
        f = open(path_dir + i, "r")
        print("  -- " + i + " --")
        first_param = f.readline()
        second_param = f.readline()
        print("Parameter(s): " + (first_param if first_param else "\n") + "Output: " + (second_param if second_param else " \n"))
    print("=== End showing test ===")
    start_ask()

def do_r():
    binaryName = raw_input("Enter the binary name of the project\n>>> ")
    while distutils.spawn.find_executable(binaryName) == None:
        print("Error: " + binaryName + " not found!")
        binaryName = raw_input("Enter the binary name of the project\n>>> ")
    path_dir = "tests/" + binaryName + "/"
    if path.exists(path_dir) == False:
        print("No test.")
        start_ask()
        return
    print("")
    in_dir_list = os.listdir(path_dir)
    for i in in_dir_list:
        if ".a" in i:
            continue
        f = open(path_dir + i, "r")
        first_param = f.readline()
        second_param = f.readline().rstrip("\n")
        third_param = f.readline()
        if third_param == "":
            print("./" + binaryName + " " + first_param)
            output = subprocess.check_output("./" + binaryName + " " + first_param, shell=True).rstrip("\n")
        else:
            print("./" + binaryName + " " + first_param.rstrip("\n") + " < " + third_param)
            output = subprocess.check_output("./" + binaryName + " " + first_param.rstrip("\n") + " < " + third_param, shell=True).rstrip("\n")
        if output == second_param:
            print colored(i, 'cyan'), colored('...', 'white'), colored('[OK]', 'green')
        else:
            print colored(i, 'cyan'), colored('...', 'white'), colored('[KO]', 'red'), colored("- Expected: \"" + second_param + "\" but got: \"" + output + "\"", 'white')
    print("")
    start_ask()

def start_ask():
    choice = raw_input("(R)un tests, (C)reate tests, (S)how existing tests, (Q)uit\n>>> ")
    while choice != 'R' and choice != 'r' and choice != 'C' and choice != 'c' and choice != 'S' and choice != 's' and choice != 'q' and choice != 'Q':
        print(choice + " is not defined!")
        choice = raw_input("(R)un tests, (C)reate tests, (S)how existing tests, (Q)uit\n>>> ")
    if choice == 'R' or choice == 'r':
        do_r()
    elif choice == 'C' or choice == 'c':
        do_c(False)
    elif choice == 'S' or choice == 's':
        do_s()
    elif choice == 'Q' or choice == 'q':
        print("Exiting program...")
        return

def main():
    start_ask()

main()