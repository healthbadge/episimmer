import os.path as osp
import unittest

from episimmer import Agent, Location, ReadAgents
from episimmer.model import BaseModel, ScheduledModel, StochasticModel


class TestModel(unittest.TestCase):
    def test_state_proportion_checker(self):
        base_model = BaseModel('Test')
        success_dict = {'a': 0.1, 'b': 0.2, 'c': 0.7}
        fail_dict1 = {'a': 0.1, 'b': 0.2, 'c': 0.9}
        fail_dict2 = {'a': 0.1, 'b': 0.2, 'c': 0.1}
        base_model.state_proportion = success_dict
        self.assertIsNone(base_model.state_proportion_checker())
        base_model.state_proportion = fail_dict1
        self.assertRaises(ValueError, base_model.state_proportion_checker)
        base_model.state_proportion = fail_dict2
        self.assertRaises(ValueError, base_model.state_proportion_checker)

    def test_set_functions(self):
        base_model = BaseModel('Test')
        self.assertRaises(TypeError, base_model.set_event_receive_fn, 5)
        self.assertRaises(TypeError, base_model.set_event_contribution_fn,
                          lambda x, y, z: 1)
        self.assertRaises(TypeError, base_model.set_external_prevalence_fn, 1)
        base_model.individual_state_types = ['a', 'b', 'c']
        self.assertRaises(TypeError, base_model.set_symptomatic_states,
                          ['a', 'd'])

    def test_update_event_infection(self):
        base_model = BaseModel('Test')
        self.assertRaises(TypeError, base_model.update_event_infection, None,
                          None, None)
        base_model.set_event_contribution_fn(lambda w, x, y, z: 1)
        self.assertRaises(TypeError, base_model.update_event_infection, None,
                          None, None)

        agent0 = Agent('Infected', {'Agent Index': '0'})
        agent1 = Agent('Infected', {'Agent Index': '1'})
        agent2 = Agent('Susceptible', {'Agent Index': '2'})
        location = Location({'Location Index': '0'})
        event_info = {
            'Location Index': '0',
            '_can_contrib': ['0', '1'],
            '_can_receive': ['2']
        }
        agents_obj = ReadAgents('', None)
        agents_obj.agents = {'0': agent0, '1': agent1, '2': agent2}

        def contribute_fn(agent, e_info, loc, current_time_step):
            return 1

        def receive_fn(agent, ambient_infection, e_info, loc,
                       current_time_step):
            return ambient_infection * 0.01

        base_model.set_event_contribution_fn(contribute_fn)
        base_model.set_event_receive_fn(receive_fn)

        base_model.update_event_infection(event_info, location, agents_obj)
        self.assertListEqual(agent2.event_probabilities, [0.02])

    def test_get_final_infection_prob(self):
        base_model = BaseModel('Test')
        agent0 = Agent(None, {'Agent Index': '0'})
        agent1 = Agent(None, {'Agent Index': '1'})
        agent2 = Agent(None, {'Agent Index': '2'})
        agents = {'0': agent0, '1': agent1, '2': agent2}

        agent0.contact_list = [{
            'Agent Index': '0',
            'Interacting Agent Index': '1'
        }, {
            'Agent Index': '0',
            'Interacting Agent Index': '2'
        }]
        agent1.contact_list = [{
            'Agent Index': '1',
            'Interacting Agent Index': '0'
        }]
        agent1.event_probabilities = [0.3]
        agent2.contact_list = [{
            'Agent Index': '2',
            'Interacting Agent Index': '1'
        }, {
            'Agent Index': '2',
            'Interacting Agent Index': '0'
        }]

        def interactions_fn(p_infected_states_list, contact_agent, c_dict,
                            time_step):
            return 0.2

        def external_prev(agent, time_step):
            if agent.index == '2':
                return 0.5
            return 0.0

        base_model.set_external_prevalence_fn(external_prev)

        expected_result1 = 1 - (1 - 0.2)**2
        expected_result2 = 1 - (1 - 0.2) * (1 - 0.3)
        expected_result3 = 1 - (1 - 0.2)**2 + 0.5
        self.assertEqual(
            base_model.get_final_infection_prob(interactions_fn, [], agent0,
                                                agents), expected_result1)
        self.assertEqual(
            base_model.get_final_infection_prob(interactions_fn, [], agent1,
                                                agents), expected_result2)
        self.assertEqual(
            base_model.get_final_infection_prob(interactions_fn, [], agent2,
                                                agents), expected_result3)


if __name__ == '__main__':
    unittest.main()
