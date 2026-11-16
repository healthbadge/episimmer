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
        self.assertRaises(TypeError, base_model.set_symptomatic_states, 1)
        self.assertRaises(ValueError, base_model.set_symptomatic_states,
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

        self.assertRaises(TypeError, base_model.get_final_infection_prob, None,
                          None, agent0, agents)

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

    def test_stoch_set_transition(self):
        stoch_model = StochasticModel(['Susceptible', 'Infected', 'Recovered'],
                                      ['Infected'], {
                                          'Susceptible': 0.99,
                                          'Infected': 0.01,
                                          'Recovered': 0.0
                                      })
        stoch_model.set_transition('Susceptible', 'Infected',
                                   stoch_model.p_standard(0.1))
        stoch_model.set_transition('Infected', 'Recovered',
                                   stoch_model.p_infection())

        def p_func(time_step):
            return 0.1 * time_step

        stoch_model.set_transition('Recovered', 'Susceptible',
                                   stoch_model.p_function(p_func))

        self.assertRaises(TypeError, stoch_model.set_transition, 'Susceptible',
                          'Recovered', 1.0)

    def test_stoch_p_standard(self):
        stoch_model = StochasticModel(['Susceptible', 'Infected', 'Recovered'],
                                      ['Infected'], {
                                          'Susceptible': 0.99,
                                          'Infected': 0.01,
                                          'Recovered': 0.0
                                      })
        self.assertRaises(ValueError, stoch_model.p_standard, -1)
        self.assertRaises(ValueError, stoch_model.p_standard, 1.2)
        self.assertRaises(TypeError, stoch_model.p_standard, 'abc')

    def test_stoch_p_function(self):
        stoch_model = StochasticModel(['Susceptible', 'Infected', 'Recovered'],
                                      ['Infected'], {
                                          'Susceptible': 0.99,
                                          'Infected': 0.01,
                                          'Recovered': 0.0
                                      })

        def p_func(a, b, c):
            return 0.1

        self.assertRaises(TypeError, stoch_model.p_function, p_func)
        self.assertRaises(TypeError, stoch_model.p_function, 1.5)

    def test_stoch_p_infection(self):
        stoch_model = StochasticModel(['Susceptible', 'Infected', 'Recovered'],
                                      ['Infected'], {
                                          'Susceptible': 0.99,
                                          'Infected': 0.01,
                                          'Recovered': 0.0
                                      })

        def prob_of_inter_fn(a, b, c, d):
            return 0.1

        self.assertRaises(TypeError, stoch_model.p_infection, prob_of_inter_fn,
                          6)
        self.assertRaises(TypeError, stoch_model.p_infection, prob_of_inter_fn,
                          ['abc', 'bcd'])

        def prob_of_inter_fn_inc(a, b, c):
            return 0.1

        self.assertRaises(TypeError, stoch_model.p_infection,
                          prob_of_inter_fn_inc)
        self.assertWarns(UserWarning, stoch_model.p_infection, None,
                         [0.1, 0.2])

    def test_sched_insert_state(self):
        sched_model = ScheduledModel()
        self.assertRaises(TypeError, sched_model.insert_state, 1, None, None,
                          sched_model.scheduled({'2': 1}), False, 0)
        self.assertRaises(TypeError, sched_model.insert_state,
                          'Infected', 1.1, 2.2,
                          sched_model.scheduled({'Recovered': 1}), True, 0.1)
        self.assertRaises(TypeError, sched_model.insert_state, 'Infected', 1,
                          2, 10, False, 0.1)
        self.assertRaises(TypeError, sched_model.insert_state, 'Infected', 1,
                          2, sched_model.scheduled({'Recovered': 1}), 9, 0.1)
        self.assertRaises(ValueError, sched_model.insert_state,
                          'Infected', 1, 2,
                          sched_model.scheduled({'Recovered': 1}), True, 1.1)
        self.assertRaises(ValueError, sched_model.insert_state,
                          'Infected', 1, 2,
                          sched_model.scheduled({'Recovered': 1}), True, -0.1)

    def test_sched_insert_state_custom(self):
        sched_model = ScheduledModel()

        def fn(time_step):
            if time_step < 10:
                return 1

            else:
                return 3

        self.assertRaises(TypeError, sched_model.insert_state_custom, 1, fn,
                          sched_model.scheduled({'2': 1}), False, 0)
        self.assertRaises(TypeError, sched_model.insert_state_custom,
                          'Infected', 12,
                          sched_model.scheduled({'Recovered': 1}), True, 0.1)
        self.assertRaises(TypeError, sched_model.insert_state_custom,
                          'Infected', fn, 10, False, 0.1)
        self.assertRaises(TypeError, sched_model.insert_state_custom,
                          'Infected', fn,
                          sched_model.scheduled({'Recovered': 1}), 9, 0.1)
        self.assertRaises(ValueError, sched_model.insert_state_custom,
                          'Infected', fn,
                          sched_model.scheduled({'Recovered': 1}), True, 1.1)
        self.assertRaises(ValueError, sched_model.insert_state_custom,
                          'Infected', fn,
                          sched_model.scheduled({'Recovered': 1}), True, -0.1)

    def test_sched_scheduled(self):
        sched_model = ScheduledModel()

        self.assertRaises(TypeError, sched_model.scheduled, [1])
        self.assertRaises(TypeError, sched_model.scheduled,
                          {'Infected': 'abc'})
        self.assertRaises(TypeError, sched_model.scheduled, {1: 1})
        self.assertRaises(ValueError, sched_model.scheduled,
                          {'Infected': 0.99})

    def test_sched_p_infection(self):
        sched_model = ScheduledModel()

        self.assertRaises(TypeError, sched_model.p_infection, [1])
        self.assertRaises(TypeError, sched_model.p_infection,
                          {'Infected': 'abc'})
        self.assertRaises(TypeError, sched_model.p_infection, {1: 1})
        self.assertRaises(ValueError, sched_model.p_infection,
                          {'Infected': 0.99})

        new_states = {'Infected': 1}

        def prob_of_inter_fn(a, b, c, d):
            return 0.1

        self.assertRaises(TypeError, sched_model.p_infection, new_states,
                          prob_of_inter_fn, 6)
        self.assertRaises(TypeError, sched_model.p_infection, new_states,
                          prob_of_inter_fn, ['abc', 'bcd'])

        def prob_of_inter_fn_inc(a, b, c):
            return 0.1

        self.assertRaises(TypeError, sched_model.p_infection, new_states,
                          prob_of_inter_fn_inc)
        self.assertWarns(UserWarning, sched_model.p_infection, new_states,
                         None, [0.1, 0.2])


if __name__ == '__main__':
    unittest.main()
