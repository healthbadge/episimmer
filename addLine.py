
import argparse
import os
os.chdir("examples")


def add_line(s):
    dirs = [x[0] for x in os.walk(os.getcwd())]
    for folder in dirs[1:]:
        config_file = open(folder + "/" + "config.txt", "a")
        checker = open(folder + "/" + "config.txt", "rb+")
        print(folder)
        checker.seek(checker.tell() - 1, 2)
        if(checker.read() == b'\n'):
            config_file.write(s + "\n")
        else:
            config_file.write("\n" + s + "\n")
        config_file.close()
        checker.close()

def add_top_line(s):
    dirs = [x[0] for x in os.walk(os.getcwd())]
    for folder in dirs[1:]:
        f = open(folder + "/" + "config.txt", "r")
        lines = f.readlines()
        f.close()
        f = open(folder + "/" + "config.txt", "w")
        f.write(s + "\n")
        for line in lines:
            f.write(line)
        f.close()

def delete_top_line():
    dirs = [x[0] for x in os.walk(os.getcwd())]
    for folder in dirs[1:]:
        f = open(folder + "/" + "config.txt", "r")
        lines = f.readlines()
        f.close()
        f = open(folder + "/" + "config.txt", "w")
        for line in lines[1:]:
            f.write(line)
        f.close()

def delete_line():
    dirs = [x[0] for x in os.walk(os.getcwd())]
    for folder in dirs[1:]:
        f = open(folder + "/" + "config.txt", "r")
        lines = f.readlines()
        f.close()
        f = open(folder + "/" + "config.txt", "w")
        for line in lines[:-1]:
            f.write(line)
        f.close()


def makescript():
    dirname = [x[1] for x in os.walk(os.getcwd())]
    os.chdir("..")
    f = open("testingScript.sh", "w")
    f.write("#!/bin/sh\n")
    f.write("cd examples\n")
    for folder in dirname[0]:
        f.write("python ../src/Main.py \"" + folder + "\"\n")
    f.close()
    os.chdir("examples")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Adds lines to config files in examples. Needs input line to be written. ")

    # options
    arg_parser.add_argument("--line", "-l", help="Line to be written in config file", required=False)
    arg_parser.add_argument("--delete", "-d", help="Delete Last n Lines", required=False)
    arg_parser.add_argument("--topline", "-topl", help="Line to be written in config file", required=False)
    arg_parser.add_argument("--topdelete", "-topd", help="Delete First n Lines", required=False)
    args = arg_parser.parse_args()

    if args.delete is not None:
        if(args.delete == 'all'):
            dirs = [x[0] for x in os.walk(os.getcwd())]
            for folder in dirs[1:]:
                f = open(folder + "/" + "config.txt", "w")
                f.close()
        else:
            try:
                for i in range((int)(args.delete)):
                    delete_line()
            except:
                pass

    if args.line is not None:
        add_line(args.line)

    if args.topline is not None:
        add_top_line(args.topline)

    if args.topdelete is not None:
        try:
            print(args.delete)
            for i in range((int)(args.delete)):
                delete_top_line()
        except:
            pass

    #makescript()  # make script to check all examples

