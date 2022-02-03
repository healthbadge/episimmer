import numpy as np

from .read_file import ReadAgents, ReadLocations, ReadOneTimeEvents
from .simulate import Simulate
from .utils.arg_parser import parse_args
from .utils.math import deep_copy_average, deep_copy_stddev
from .utils.time import Time
from .utils.visualize import plot_results, store_animated_time_plot


class World():
    def __init__(self, config_obj, model, policy_list, event_restriction_fn,
                 agents_filename, interaction_files_list,
                 probabilistic_interaction_files_list, locations_filename,
                 event_files_list, one_time_event_file):
        self.config_obj = config_obj
        self.policy_list = policy_list
        self.event_restriction_fn = event_restriction_fn
        self.agents_filename = agents_filename
        self.locations_filename = locations_filename
        self.model = model
        self.interaction_files_list = interaction_files_list
        self.probabilistic_interaction_files_list = probabilistic_interaction_files_list
        self.event_files_list = event_files_list
        self.one_time_event_file = one_time_event_file

    def one_world(self):

        time_steps = self.config_obj.time_steps

        Time.new_world()

        # Initialize agents
        agents_obj = ReadAgents(self.agents_filename, self.config_obj)

        # Initialize locations
        locations_obj = ReadLocations(self.locations_filename, self.config_obj)

        # Initialize one time events
        one_time_event_obj = ReadOneTimeEvents(self.one_time_event_file)

        sim_obj = Simulate(self.config_obj, self.model, self.policy_list,
                           self.event_restriction_fn, agents_obj,
                           locations_obj)
        sim_obj.on_start_simulation()

        for current_time_step in range(time_steps):
            sim_obj.on_start_time_step(
                self.interaction_files_list, self.event_files_list,
                self.probabilistic_interaction_files_list, one_time_event_obj)
            sim_obj.handle_time_step_for_all_agents()
            sim_obj.end_time_step()
            Time.increment_current_time_step()

        end_state = sim_obj.end_simulation()
        return end_state, agents_obj, locations_obj

    # Averages multiple simulations and plots a single plot
    def simulate_worlds(self):

        args = parse_args()
        plot = args.noplot
        anim = args.animate

        tdict = {}
        t2_dict = {}
        max_dict = {}
        min_dict = {}
        for state in self.model.individual_state_types:
            tdict[state] = [0] * (self.config_obj.time_steps + 1)
            t2_dict[state] = [0] * (self.config_obj.time_steps + 1)
            max_dict[state] = [0] * (self.config_obj.time_steps + 1)
            min_dict[state] = [np.inf] * (self.config_obj.time_steps + 1)

        for i in range(self.config_obj.worlds):
            sdict, _, _ = self.one_world()
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j] += sdict[state][j]
                    t2_dict[state][j] += sdict[state][j]**2
                    max_dict[state][j] = max(max_dict[state][j],
                                             sdict[state][j])
                    min_dict[state][j] = min(min_dict[state][j],
                                             sdict[state][j])

        # Average number time series
        avg_dict = deep_copy_average(tdict, self.config_obj.worlds)
        stddev_dict = deep_copy_stddev(tdict, t2_dict, self.config_obj.worlds)
        plot_results(self.config_obj.example_path, self.model, avg_dict,
                     stddev_dict, max_dict, min_dict, plot)
        if anim:
            store_animated_time_plot(self.config_obj.example_path, self.model,
                                     avg_dict)

        return avg_dict
