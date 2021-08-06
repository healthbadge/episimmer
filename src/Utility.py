import matplotlib.pyplot as plt
import matplotlib.animation as ani
import importlib.util
import argparse
import webbrowser
import functools
import os
import os.path as osp
from pyvis.network import Network
import time
import math
import Time
import numpy as np
import copy

def average(tdict, number):
    avg_dict=copy.deepcopy(tdict)
    for k in avg_dict.keys():
        l = avg_dict[k]
        for i in range(len(l)):
            avg_dict[k][i] /= number
    return avg_dict

def stddev(tdict, t2_dict, number):
    stddev_dict=copy.deepcopy(tdict)
    for k in stddev_dict.keys():
        l = stddev_dict[k]
        for i in range(len(l)):
            stddev_dict[k][i] = np.sqrt(t2_dict[k][i]/number - (tdict[k][i]/number)**2)
    return stddev_dict

def plotResults(model, avg_dict, stddev_dict, maxdict, mindict, plot):
    for state in avg_dict.keys():
        x=np.arange(0,len(avg_dict[state]))
        plt.plot(avg_dict[state], color=model.colors[state])
        #y=np.array(avg_dict[state])
        #error=np.array(stddev_dict[state])
        plt.fill_between(x, mindict[state], maxdict[state], alpha=0.2, facecolor=model.colors[state],linewidth=0)
    plt.title(model.name + ' Plot')
    plt.legend(list(avg_dict.keys()), loc='upper right', shadow=True)
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


def get_interaction_graph_from_object(obj):

    outpath = 'dynamic_graph.html'
    agents_obj = obj.agents_obj
    model = obj.model
    locations_obj = obj.locations_obj

    number_of_agents = agents_obj.n
    root_num = int(math.sqrt(number_of_agents))
    agents_dict = agents_obj.agents
    infected_states = model.infected_states

    net = Network()

    # Agent Nodes
    for i,agent in enumerate(agents_dict.values()):
        if(agent.state in infected_states):
            net.add_node(agent.index, x=100*(i%root_num), y = 100*(i/root_num), color = "red")
        else:
            net.add_node(agent.index, x=100*(i%root_num), y = 100*(i/root_num))

    # Interactions
    for agent in agents_dict.values():
        if(agent.can_contribute_infection):
            for int_agent in agent.contact_list:
                int_agent_indx = int_agent["Interacting Agent Index"]
                if(agents_obj.agents[int_agent_indx].can_recieve_infection):
                    net.add_edge(agent.index, int_agent_indx,color="black")

    # Events
    for j,location in enumerate(locations_obj.locations.values()):
        if not location.lock_down_state:
            for i,event_info in enumerate(location.events):
                net.add_node(event_info["Location Index"]+"_event"+str(i),x=-300 - 100*j,y=100*i,shape="triangle")
                for agent in event_info["Agents"]:
                    net.add_edge(event_info["Location Index"]+"_event"+str(i), agent,color="black")

    net.toggle_physics(False)
    net.show(outpath)
    return outpath

def viz_single_graph(obj):
    path = get_interaction_graph_from_object(obj)
    filename = 'file:'+os.sep+os.sep+osp.join(os.getcwd(),path)
    print("Timestep = "+str(Time.Time.get_current_time_step()))
    if Time.Time.get_current_time_step()==0:
        webbrowser.open_new(filename)
        time.sleep(3)
    else:
        webbrowser.open(filename, new=0)
        time.sleep(1)

def viz_dynamic_graph():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(ref, *args,**kwargs) :
            func(ref, *args, **kwargs)
            args = parse_args()
            if(args.viz_dyn):
                viz_single_graph(ref)
        return wrapper

    return decorator

def parse_args():
    arg_parser = argparse.ArgumentParser(prog='Main.py', usage='%(prog)s example_path [options]')

    # input argument options
    arg_parser.add_argument(dest="example_path", type = str, help="Pass the path to your data folder")
    arg_parser.add_argument("-np", "--noplot", dest="noplot", action="store_false", default=True, help="doesn't show plot after simulation")
    arg_parser.add_argument("-an", "--animate", dest="animate", action="store_true", default=False, help="creates gif animation in the example folder")
    arg_parser.add_argument("-s", "--stats", dest="stats", action="store_true", default=False, help="Choose to store statistics. Default = False")
    arg_parser.add_argument("-vd", "--vizdyn", dest="viz_dyn", action="store_true", default=False, help="Choose to vizualize simulation dynamically. Default = False")
    args = arg_parser.parse_args()
    return args
