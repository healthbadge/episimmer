import unittest
from src import Testing_Policy,Agent
import copy


class TestMachine(unittest.TestCase):
    def test_machine_register_single_testtube(self):
        machine = Testing_Policy.Machine('Test', 100, 0, 0, 0, 1)
        testtube = Testing_Policy.Testtube()
        machine.register_testtube(testtube)
        self.assertEqual(len(machine.testtubes),1)

    def test_machine_run_single_test(self):
        machine = Testing_Policy.Machine('Test', 100, 0, 0, 0, 1)
        testtube = Testing_Policy.Testtube()
        agent = Agent.Agent(state="Infected",info_dict={'Agent Index':0})
        testtube.register_agent(agent)
        machine.register_testtube(testtube)
        machine.run_single_test(testtube, infected_states=["Infected"])
        self.assertEqual(testtube.testtube_result,"Positive")

class TestPolicy(unittest.TestCase):
    def test_add_machine(self):
        TP = Testing_Policy.Test_Policy(lambda x:60)
        TP.add_machine('Test', 100, 0, 0, 0, 1, 1)
        self.assertEqual(len(TP.machine_list),1)
        self.assertEqual(TP.current_machines['Test'],{'parameters':[100, 0, 0, 0, 1],'number':1})


    def test_copy_agents(self):

        agent_list = [Agent.Agent(state="Infected",info_dict={'Agent Index':0})]
        agent_copy = copy.copy(agent_list)

        self.assertIsNot(agent_list,agent_copy)
        agent_copy[0].state = "Recovered"

        self.assertEqual(agent_list[0].state,"Recovered")

    def test_deep_copy_agents(self):

        agent_list = [Agent.Agent(state="Infected",info_dict={'Agent Index':0})]
        agent_copy = copy.deepcopy(agent_list)

        self.assertIsNot(agent_list,agent_copy)
        agent_copy[0].state = "Recovered"

        self.assertNotEqual(agent_list[0].state,"Recovered")


if __name__ == '__main__':
    unittest.main()
