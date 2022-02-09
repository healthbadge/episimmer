import functools
import math
import os.path as osp
from typing import TYPE_CHECKING, Callable, Dict, List, Tuple, Union

import matplotlib.animation as ani
import matplotlib.collections as collections
import matplotlib.figure as figure
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.axes import Axes

from .arg_parser import parse_args
from .time import Time

if TYPE_CHECKING:
    from episimmer.model import BaseModel
    from episimmer.simulate import Simulate


def plot_results(example_path: str, model: 'BaseModel',
                 avg_dict: Dict[str, List[float]],
                 stddev_dict: Dict[str,
                                   List[float]], max_dict: Dict[str,
                                                                List[int]],
                 min_dict: Dict[str, List[int]], plot: bool) -> None:
    """
    Plots the epidemic trajectory

    Args:
        example_path: Path to directory containing simulation files
        model: Disease model used
        avg_dict: Average of epidemic trajectory
        stddev_dict: Standard deviation of epidemic trajectory
        max_dict: Maximum values of epidemic trajectory across worlds
        min_dict: Minimum values of epidemic trajectory across worlds
        plot: Boolean used to plot the epidemic trajectory
    """
    for state in avg_dict.keys():
        x = np.arange(0, len(avg_dict[state]))
        plt.plot(avg_dict[state], color=model.colors[state])
        # y=np.array(avg_dict[state])
        # error=np.array(stddev_dict[state])
        plt.fill_between(x,
                         min_dict[state],
                         max_dict[state],
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


def buildgraph(i: int, model: 'BaseModel',
               avg_dict: Dict[str, List[float]]) -> None:
    """
    Builds the epidemic trajectory graph for current frame i

    Args:
        i: Current frame
        model: Disease model used
        avg_dict: Average of epidemic trajectory
    """
    plt.clf()
    plt.title(model.name + ' Plot')
    plt.ylabel('Population')
    plt.xlabel('Time Steps (in unit steps)')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    for state in avg_dict.keys():
        plt.plot(avg_dict[state][:i], label=state, color=model.colors[state])
    plt.legend(loc='upper left', shadow=True)


def store_animated_time_plot(example_path: str, model: 'BaseModel',
                             avg_dict: Dict[str, List[float]]) -> None:
    """
    Saves the animation of epidemic trajectory to a gif file

    Args:
        example_path: Path to directory containing simulation files
        model: Disease model used
        avg_dict: Average of epidemic trajectory
    """
    fig = plt.figure()
    fig.set_size_inches(8, 5)

    anim = ani.FuncAnimation(fig,
                             buildgraph,
                             interval=100,
                             fargs=(model, avg_dict))
    anim.save(osp.join(example_path, 'results', 'time_plot.gif'),
              writer=ani.PillowWriter(fps=10))


def get_interaction_graph_from_object(obj: 'Simulate') -> nx.Graph:
    """
    Generates the interaction graph from the simulation object

    Args:
        obj: Simulation object

    Returns:
        Interaction graph
    """
    agents_obj = obj.agents_obj
    model = obj.model
    locations_obj = obj.locations_obj

    number_of_agents = agents_obj.n
    root_num = int(math.sqrt(number_of_agents))
    agents_dict = agents_obj.agents
    infected_states = model.infected_states

    g = nx.Graph()

    # Agent Nodes
    for i, agent in enumerate(agents_dict.values()):
        if agent.state in infected_states:
            g.add_node(agent.index,
                       color=model.colors[agent.state],
                       pos=(500 * (i % root_num), 500 * (i / root_num)))
        else:
            g.add_node(agent.index,
                       color=model.colors[agent.state],
                       pos=(500 * (i % root_num), 500 * (i / root_num)))

    # Interactions
    for agent in agents_dict.values():
        if agent.can_contribute_infection > 0:
            for int_agent in agent.contact_list:
                int_agent_indx = int_agent['Interacting Agent Index']
                if (agents_obj.agents[int_agent_indx].can_receive_infection >
                        0):
                    g.add_edge(agent.index, int_agent_indx, color='black')

    # Events
    for j, location in enumerate(locations_obj.locations.values()):
        if not location.lock_down_state:
            for i, event_info in enumerate(location.events):
                g.add_node(event_info['Location Index'] + '_event' + str(i),
                           color='#40E0D0',
                           pos=(-1500 - 500 * j, 500 * i))
                for agent in event_info['Agents']:
                    if (agents_obj.agents[agent].can_receive_infection > 0 or
                            agents_obj.agents[agent].can_contribute_infection >
                            0):
                        g.add_edge(event_info['Location Index'] + '_event' +
                                   str(i),
                                   agent,
                                   color='black')

    return g


def save_env_graph() -> Callable:
    """
    Decorator to save the interactions graph to the :class:`~episimmer.simulate.Simulate` object

    Returns:
        Callable function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(ref: 'Simulate', *args, **kwargs) -> None:
            func(ref, *args, **kwargs)
            if ref.config_obj.worlds - 1 == Time.get_current_world():
                args = parse_args()
                if args.viz_dyn:
                    g = get_interaction_graph_from_object(ref)
                    ref.g_list.append(g)

        return wrapper

    return decorator


def set_ax_params(ax: Axes, model: 'BaseModel', time_step: int) -> Axes:
    """
    Sets the title and legend of the Axes for the interaction graph

    Args:
        ax: Axes
        model: Disease model used
        time_step: Current time step

    Returns:
        Axes
    """
    ax.set_title(f'Time step {time_step}', {'fontsize': 18})
    for state in model.individual_state_types:
        ax.scatter([0], [0], color=model.colors[state], label=state)

    ax.scatter([0], [0], color='#40E0D0',
               label='Event location')  # Events - Turquoise
    ax.scatter([0], [0], color='#FFFFFF')

    ax.legend(bbox_to_anchor=(1, 1), prop={'size': 12})
    return ax


def draw_graph(
    g: nx.Graph, ax: Axes, seed: Union[str, int]
) -> Tuple[collections.PatchCollection, collections.LineCollection]:
    """
    Sets the node positions and edges according to the spring layout and returns them.

    Args:
        g: Current interaction graph
        ax: Axes
        seed: Seed for consistent graph

    Returns:
        Nodes and Edges

    """
    pos = nx.get_node_attributes(g, 'pos')
    color = nx.get_node_attributes(g, 'color')

    # Shuffling positions
    # temp = list(pos.values())
    # random.shuffle(temp)
    # pos = dict(zip(pos, temp))

    # Layout positions
    pos = nx.spring_layout(g, seed=int(seed))

    nodes = nx.draw_networkx_nodes(g, pos, node_color=color.values(), ax=ax)
    edges = nx.draw_networkx_edges(g,
                                   pos,
                                   ax=ax,
                                   connectionstyle='arc3, rad = 0.1')
    return nodes, edges


def animate_graph(
    time_step: int, fig: figure.Figure, model: 'BaseModel',
    g_list: List[nx.Graph], seed: Union[str, int]
) -> Tuple[collections.PatchCollection, collections.LineCollection]:
    """
    Sets up the figure to plot the current time step interaction network

    Args:
        time_step: Current time step
        fig: Figure used to plot
        model: Disease model used
        g_list: List of interaction graphs for every time step
        seed: Seed for consistent graph

    Returns:
        Nodes and edges for current time step
    """
    if not seed:
        seed = 42
    fig.clf()
    ax = fig.gca()
    ax = set_ax_params(ax, model, time_step)

    current_g = g_list[time_step % len(g_list)]
    return draw_graph(current_g, ax, seed)


def store_animated_dynamic_graph() -> Callable:
    """
    Decorator to store the evolving interactions graph as a gif.

    Returns:
        Callable function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(ref: 'Simulate', *args, **kwargs) -> None:
            if ref.config_obj.worlds - 1 == Time.get_current_world():
                cmd_args = parse_args()
                if cmd_args.viz_dyn:

                    fig = plt.figure()
                    fig.set_size_inches(20, 14)
                    anim = ani.FuncAnimation(
                        fig,
                        animate_graph,
                        frames=ref.config_obj.time_steps,
                        fargs=(fig, ref.model, ref.g_list,
                               ref.config_obj.random_seed))
                    anim.save(osp.join(ref.config_obj.example_path, 'results',
                                       'dyn_graph.gif'),
                              writer=ani.PillowWriter(fps=5))
                    fig.clf()

            return func(ref, *args, **kwargs)

        return wrapper

    return decorator
