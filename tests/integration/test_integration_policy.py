import unittest
import os.path as osp
from src.Main import *
import random

class TestIntegrationPolicy(unittest.TestCase):

    def get_stats(self, example_path):
        config_filename = get_config_path(example_path)

        config_obj=ReadFile.ReadConfiguration(config_filename)

        agents_filename, interactions_FilesList_filename,\
        events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
        interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

        model = get_model(example_path)
        policy_list, event_restriction_fn=get_policy(example_path)

        world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
        tdict, agents_obj, locations_obj = world_obj.one_world()
        return tdict, agents_obj, locations_obj

    def test_agent(self):
        example_path = osp.join('tests','integration','fixtures','Example_Single_Agent_Testing_Policy')
        tdict, agents_obj, locations_obj = self.get_stats(example_path)

        self.assertEqual(len(agents_obj.agents['0'].get_policy_history('Testing')),30)


    def test_three_agents(self):
        example_path = osp.join('tests','integration','fixtures','Example_Three_Agents_Group_Testing_Policy')
        tdict, agents_obj, locations_obj = self.get_stats(example_path)

        self.assertEqual((len(agents_obj.agents)),3)
        self.assertEqual(len(agents_obj.agents['0'].get_policy_history('Testing')),60) # 3 x 2/3 = 2 ; 2 x 30 = 60


if __name__ == '__main__':
    unittest.main()
