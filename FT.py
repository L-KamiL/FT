import os.path
from os import path
import os
import distutils.spawn
import subprocess
from termcolor import colored
import shlex

  
def write_in_file(pathname, content):
    f = open(pathname, "a")
    f.write(content)
    f.close()

def do_c(isAdvanced):
    print("\n=== Creating test ===")
    if path.exists("tests") == False:
        os.system("mkdir tests/")
    binaryName = input("Enter the binary name of the project for this test\n>>> ")
    if path.exists("tests/" + binaryName) == False:
        os.system("mkdir tests/" + binaryName)
    if path.exists("tests/" + binaryName + "/advanced") == False:
        os.system("mkdir tests/" + binaryName + "/advanced")
    newFileName = input("Enter a filename for your test\n>>> ")
    while path.isfile("tests/" + binaryName + "/" + newFileName):
        print("/!\ Error: " + newFileName + " already exists! (tests/" + binaryName + "/" + newFileName + ") /!\ ")
        newFileName = input("Enter a filename for your test\n>>> ")
    pathFile = "tests/" + binaryName + "/" + newFileName
    os.system("touch " + pathFile)
    parameters = input("Enter parameter(s) separated by space (ex: exParam1 exParam2)\n>>> ")
    write_in_file(pathFile, parameters + '\n')
    output = input("Enter output expected\n>>> ")
    write_in_file(pathFile, output + '\n')
    if isAdvanced == True:
        content = input("Enter content for game's loop (EOF to end)\n>>> ")
        while content != "EOF":
            write_in_file("tests/" + binaryName + "/advanced/" + newFileName + ".a", content + '\n')
            content = input(">>> ")
        write_in_file(pathFile, "tests/" + binaryName + "/advanced/" + newFileName + ".a")
    print("=== Test created (" + pathFile + ") ===")
    start_ask()

def do_s():
    print("\n=== Showing test ===")
    if path.exists("tests") == False:
        print("No test.")
        start_ask()
        return
    binaryName = input("Enter the binary name of the project\n>>> ")
    if path.exists("tests/" + binaryName) == False:
        print("No test.")
        start_ask()
        return
    path_dir = "tests/" + binaryName + "/"
    in_dir_list = os.listdir(path_dir)
    print("")
    for i in in_dir_list:
        if path.isfile(path_dir + i) == False:
            continue
        f = open(path_dir + i, "r")
        print("  -- " + i + " --")
        first_param = f.readline()
        second_param = f.readline()
        print("Parameter(s): " + (first_param if first_param else "\n") + "Output: " + (second_param if second_param else " \n"))
    print("=== End showing test ===")
    start_ask()

def do_r():
    binaryName = input("Enter the binary name of the project\n>>> ")
    while distutils.spawn.find_executable(binaryName) == None:
        print("Error: " + binaryName + " not found!")
        binaryName = input("Enter the binary name of the project\n>>> ")
    path_dir = "tests/" + binaryName + "/"
    if path.exists(path_dir) == False:
        print("No test.")
        start_ask()
        return
    print("")
    in_dir_list = os.listdir(path_dir)
    for i in in_dir_list:
        hasToPrint = True
        if path.isfile(path_dir + i) == False:
            continue
        f = open(path_dir + i, "r")
        first_param = f.readline()
        second_param = f.readline().rstrip("\n")
        third_param = f.readline()
        output = ""
        if third_param == "":
            try:
                output = subprocess.check_output(shlex.split("./" + binaryName + " " + first_param.rstrip('\n')), timeout=6).decode('utf-8')
            except subprocess.CalledProcessError as e:
                hasToPrint = True
            except subprocess.TimeoutExpired:
                print(colored(i, 'cyan'), colored('...', 'white'), colored('[KO]', 'red'), colored(" - Timeout after 6 seconds", 'white'))
                hasToPrint = False
        else:
            try:
                output = subprocess.check_output("./" + binaryName + " " + first_param.rstrip("\n") + " < " + third_param, shell=True, timeout=6).decode('utf-8')
            except subprocess.TimeoutExpired:
                print(colored(i, 'cyan'), colored('...', 'white'), colored('[KO]', 'red'), colored(" - Timeout after 6 seconds", 'white'))
                hasToPrint = False
            except subprocess.CalledProcessError as e:
                hasToPrint = True
        if hasToPrint == True:
            if output.rstrip("\n") == second_param:
                print(colored(i, 'cyan'), colored('...', 'white'), colored('[OK]', 'green'))
            else:
                print(colored(i, 'cyan'), colored('...', 'white'), colored('[KO]', 'red'), colored("- Expected: \"" + second_param + "\" but got: \"" + output.rstrip("\n") + "\"", 'white'))
    print("")
    start_ask()

def start_ask():
    choice = input("(R)un tests, (C)reate tests, (S)how existing tests, (Q)uit\n>>> ")
    while choice != 'R' and choice != 'r' and choice != 'C' and choice != 'c' and choice != 'S' and choice != 's' and choice != 'q' and choice != 'Q':
        print(choice + " is not defined!")
        choice = input("(R)un tests, (C)reate tests, (S)how existing tests, (Q)uit\n>>> ")
    if choice == 'R' or choice == 'r':
        do_r()
    elif choice == 'C' or choice == 'c':
        isAvanced = input("(S)mple or (A)dvanced test ?\n>>> ")
        while isAvanced != 'S' and isAvanced != 's' and isAvanced != 'A' and isAvanced != 'a':
            print(isAvanced + " is not defined!")
            isAvanced = input("(S)mple or (A)dvanced test ?\n>>> ")
        do_c(False if isAvanced == 'S' or isAvanced == 's' else True)
    elif choice == 'S' or choice == 's':
        do_s()
    elif choice == 'Q' or choice == 'q':
        print("Exiting program...")
        return

def main():
    start_ask()

main()