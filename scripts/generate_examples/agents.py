import argparse
import ast
import random
from csv import DictWriter


def makeAgents(filename, n, titles="", pdicts=[]):
    k = len(titles)
    div = []
    for pdict in pdicts:
        if sum(pdict.values()) != 1:
            print("ERROR: Proportions don't add up to 1.")
            exit()
        else:
            div.append([[key, int(pdict[key] * n)] for key in pdict])
            for li in div:
                for i in range(len(li)):
                    if li[i][1] == 0 and len(li) != 1:
                        li.pop(i)

    if filename.endswith('.txt'):
        f = open(filename, 'w')
        if pdicts != None:
            f.write(str(n) + '\n')
            f.write('Agent Index:' + ':'.join(titles) + '\n')
            for i in range(n):
                f.write(str(i))
                for t in range(k):
                    index = random.randint(0, len(div[t]) - 1)
                    f.write(':' + div[t][index][0])
                    div[t][index][1] -= 1
                    if (div[t][index][1] == 0 and len(div[t]) != 1):
                        div[t].pop(index)
                f.write('\n')
        else:
            f.write(str(n) + '\n')
            f.write('Agent Index\n')
            for i in range(n):
                f.write(str(i) + '\n')
        f.close()

    if filename.endswith('.csv'):
        with open(filename, 'w', newline='') as file:
            if pdicts != None:
                fieldnames = ['Agent Index'] + titles
                writer = DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(n):
                    tdict = {'Agent Index': i}
                    for t in range(k):
                        index = random.randint(0, len(div[t]) - 1)
                        tdict[titles[t]] = div[t][index][0]
                        div[t][index][1] -= 1
                        if (div[t][index][1] == 0 and len(div[t]) != 1):
                            div[t].pop(index)
                    writer.writerow(tdict)
            else:
                fieldnames = ['Agent Index']
                writer = DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(n):
                    writer.writerow({'Agent Index': i})


def addLine(filename, value):
    f = open(filename, 'a')
    f.write(value + '\n')
    f.close()


def cleanFile(filename):
    f = open(filename, 'w')
    f.close()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Utility functions for generating agents file",
        usage='% (prog)s filename [options]')

    # options
    arg_parser.add_argument("filename")
    arg_parser.add_argument("--number", "-n", required=False)
    arg_parser.add_argument("--proportion", "-p", nargs=2, action='append',
                            required=False)
    arg_parser.add_argument("--addLine", "-a", required=False)
    arg_parser.add_argument("--clean", "-c", action="store_true",
                            required=False)

    args = arg_parser.parse_args()

    if args.number:
        if (args.proportion):
            titles = [x[0] for x in args.proportion]
            pdicts = [ast.literal_eval(x[1]) for x in args.proportion]
            makeAgents(args.filename, int(args.number), titles, pdicts)
        else:
            makeAgents(args.filename, int(args.number))
    elif args.addLine:
        addLine(args.filename, args.addLine)
    elif args.clean:
        cleanFile(args.filename)
