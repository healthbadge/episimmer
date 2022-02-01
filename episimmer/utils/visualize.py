from typing import Callable, Dict, List, Union, ValuesView,Tuple
from xmlrpc.client import Boolean
import functools
import math
import os.path as osp

import matplotlib.animation as ani
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .arg_parser import parse_args
from .time import Time


def plot_results(example_path:str, model:object, avg_dict:Dict[str,List[int]], stddev_dict, maxdict:Dict[str,int], mindict:Dict[str,int],
                 plot)->None:
    """
    Plots the result of simulation.

    Args:
        example_path:path of episimmer example.
        model:model object of example.
        maxdict:global maxima of state of example.
        mindict:global minima of state of example.
    """
    for state in avg_dict.keys():
        x = np.arange(0, len(avg_dict[state]))
        plt.plot(avg_dict[state], color=model.colors[state])
        #y=np.array(avg_dict[state])
        #error=np.array(stddev_dict[state])
        plt.fill_between(x,
                         mindict[state],
                         maxdict[state],
                         alpha=0.2,
                         facecolor=model.colors[state],
                         linewidth=0)
    plt.title(model.name + ' Plot')
    plt.legend(list(avg_dict.keys()), loc='upper right', shadow=True)
    plt.ylabel('Population')
    plt.xlabel('Time Steps (in unit steps)')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    fig = plt.gcf()
    fig.set_size_inches(8, 5)
    if plot:
        plt.show()
    fig.savefig(osp.join(example_path, 'results', 'results.jpg'))


def buildgraph(i, fig, model: object , tdict)->None:
    """
    Noting down labels of graph.

    Args:
        model:Model object of example.

    """
    plt.clf()
    plt.title(model.name + ' Plot')
    plt.ylabel('Population')
    plt.xlabel('Time Steps (in unit steps)')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    for state in tdict.keys():
        plt.plot(tdict[state][:i], label=state, color=model.colors[state])
    plt.legend(loc='upper left', shadow=True)


def store_animated_time_plot(example_path, model, tdict):
    fig = plt.figure()
    fig.set_size_inches(8, 5)

    anim = ani.FuncAnimation(fig,
                             buildgraph,
                             interval=100,
                             fargs=(fig, model, tdict))
    anim.save(osp.join(example_path, 'results', 'time_plot.gif'),
              writer=ani.PillowWriter(fps=10))


def get_interaction_graph_from_object(obj)->Graph:

    agents_obj = obj.agents_obj
    model = obj.model
    locations_obj = obj.locations_obj

    number_of_agents = agents_obj.n
    root_num = int(math.sqrt(number_of_agents))
    agents_dict = agents_obj.agents
    infected_states = model.infected_states

    G = nx.Graph()

    # Agent Nodes
    for i, agent in enumerate(agents_dict.values()):
        if (agent.state in infected_states):
            G.add_node(agent.index,
                       color=model.colors[agent.state],
                       pos=(500 * (i % root_num), 500 * (i / root_num)))
        else:
            G.add_node(agent.index,
                       color=model.colors[agent.state],
                       pos=(500 * (i % root_num), 500 * (i / root_num)))

    # Interactions
    for agent in agents_dict.values():
        if (agent.can_contribute_infection > 0):
            for int_agent in agent.contact_list:
                int_agent_indx = int_agent['Interacting Agent Index']
                if (agents_obj.agents[int_agent_indx].can_recieve_infection >
                        0):
                    G.add_edge(agent.index, int_agent_indx, color='black')

    # Events
    for j, location in enumerate(locations_obj.locations.values()):
        if not location.lock_down_state:
            for i, event_info in enumerate(location.events):
                G.add_node(event_info['Location Index'] + '_event' + str(i), color='#40E0D0',\
                             pos=(-1500 - 500 * j, 500 * i))
                for agent in event_info['Agents']:
                    if (agents_obj.agents[agent].can_recieve_infection > 0 or
                            agents_obj.agents[agent].can_contribute_infection >
                            0):
                        G.add_edge(event_info['Location Index'] + '_event' +
                                   str(i),
                                   agent,
                                   color='black')

    return G


def save_env_graph()->None:
    def decorator(func):
        @functools.wraps(func)
        def wrapper(ref, *args, **kwargs):
            func(ref, *args, **kwargs)
            if ref.config_obj.worlds - 1 == Time.get_current_world():
                args = parse_args()
                if (args.viz_dyn):
                    G = get_interaction_graph_from_object(ref)
                    ref.G_list.append(G)

        return wrapper

    return decorator


def set_ax_params(ax, model, timestep):
    ax.set_title(f'Timestep {timestep}', {'fontsize': 18})
    for state in model.individual_state_types:
        ax.scatter([0], [0], color=model.colors[state], label=state)

    ax.scatter([0], [0], color='#40E0D0',
               label='Event location')  # Events - Turquoise
    ax.scatter([0], [0], color='#FFFFFF')

    ax.legend(bbox_to_anchor=(1, 1), prop={'size': 12})
    return ax


def draw_graph(G, ax, seed):
    """

    """
    pos = nx.get_node_attributes(G, 'pos')
    color = nx.get_node_attributes(G, 'color')

    # Shuffling positions
    # temp = list(pos.values())
    # random.shuffle(temp)
    # pos = dict(zip(pos, temp))

    # Layout positions
    pos = nx.spring_layout(G, seed=int(seed))

    nodes = nx.draw_networkx_nodes(G, pos, node_color=color.values(), ax=ax)
    edges = nx.draw_networkx_edges(G,
                                   pos,
                                   ax=ax,
                                   connectionstyle='arc3, rad = 0.1')
    return nodes, edges


def animate_graph(timestep, fig, model, G_list, seed):
    if not seed:
        seed = 42
    fig.clf()
    ax = fig.gca()
    ax = set_ax_params(ax, model, timestep)

    current_G = G_list[timestep % len(G_list)]
    return draw_graph(current_G, ax, seed)


def store_animated_dynamic_graph():
    """
    Plots results of simulation as an animation.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(ref, *args, **kwargs):
            if ref.config_obj.worlds - 1 == Time.get_current_world():
                cmd_args = parse_args()
                if (cmd_args.viz_dyn):

                    fig = plt.figure()
                    fig.set_size_inches(20, 14)
                    anim = ani.FuncAnimation(
                        fig,
                        animate_graph,
                        frames=ref.config_obj.time_steps,
                        fargs=(fig, ref.model, ref.G_list,
                               ref.config_obj.random_seed))
                    anim.save(osp.join(ref.config_obj.example_path, 'results',
                                       'dyn_graph.gif'),
                              writer=ani.PillowWriter(fps=5))
                    fig.clf()

            return func(ref, *args, **kwargs)

        return wrapper

    return decorator
