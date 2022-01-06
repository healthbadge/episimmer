import argparse
from csv import DictWriter

def readAgents(agents):
    agList = ''
    if agents.endswith('.txt'):
        f = open(agents, 'r')
        n = f.readline()
        header = f.readline().strip('\n').split(':')
        lines = [x.strip('\n').split(':') for x in f.readlines()]
        index = header.index('Agent Index')
        for line in lines:
            agList += line[index] + ','
        f.close()
    elif agents.endswith('.csv'):
        f = open(agents, 'r')
        header = f.readline().strip('\n').split(',')
        lines = [x.strip('\n').split(',') for x in f.readlines()]
        index = header.index('Agent Index')
        for line in lines:
            agList += line[index] + ','
        f.close()
    else:
        agList = agents + ','
    return agList[:-1]

def makeEvents(filename, agents1, agents2, noHead, both):
    ag1 = readAgents(agents1).split(',')
    ag2 = readAgents(agents2).split(',')

    if filename.endswith('.txt'):
        f = open(filename, 'a')
        if not noHead:
            if both:
                f.write(str(2*len(ag1)*len(ag2)) + '\n')
            else:
                f.write(str(len(ag1)*len(ag2)) + '\n')
            f.write('Agent Index:Interacting Agent Index\n')
        for a1 in ag1:
            for a2 in ag2:
                f.write(a1 + ':' + a2 + '\n')
        if both:
            for a1 in ag2:
                for a2 in ag1:
                    f.write(a1 + ':' + a2 + '\n')
        f.close()

    if filename.endswith('.csv'):
        with open(filename, 'a', newline='') as file:
            fieldnames = ['Agent Index', 'Interacting Agent Index']
            writer = DictWriter(file, fieldnames=fieldnames)
            if not noHead:
                writer.writeheader()
            for a1 in ag1:
                for a2 in ag2:
                    writer.writerow({'Agent Index': a1, 'Interacting Agent Index': a2})
            if both:
                for a1 in ag2:
                    for a2 in ag1:
                        writer.writerow({'Agent Index': a1, 'Interacting Agent Index': a2})


def addLine(filename, value):
    f = open(filename, 'a')
    f.write(value + '\n')
    f.close()


def cleanFile(filename):
    f = open(filename, 'w')
    f.close()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Utility functions for generating agents file', usage='% (prog)s filename [options]')

    # options
    arg_parser.add_argument('filename')
    arg_parser.add_argument('--agents1', '-from', required=False)
    arg_parser.add_argument('--agents2', '-to', required=False)
    arg_parser.add_argument('--addLine', '-a', required=False)
    arg_parser.add_argument('--clean', '-c', action='store_true', required=False)
    arg_parser.add_argument('--both', '-b', action='store_true', required=False)
    arg_parser.add_argument('--noHeader', '-nh', action='store_true', required=False)

    args = arg_parser.parse_args()

    if args.clean:
        cleanFile(args.filename)
    if args.agents1 != None and args.agents1 != None:
        makeEvents(args.filename, args.agents1, args.agents2, args.noHeader, args.both)
    elif args.addLine:
        addLine(args.filename, args.addLine)
