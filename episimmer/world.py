import numpy as np

from .read_file import ReadAgents, ReadLocations, ReadOneTimeEvents
from .simulate import Simulate
from .utils.arg_parser import parse_args
from .utils.math import average, stddev
from .utils.time import Time
from .utils.visualize import plot_results, store_animated_time_plot


class World():
    def __init__(self, config_obj, model, policy_list, event_restriction_fn,
                 agents_filename, interactionFiles_list,
                 probabilistic_interactionFiles_list, locations_filename,
                 eventFiles_list, one_time_event_file):
        self.config_obj = config_obj
        self.policy_list = policy_list
        self.event_restriction_fn = event_restriction_fn
        self.agents_filename = agents_filename
        self.locations_filename = locations_filename
        self.model = model
        self.interactionFiles_list = interactionFiles_list
        self.probabilistic_interactionsFiles_list = probabilistic_interactionFiles_list
        self.eventFiles_list = eventFiles_list
        self.one_time_event_file = one_time_event_file

    def one_world(self):

        time_steps = self.config_obj.time_steps

        Time.new_world()

        # Initialize agents
        agents_obj = ReadAgents(self.agents_filename, self.config_obj)

        # Intialize locations
        locations_obj = ReadLocations(self.locations_filename, self.config_obj)

        # Initialize one time events
        oneTimeEvent_obj = ReadOneTimeEvents(self.one_time_event_file)

        sim_obj = Simulate(self.config_obj, self.model, self.policy_list,
                           self.event_restriction_fn, agents_obj,
                           locations_obj)
        sim_obj.onStartSimulation()

        for current_time_step in range(time_steps):
            sim_obj.onStartTimeStep(self.interactionFiles_list,
                                    self.eventFiles_list,
                                    self.probabilistic_interactionsFiles_list,
                                    oneTimeEvent_obj)
            sim_obj.handleTimeStepForAllAgents()
            sim_obj.endTimeStep()
            Time.increment_current_time_step()

        end_state = sim_obj.endSimulation()
        return end_state, agents_obj, locations_obj

    # Averages multiple simulations and plots a single plot
    def simulate_worlds(self):

        args = parse_args()
        plot = args.noplot
        anim = args.animate

        tdict = {}
        t2_dict = {}
        maxdict = {}
        mindict = {}
        for state in self.model.individual_state_types:
            tdict[state] = [0] * (self.config_obj.time_steps + 1)
            t2_dict[state] = [0] * (self.config_obj.time_steps + 1)
            maxdict[state] = [0] * (self.config_obj.time_steps + 1)
            mindict[state] = [np.inf] * (self.config_obj.time_steps + 1)

        for i in range(self.config_obj.worlds):
            sdict, _, _ = self.one_world()
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j] += sdict[state][j]
                    t2_dict[state][j] += sdict[state][j]**2
                    maxdict[state][j] = max(maxdict[state][j], sdict[state][j])
                    mindict[state][j] = min(mindict[state][j], sdict[state][j])

        # Average number time series
        avg_dict = average(tdict, self.config_obj.worlds)
        stddev_dict = stddev(tdict, t2_dict, self.config_obj.worlds)
        plot_results(self.config_obj.example_path, self.model, avg_dict,
                     stddev_dict, maxdict, mindict, plot)
        if anim:
            store_animated_time_plot(self.config_obj.example_path, self.model,
                                     avg_dict)

        return avg_dict
