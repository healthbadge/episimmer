import random

from .read_file import (ReadEvents, ReadInteractions,
                        ReadProbabilisticInteractions)
from .utils.statistics import save_stats
from .utils.time import Time
from .utils.visualize import save_env_graph, store_animated_dynamic_graph


class Simulate():
    def __init__(self, config_obj, model, policy_list, agents_obj,
                 locations_obj):
        self.agents_obj = agents_obj
        self.locations_obj = locations_obj
        self.model = model
        self.policy_list = policy_list
        self.config_obj = config_obj
        self.state_list = {}
        self.state_history = {}
        self.G_list = []

    def on_start_simulation(self):
        # Initialize state list
        for state in self.model.individual_state_types:
            self.state_list[state] = []
            self.state_history[state] = []

        # Initialize states
        self.model.initalize_states(self.agents_obj.agents)

        # Reset Policies
        for policy_index, policy in enumerate(self.policy_list):
            policy.reset(self.agents_obj.agents.values(), policy_index)

        # Update State list
        for agent in self.agents_obj.agents.values():
            self.state_list[agent.state].append(agent.index)

        # Store state list
        self.store_state()

    @save_env_graph()
    @save_stats([('agents_obj', 3)], 'Agents', ['state'])
    def on_start_time_step(self, interaction_files_list_of_list,
                           event_files_list_of_list,
                           probabilistic_interaction_files_list_of_list,
                           one_time_event_obj):

        for agent in self.agents_obj.agents.values():
            agent.new_time_step()

        for location in self.locations_obj.locations.values():
            location.new_time_step()

        # Initialize filenames
        interactions_filename = events_filename = None

        # Load interactions
        for interaction_files_list in interaction_files_list_of_list:
            if interaction_files_list:
                interactions_filename = interaction_files_list[
                    Time.get_current_time_step() % len(interaction_files_list)]
                ReadInteractions(interactions_filename, self.config_obj,
                                 self.agents_obj)

        # Load probabilistic interactions
        for probabilistic_interaction_files_list in probabilistic_interaction_files_list_of_list:
            if probabilistic_interaction_files_list:
                probabilistic_interactions_filename = probabilistic_interaction_files_list[
                    Time.get_current_time_step() %
                    len(probabilistic_interaction_files_list)]
                ReadProbabilisticInteractions(
                    probabilistic_interactions_filename, self.config_obj,
                    self.agents_obj)

        # Load Events
        for event_files_list in event_files_list_of_list:
            if event_files_list:
                events_filename = event_files_list[
                    Time.get_current_time_step() % len(event_files_list)]
                ReadEvents(events_filename, self.config_obj,
                           self.locations_obj, self.agents_obj)

        # Load One Time Events
        one_time_event_obj.ReadOneTimeEvents(self.config_obj,
                                             self.locations_obj,
                                             self.agents_obj)

        # Enact policies by updating agent and location states.
        for policy_index, policy in enumerate(self.policy_list):
            policy.enact_policy(Time.get_current_time_step(),
                                self.agents_obj.agents,
                                self.locations_obj.locations.values(),
                                self.model, policy_index)

        # Restrict agents with can_contribute_infection and can_receive_infection
        # All interactions and events restricted by removing elements in
        # agent.contact_list and location.events
        self.save_valid_interactions_events()

        # Enact post-policy procedures after updating agent contacts and event lists.
        for policy_index, policy in enumerate(self.policy_list):
            policy.post_policy(Time.get_current_time_step(),
                               self.agents_obj.agents,
                               self.locations_obj.locations.values(),
                               self.model, policy_index)

        if events_filename is not None:
            # Update event info to agents from location
            for location in self.locations_obj.locations.values():
                if not location.lock_down_state:
                    for event_info in location.events:
                        self.model.update_event_infection(
                            event_info, location, self.agents_obj)

    def handle_time_step_for_all_agents(self):
        # To ensure concurrency we update agent.next_state in method handleTimeStepAsAgent
        # After every agent has updated next_state we update states of all agents in method handleTimeStep()

        for agent in self.agents_obj.agents.values():
            self.handle_time_step_as_agent(agent)

        for agent in self.agents_obj.agents.values():
            self.convert_state(agent)

    def handle_time_step_as_agent(self, agent):
        # To ensure concurrency we update agent.next_state in method handleTimeStepAsAgent
        # After every agent has updated next_state we update states of all agents in method handleTimeStep()

        # Finding next_state
        agent.set_next_state(
            self.model.find_next_state(agent, self.agents_obj.agents))

    def end_time_step(self):
        self.store_state()

    def valid_interaction(self, agent, c_dict):
        if agent.under_protection:
            return False

        r = random.random()
        contact_index = c_dict['Interacting Agent Index']
        contact_agent = self.agents_obj.agents[contact_index]
        if r < contact_agent.can_contribute_infection and r < agent.can_recieve_infection:
            return True
        return False

    def store_event_lists(self, event_info):
        event_info['can_contrib'] = []
        event_info['can_receive'] = []
        for agent_index in event_info['Agents']:
            r = random.random()
            agent = self.agents_obj.agents[agent_index]

            if r < agent.can_contribute_infection:
                event_info['can_contrib'].append(agent_index)

            if not agent.under_protection and r < agent.can_recieve_infection:
                event_info['can_receive'].append(agent_index)

    def save_valid_interactions_events(self):
        for agent in self.agents_obj.agents.values():
            agent.contact_list[:] = [
                c_dict for c_dict in agent.contact_list
                if self.valid_interaction(agent, c_dict)
            ]

        for location in self.locations_obj.locations.values():
            for event_info in location.events:
                self.store_event_lists(event_info)

    @store_animated_dynamic_graph()
    def end_simulation(self):
        return self.state_history

    def store_state(self):
        for state in self.state_history.keys():
            self.state_history[state].append(len(self.state_list[state]))

    def convert_state(self, agent):
        self.state_list[agent.state].remove(agent.index)
        agent.update_state()
        self.state_list[agent.state].append(agent.index)
