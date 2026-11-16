import os.path as osp
import unittest

from episimmer.read_file import (ReadAgents, ReadConfiguration, ReadEvents,
                                 ReadInteractions, ReadLocations,
                                 ReadOneTimeEvents,
                                 ReadProbabilisticInteractions,
                                 ReadVDConfiguration)


class TestReadFile(unittest.TestCase):

    def test_read_config(self):
        example_path = osp.join('tests', 'unit', 'Complete_Interaction_Space')
        config_filename = osp.join(example_path, 'config.txt')
        config_obj = ReadConfiguration(config_filename)

        target_dict = {
            'filename':
            'tests/unit/Complete_Interaction_Space/config.txt',
            'example_path':
            'tests/unit/Complete_Interaction_Space',
            'random_seed':
            '10',
            'worlds':
            1,
            'time_steps':
            10,
            'agent_info_keys':
            'Agent Index',
            'agents_filename':
            'agents.csv',
            'interaction_info_keys':
            'Agent Index:Interacting Agent Index:duration',
            'interactions_files_list_list':
            ['interaction_files_list.txt', 'interaction_files_list2.txt'],
            'probabilistic_interactions_files_list_list': [
                'probabilistic_interaction_files_list.txt',
                'probabilistic_interaction_files_list2.txt'
            ],
            'location_info_keys':
            'Location Index',
            'locations_filename':
            'locations.txt',
            'event_info_keys':
            'Location Index:Agents',
            'events_files_list_list':
            ['event_files_list.txt', 'event_files_list2.txt'],
            'one_time_event_file':
            'one_time_event.txt'
        }
        self.assertDictEqual(target_dict, config_obj.__dict__)

        agents_filename, interactions_files_list_filename, \
            events_files_list_filename, locations_filename, \
            one_time_event_file, \
            probabilistic_interactions_files_list_filename = config_obj.get_file_paths(example_path)

        self.assertEqual('tests/unit/Complete_Interaction_Space/agents.csv',
                         agents_filename)
        self.assertListEqual([
            'tests/unit/Complete_Interaction_Space/interaction_files_list.txt',
            'tests/unit/Complete_Interaction_Space/interaction_files_list2.txt'
        ], interactions_files_list_filename)
        self.assertListEqual([
            'tests/unit/Complete_Interaction_Space/event_files_list.txt',
            'tests/unit/Complete_Interaction_Space/event_files_list2.txt'
        ], events_files_list_filename)
        self.assertListEqual([
            'tests/unit/Complete_Interaction_Space/probabilistic_interaction_files_list.txt',
            'tests/unit/Complete_Interaction_Space/probabilistic_interaction_files_list2.txt'
        ], probabilistic_interactions_files_list_filename)

        self.assertEqual('tests/unit/Complete_Interaction_Space/locations.txt',
                         locations_filename)
        self.assertEqual(
            'tests/unit/Complete_Interaction_Space/one_time_event.txt',
            one_time_event_file)

        interactions_files_list, events_files_list, \
            probabilistic_interactions_files_list = config_obj.get_file_names_list(
                                                                example_path, interactions_files_list_filename,
                                                                events_files_list_filename,
                                                                probabilistic_interactions_files_list_filename)

        self.assertListEqual(
            [['tests/unit/Complete_Interaction_Space/interactions_list.csv'],
             ['tests/unit/Complete_Interaction_Space/interactions_list2.txt']],
            interactions_files_list)
        self.assertListEqual(
            [[
                'tests/unit/Complete_Interaction_Space/empty_event.txt',
                'tests/unit/Complete_Interaction_Space/non_empty_event.txt'
            ],
             [
                 'tests/unit/Complete_Interaction_Space/non_empty_event.txt',
                 'tests/unit/Complete_Interaction_Space/empty_event.txt'
             ]], events_files_list)
        self.assertListEqual([
            [
                'tests/unit/Complete_Interaction_Space/probabilistic_interactions_list.txt'
            ],
            [
                'tests/unit/Complete_Interaction_Space/probabilistic_interactions_list2.txt'
            ]
        ], probabilistic_interactions_files_list)

        print('Read config test Complete!')

    def test_read_vd_config(self):
        example_path = osp.join('tests', 'unit', 'Complete_Interaction_Space')
        config_filename = osp.join(example_path, 'vd_config.txt')
        vd_config_obj = ReadVDConfiguration(config_filename)
        target_dict = {
            'filename': 'tests/unit/Complete_Interaction_Space/vd_config.txt',
            'example_path': 'tests/unit/Complete_Interaction_Space',
            'target': 'Agent',
            'algorithm': 'EarlyVulnerableAgent',
            'parameter_dict': {
                'states': ['Infected', 'Recovered'],
                'num_runs': 100
            },
            'pre_process': '',
            'post_process': '',
            'output_mode': 'Default'
        }

        self.assertDictEqual(target_dict, vd_config_obj.__dict__)

    def test_read_single_file(self):
        example_path = osp.join('tests', 'unit', 'Complete_Interaction_Space')
        config_filename = osp.join(example_path, 'config.txt')
        config_obj = ReadConfiguration(config_filename)
        agents_filename, _, _, locations_filename, one_time_event_file, _ = config_obj.get_file_paths(
            example_path)

        agents_obj = ReadAgents(agents_filename, config_obj)
        self.assertEqual(len(agents_obj.agents), 10)
        self.assertListEqual(agents_obj.parameter_keys, ['Agent Index'])

        locations_obj = ReadLocations(locations_filename, config_obj)
        self.assertEqual(len(locations_obj.locations), 5)
        self.assertListEqual(locations_obj.parameter_keys, ['Location Index'])

        one_time_event_obj = ReadOneTimeEvents(one_time_event_file)
        self.assertDictEqual(one_time_event_obj.eventsAt, {
            0: ['1:4,5,6,7,8,9'],
            1: ['0:1,2,3'],
            3: ['0:1,2,3']
        })

    def test_read_interactions(self):
        example_path = osp.join('tests', 'unit', 'Complete_Interaction_Space')
        config_filename = osp.join(example_path, 'config.txt')
        config_obj = ReadConfiguration(config_filename)
        agents_filename, interactions_files_list_filename, \
            events_files_list_filename, locations_filename, \
            one_time_event_file, \
            probabilistic_interactions_files_list_filename = config_obj.get_file_paths(example_path)

        interaction_files_list_of_list, event_files_list_of_list, \
            probabilistic_interaction_files_list_of_list = config_obj.get_file_names_list(
                                                                example_path, interactions_files_list_filename,
                                                                events_files_list_filename,
                                                                probabilistic_interactions_files_list_filename)

        agents_obj = ReadAgents(agents_filename, config_obj)

        for interaction_files_list in interaction_files_list_of_list:
            if interaction_files_list:
                interactions_filename = interaction_files_list[0]
                ReadInteractions(interactions_filename, config_obj, agents_obj)

        contacts_dict = {}
        for agent in agents_obj.agents.values():
            contacts_dict[agent.index] = []
            for contact_dict in agent.contact_list:
                contacts_dict[agent.index].append(
                    contact_dict['Interacting Agent Index'])

        target_dict = {
            '0': ['1'],
            '1': ['2', '2', '4'],
            '2': ['4', '3'],
            '3': ['4'],
            '4': ['5'],
            '5': [],
            '6': ['7'],
            '7': [],
            '8': ['9'],
            '9': []
        }
        self.assertDictEqual(contacts_dict, target_dict)

    def test_read_prob_interactions(self):
        example_path = osp.join('tests', 'unit', 'Complete_Interaction_Space')
        config_filename = osp.join(example_path, 'config.txt')
        config_obj = ReadConfiguration(config_filename)

        agents_filename, interactions_files_list_filename, \
            events_files_list_filename, locations_filename, \
            one_time_event_file, \
            probabilistic_interactions_files_list_filename = config_obj.get_file_paths(example_path)

        interaction_files_list_of_list, event_files_list_of_list, \
            probabilistic_interaction_files_list_of_list = config_obj.get_file_names_list(
                                                                example_path, interactions_files_list_filename,
                                                                events_files_list_filename,
                                                                probabilistic_interactions_files_list_filename)

        agents_obj = ReadAgents(agents_filename, config_obj)

        for probabilistic_interaction_files_list in probabilistic_interaction_files_list_of_list:
            if probabilistic_interaction_files_list:
                probabilistic_interactions_filename = probabilistic_interaction_files_list[
                    0]
                ReadProbabilisticInteractions(
                    probabilistic_interactions_filename, config_obj,
                    agents_obj)

        contacts_dict = {}
        for agent in agents_obj.agents.values():
            contacts_dict[agent.index] = []
            for contact_dict in agent.contact_list:
                contacts_dict[agent.index].append(
                    contact_dict['Interacting Agent Index'])

        target_dict = {
            '0': ['2'],
            '1': ['3', '5', '2'],
            '2': ['3', '5', '1', '0', '4', '6'],
            '3': ['5', '1', '2'],
            '4': ['5', '2', '6', '6', '8'],
            '5': ['3', '1', '2', '4'],
            '6': ['2', '4', '4'],
            '7': [],
            '8': ['4'],
            '9': []
        }

        self.assertDictEqual(contacts_dict, target_dict)

    def test_read_events(self):
        example_path = osp.join('tests', 'unit', 'Complete_Interaction_Space')
        config_filename = osp.join(example_path, 'config.txt')
        config_obj = ReadConfiguration(config_filename)
        agents_filename, interactions_files_list_filename, \
            events_files_list_filename, locations_filename, \
            one_time_event_file, \
            probabilistic_interactions_files_list_filename = config_obj.get_file_paths(example_path)

        interaction_files_list_of_list, event_files_list_of_list, \
            probabilistic_interaction_files_list_of_list = config_obj.get_file_names_list(
                                                                example_path, interactions_files_list_filename,
                                                                events_files_list_filename,
                                                                probabilistic_interactions_files_list_filename)

        agents_obj = ReadAgents(agents_filename, config_obj)
        locations_obj = ReadLocations(locations_filename, config_obj)

        for event_files_list in event_files_list_of_list:
            if event_files_list:
                events_filename = event_files_list[0]
                ReadEvents(events_filename, config_obj, locations_obj,
                           agents_obj)

        events_dict = {}
        for location in locations_obj.locations.values():
            events_dict[location.index] = []
            for event_dict in location.events:
                events_dict[location.index] = event_dict['Agents']
                events_dict[location.index].sort()

        self.assertListEqual(
            events_dict['0'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.assertListEqual(events_dict['1'], ['1', '3', '5', '7', '9'])
        self.assertListEqual(events_dict['2'], ['2', '4', '6', '8'])

    def test_read_one_time_events(self):
        example_path = osp.join('tests', 'unit', 'Complete_Interaction_Space')
        config_filename = osp.join(example_path, 'config.txt')
        config_obj = ReadConfiguration(config_filename)
        agents_filename, interactions_files_list_filename, \
            events_files_list_filename, locations_filename, \
            one_time_event_file, \
            probabilistic_interactions_files_list_filename = config_obj.get_file_paths(example_path)

        agents_obj = ReadAgents(agents_filename, config_obj)
        locations_obj = ReadLocations(locations_filename, config_obj)
        one_time_event_obj = ReadOneTimeEvents(one_time_event_file)

        def one_time_event_helper(time_step):
            one_time_event_obj.populate_one_time_events(
                config_obj, locations_obj, agents_obj, time_step)

            events_dict = {}
            for location in locations_obj.locations.values():
                events_dict[location.index] = []
                for event_dict in location.events:
                    events_dict[location.index] = event_dict['Agents']
                    events_dict[location.index].sort()

            return events_dict

        target_dict = {
            '0': [],
            '1': ['4', '5', '6', '7', '8', '9'],
            '2': [],
            '3': [],
            '4': []
        }
        self.assertDictEqual(one_time_event_helper(0), target_dict)
        self.assertDictEqual(one_time_event_helper(1),
                             one_time_event_helper(3))


if __name__ == '__main__':
    unittest.main()
