import argparse
from csv import DictWriter

# python events.py events.txt -ag "1,2" -loc "3,4"

def makeEvents(filename, agents, locations, noHead):
    agList = ""
    locList = []
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
    agList = agList[:-1]
    if locations.endswith('.txt'):
        f = open(locations, 'r')
        n = f.readline()
        header = f.readline().strip('\n').split(':')
        lines = [x.strip('\n').split(':') for x in f.readlines()]
        index = header.index('Location Index')
        for line in lines:
            locList.append(line[index])
        f.close()
    elif locations.endswith('.csv'):
        f = open(locations, 'r')
        header = f.readline().strip('\n').split(',')
        lines = [x.strip('\n').split(',') for x in f.readlines()]
        index = header.index('Location Index')
        for line in lines:
            locList.append(line[index])
        f.close()
    else:
        locList = locations.split(',')

    if filename.endswith('.txt'):
        f = open(filename, 'a')
        if not noHead:
            f.write(str(len(locList)) + '\n')
            f.write('Location Index: Agents\n')
        for loc in locList:
            f.write(loc + ':' + agList + '\n')
        f.close()

    if filename.endswith('.csv'):
        with open(filename, 'a', newline='') as file:
            fieldnames = ['Location Index', 'Agents']
            writer = DictWriter(file, fieldnames=fieldnames)
            if not noHead:
                writer.writeheader()
            for loc in locList:
                writer.writerow({'Location Index': loc, 'Agents': agList })

def addLine(filename, value):
    f = open(filename, 'a')
    f.write(value + '\n')
    f.close()


def cleanFile(filename):
    f = open(filename, 'w')
    f.close()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Utility functions for generating agents file", usage='% (prog)s filename [options]')

    # options
    arg_parser.add_argument("filename")
    arg_parser.add_argument("--agents", "-ag", required=False)
    arg_parser.add_argument("--locations", "-loc", required=False)
    arg_parser.add_argument("--addLine", "-a", required=False)
    arg_parser.add_argument("--clean", "-c", action="store_true", required=False)
    arg_parser.add_argument("--noHeader", "-nh", action="store_true", required=False)

    args = arg_parser.parse_args()

    if args.clean:
        cleanFile(args.filename)
    if args.agents != None and args.locations != None:
        makeEvents(args.filename, args.agents, args.locations, args.noHeader)
    elif args.addLine:
        addLine(args.filename, args.addLine)
