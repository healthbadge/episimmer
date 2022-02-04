import os.path as osp
import unittest

from episimmer.read_file import ReadConfiguration


class TestReadFile(unittest.TestCase):
    def test_read_config(self):
        print()
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


if __name__ == '__main__':
    unittest.main()
