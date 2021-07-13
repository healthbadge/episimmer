import matplotlib.pyplot as plt
import matplotlib.animation as ani
import importlib.util
import argparse

def average(tdict, number):
    for k in tdict.keys():
        l = tdict[k]
        for i in range(len(l)):
            tdict[k][i] /= number
    return tdict

def plotResults(model_name, tdict, plot):
    for state in tdict.keys():
        plt.plot(tdict[state])
    plt.title(model_name + ' Plot')
    plt.legend(list(tdict.keys()), loc='upper right', shadow=True)
    plt.ylabel('Population')
    plt.xlabel('Time Steps (in unit steps)')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999',linestyle='-', alpha=0.2)
    fig = plt.gcf()
    if plot:
        plt.show()
    return fig

def animateResults(model_name, tdict):
    fig = plt.figure()
    def buildmebarchart(i=int):
        plt.clf()
        plt.title(model_name + ' Plot')
        plt.ylabel('Population')
        plt.xlabel('Time Steps (in unit steps)')
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        for state in tdict.keys():
            plt.plot(tdict[state][:i], label=state)
        plt.legend(loc='upper left', shadow=True)
    return ani.FuncAnimation(fig, buildmebarchart, interval=150)


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def parse_args():
    arg_parser = argparse.ArgumentParser(prog='Main.py', usage='%(prog)s example_path [options]')

    # input argument options
    arg_parser.add_argument(dest="example_path", type = str, help="Pass the path to your data folder")
    arg_parser.add_argument("-np", "--noplot", dest="noplot", action="store_false", default=True, help="doesn't show plot after simulation")
    arg_parser.add_argument("-an", "--animate", dest="animate", action="store_true", default=False, help="creates gif animation in the example folder")
    arg_parser.add_argument("-s", "--stats", dest="stats", action="store_true", default=False, help="Choose to store statistics. Default = False")
    args = arg_parser.parse_args()
    return args
