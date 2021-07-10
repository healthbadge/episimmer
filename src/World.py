import Simulate
import ReadFile
import os
from Utility import *

class World():
    def __init__(self, config_obj, model, policy_list, event_restriction_fn, agents_filename, interactionFiles_list, probabilistic_interactionFiles_list, locations_filename, eventFiles_list, one_time_event_file):
        self.config_obj = config_obj
        self.policy_list = policy_list
        self.event_restriction_fn = event_restriction_fn
        self.agents_filename = agents_filename
        self.locations_filename = locations_filename
        self.model = model
        self.interactionFiles_list = interactionFiles_list
        self.probabilistic_interactionsFiles_list=probabilistic_interactionFiles_list
        self.eventFiles_list = eventFiles_list
        self.one_time_event_file = one_time_event_file

    def one_world(self):

        time_steps = self.config_obj.time_steps

        # Initialize agents
        agents_obj = ReadFile.ReadAgents(self.agents_filename, self.config_obj)

        # Intialize locations
        locations_obj = ReadFile.ReadLocations(self.locations_filename, self.config_obj)

        # Initialize one time events
        oneTimeEvent_obj = ReadFile.ReadOneTimeEvents(self.one_time_event_file)

        sim_obj = Simulate.Simulate(self.config_obj, self.model, self.policy_list, self.event_restriction_fn, agents_obj, locations_obj)
        sim_obj.onStartSimulation()

        for current_time_step in range(time_steps):
            sim_obj.onStartTimeStep(self.interactionFiles_list, self.eventFiles_list, self.probabilistic_interactionsFiles_list, oneTimeEvent_obj, current_time_step)
            sim_obj.handleTimeStepForAllAgents()
            sim_obj.endTimeStep()

        end_state = sim_obj.endSimulation()
        return end_state, agents_obj, locations_obj

    # Averages multiple simulations and plots a single plot
    def simulate_worlds(self, plot, anim):

        tdict = {}
        for state in self.model.individual_state_types:
            tdict[state] = [0]*(self.config_obj.time_steps+1)

        for i in range(self.config_obj.worlds):
            sdict, _, _ = self.one_world()
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j] += sdict[state][j]

        # Average number time series
        tdict = average(tdict, self.config_obj.worlds)
        # make a results directory
        if not os.path.isdir(self.config_obj.example_path + '/results'):
            os.mkdir(self.config_obj.example_path + '/results')
        plottor = plotResults(self.model.name, tdict, plot)
        plottor.savefig(self.config_obj.example_path + '/results/results.jpg')
        if anim:
            animator = animateResults(self.model.name, tdict)
            animator.save(self.config_obj.example_path + '/results/results.gif')

        return tdict
