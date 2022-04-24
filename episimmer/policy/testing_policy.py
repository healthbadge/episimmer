import copy
import json
import random
from collections import deque
from functools import partial
from typing import Callable, Deque, Dict, List, Union, ValuesView

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.model import BaseModel

from .base import AgentPolicy
from .contact_tracing_policy import CTPolicy


class TestResult():
    """
    Class for a Test Result.

    Args:
        result: Result of test for testtube
        agent: Instance of the :class:`~episimmer.agent.Agent` tested
        machine_name: Name of machine used for testing
        time_step: Time step agent tested
        machine_start_step: Time step machine started testing
        time_step_done: Time step machine completed test
        valid_period: Number of time steps the test is considered to be valid
    """
    def __init__(self, result: str, agent: Agent, machine_name: str,
                 time_step: int, machine_start_step: int, time_step_done: int,
                 valid_period: int):
        self.result: str = result
        self.agent: Agent = agent
        self.machine_name: str = machine_name
        self.time_step: int = time_step
        self.machine_start_step: int = machine_start_step
        self.time_step_done: int = time_step_done
        self.valid_period: int = valid_period

    def get_machine_name(self) -> str:
        """
        Returns the name of machine used for testing

        Returns:
            Name of machine used for testing
        """
        return self.machine_name

    def get_result(self) -> str:
        """
        Returns the result of test

        Returns:
            Result of test
        """
        return self.result

    def __repr__(self) -> str:
        """
        Shows the representation of the object as the string result

        Returns:
            The result of test in string format
        """
        return self.result


class TestTube():
    """
    Class for a Testtube.
    """
    def __init__(self):
        self.testtube_agent_dict: Dict[Agent, Dict[str, Union[str, int]]] = {}
        self.testtube_result: Union[str, None] = None
        self.in_machine: bool = False

    def register_agent(self, agent: Agent, time_step: int) -> None:
        """
        Testtube registering an agent.

        Args:
            agent: Instance of :class:`~episimmer.agent.Agent`
            time_step: Current time step
        """
        self.testtube_agent_dict[agent] = {
            'state': agent.state,
            'time_step': time_step
        }

    def get_num_agents(self) -> int:
        """
        Returns the number of agents in the testtube.

        Returns:
            Number of agents in testtube
        """
        return len(self.testtube_agent_dict)

    def set_result(self, result: str) -> None:
        """
        Sets the result of test - Positive or Negative.

        Args:
            result: Result of test
        """
        self.testtube_result = result

    def set_in_machine(self, bool_val: bool) -> None:
        """
        Sets the testtube to be in the machine.

        Args:
            bool_val: Boolean for in machine
        """
        if bool_val:
            self.in_machine = bool_val
        else:
            self.in_machine = bool_val
            self.testtube_agent_dict = {}
            self.testtube_result = None

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating whether testtube is empty.

        Returns:
            Boolean indicating whether testtube is empty
        """
        if len(self.testtube_agent_dict) == 0:
            return True

        return False

    def is_in_machine(self) -> bool:
        """
        Returns a boolean indicating whether testtube is in machine.

        Returns:
            Boolean indicating whether testtube in machine
        """
        return self.in_machine


class Machine():
    """
    Class for a Testing Machine.

    Args:
        machine_name: Name of machine
        cost: Cost for a single test in the machine
        false_positive_rate: False positive rate of the machine
        false_negative_rate: False negative rate of the machine
        turnaround_time: Time taken for a test result
        capacity: Capacity of the machine for tests
        valid_period: Number of time steps the test is considered to be valid
    """
    def __init__(self, machine_name: str, cost: int,
                 false_positive_rate: float, false_negative_rate: float,
                 turnaround_time: int, capacity: int, valid_period: int):
        self.machine_name: str = machine_name
        self.cost: int = cost
        self.false_positive_rate: float = false_positive_rate
        self.false_negative_rate: float = false_negative_rate
        self.true_positive_rate: float = 1 - self.false_negative_rate
        self.true_negative_rate: float = 1 - self.false_positive_rate
        self.turnaround_time: int = turnaround_time
        self.capacity: int = capacity
        self.valid_period: int = valid_period
        self.testtubes: List[TestTube] = []
        self.results: List[TestResult] = []
        self.available: bool = True
        self.start_step: Union[int, None] = None
        self.machine_cost: int = 0

    def is_running(self) -> bool:
        """
        Returns a boolean indicating whether machine is running.

        Returns:
            Boolean indicating whether machine is running
        """
        if not self.available:
            return True

        return False

    def is_full(self) -> bool:
        """
        Returns a boolean indicating whether machine is full.

        Returns:
            Boolean indicating whether machine is full
        """
        if len(self.testtubes) >= self.capacity:
            return True

        return False

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating whether machine is completely empty.

        Returns:
            Boolean indicating whether machine is completely empty
        """
        if len(self.testtubes) == 0:
            return True

        return False

    def has_empty_results(self) -> bool:
        """
        Returns a boolean indicating whether machine has no results.

        Returns:
            Boolean indicating whether machine has no results
        """
        if len(self.results) == 0:
            return True

        return False

    def reset_machine(self) -> None:
        """
        Resets the machine's list of testtubes, results and sets its availability to True.
        """
        self.testtubes = []
        self.results = []
        self.available = True

    def register_testtube(self, testtube: TestTube) -> None:
        """
        Registers a testtube to the machine. Since each testtube corresponds to a single test, the machine cost
        accumulates the saved cost value once.

        Args:
            testtube: Instance of :class:`TestTube`
        """
        testtube.set_in_machine(True)
        self.testtubes.append(testtube)
        self.machine_cost += self.cost

    def run_tests(self, infected_states: List[str], time_step: int) -> None:
        """
        Runs the tests for each testtube in the machine.

        Args:
            infected_states: Infected states of the disease model
            time_step: Current time step
        """
        self.available = False
        self.start_step = time_step

        for testtube in self.testtubes:
            self.run_single_test(testtube, infected_states)

    def run_single_test(self, testtube: TestTube,
                        infected_states: List[str]) -> None:
        """
        Runs a single test for a testtube in the machine and saves the result for that testtube.

        Args:
            testtube: Instance of :class:`TestTube`
            infected_states: Infected states of the disease model
        """
        result = 'Negative'

        for agent in testtube.testtube_agent_dict.keys():
            if (testtube.testtube_agent_dict[agent]['state']
                    in infected_states):
                result = 'Positive'
                break

        if result == 'Negative':
            if random.random() > self.true_negative_rate:
                result = 'Positive'
        else:
            if random.random() > self.true_positive_rate:
                result = 'Negative'

        testtube.set_result(result)

    def populate_machine_results(self, time_step: int) -> None:
        """
        Populates the machine with results for each testtube if the machine has completed running. It also
        removes the testtube from the machine.

        Args:
            time_step: Current time step
        """
        if self.run_completed(time_step):
            for testtube_with_result in self.testtubes:
                self.save_results(testtube_with_result, time_step)
                testtube_with_result.set_in_machine(False)

    def run_completed(self, time_step: int) -> bool:
        """
        Returns a boolean indicating whether machine has completed running tests.

        Returns:
            Boolean indicating whether machine has completed running tests
        """
        return time_step - self.start_step >= self.turnaround_time

    def save_results(self, testtube: TestTube, time_step: int) -> None:
        """
        Saves the results for a testtube in the results list.

        Args:
            testtube: Instance of :class:`TestTube`
            time_step: Current time step
        """
        for agent in testtube.testtube_agent_dict.keys():
            time_step_entered = testtube.testtube_agent_dict[agent][
                'time_step']
            result_obj = TestResult(testtube.testtube_result, agent,
                                    self.machine_name, time_step_entered,
                                    self.start_step, time_step,
                                    self.valid_period)
            self.results.append(result_obj)

    def get_results(self) -> List[TestResult]:
        """
        Returns the results saved in the results list

        Returns:
            Results saved in the results list
        """
        return self.results

    def get_machine_name(self) -> str:
        """
        Returns the name of machine

        Returns:
            Name of machine
        """
        return self.machine_name


class TestPolicy(AgentPolicy):
    """
    Class for implementing the testing policy.
    Inherits :class:`~episimmer.policy.base.AgentPolicy` class.

    Note that for disease control, we require locking down agents that are positive, thus we have included a
    lockdown policy in the examples below.

    An example of a GeneratePolicy.py file illustrating normally testing random agents (and locking down positively
    tested agents) is given below.

    .. code-block:: python
            :linenos:

            from episimmer.policy import lockdown_policy, testing_policy

            def generate_policy():
                policy_list=[]

                Normal_Test = testing_policy.TestPolicy(lambda x:60)
                Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
                Normal_Test.set_register_agent_testtube_func(Normal_Test.random_testing(1, 1))
                policy_list.append(Normal_Test)

                ATP = lockdown_policy.TestingBasedLockdown(lambda x:True,10)
                policy_list.append(ATP)

                return policy_list

    An example of a GeneratePolicy.py file illustrating pool testing random agents with (NAPT, NTPA) = (3,2) (and
    locking down positively tested agents) is given below

    .. code-block:: python
            :linenos:

            from episimmer.policy import lockdown_policy, testing_policy

            def generate_policy():
                policy_list=[]

                Normal_Test = testing_policy.TestPolicy(lambda x:60)
                Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
                Normal_Test.set_register_agent_testtube_func(Normal_Test.random_testing(3, 2))
                policy_list.append(Normal_Test)

                ATP = lockdown_policy.TestingBasedLockdown(lambda x:True,10)
                policy_list.append(ATP)

                return policy_list

    An example of a GeneratePolicy.py file illustrating normally testing random agents along with testing their contacts
    in case they are positive (and locking down positively tested agents) is given below. Here, we need to also include
    a contact tracing policy to save contacts each time step.

    .. code-block:: python
            :linenos:

            from episimmer.policy import (contact_tracing_policy, lockdown_policy,
                                          testing_policy)


            def generate_policy():
                policy_list=[]
                Normal_Test1 = testing_policy.TestPolicy(lambda x: 2)
                Normal_Test1.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2, 2)
                Normal_Test1.set_register_agent_testtube_func(Normal_Test1.random_testing(1, 1))
                policy_list.append(Normal_Test1)

                Normal_Test2 = testing_policy.TestPolicy(lambda x: 2)
                Normal_Test2.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2, 2)
                Normal_Test2.set_register_agent_testtube_func(Normal_Test2.contact_testing(1, 1))
                policy_list.append(Normal_Test2)

                CT_object = contact_tracing_policy.CTPolicy(7)
                policy_list.append(CT_object)

                Lockdown_object = lockdown_policy.TestingBasedLockdown(lambda x:1, 2)
                policy_list.append(Lockdown_object)

                return policy_list


    Args:
        agents_per_step_fn: User-defined function to specify the number of agents to test per time step
    """
    def __init__(self, agents_per_step_fn: Callable):
        super().__init__('Testing')
        self.register_agent_testtube_func: Union[Callable, None] = None
        self.cur_testtubes: Union[List[TestTube], None] = None
        self.ready_queue: Deque[TestTube] = deque()
        self.machine_list: List[Machine] = []
        self.statistics: Dict[int, Dict] = {}
        self.current_machines: Dict[str, Dict[str, Union[int, float]]] = {}
        self.total_cost: int = 0
        self.num_agents_to_test: Union[int, None] = None

        assert callable(agents_per_step_fn)
        self.agents_per_step_fn: Callable = agents_per_step_fn

    def reset(self,
              agents: Union[ValuesView[Agent], None] = None,
              locations: Union[ValuesView[Location], None] = None,
              model: Union[BaseModel, None] = None,
              policy_index: Union[int, None] = None) -> None:
        """
        Resets statistics, ready queue and all the machines for a new world.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        self.statistics = {}
        self.ready_queue = deque()
        for machine in self.machine_list:
            machine.machine_cost = 0
            machine.testtubes = []
            machine.results = []
            machine.available = True
            machine.start_step = None

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: BaseModel,
                     policy_index: Union[int, None] = None) -> None:
        """
        Executes testing policy for the given time step.

        Args:
            time_step: Time step in which the policy is enacted
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        self.new_time_step(time_step)
        self.populate_results_in_machine(time_step)
        self.release_results(time_step)
        self.register_agent_testtube_func(agents, time_step, model)
        self.add_partial_to_ready_queue()
        self.register_testtubes_to_machines()
        self.run_tests(model, time_step)
        self.zero_turnaround_time_func(time_step)
        self.end_time_step(time_step)

    def zero_turnaround_time_func(self, time_step: int) -> None:
        """
        When turnaround time = 0, results are populated in the same time step. This function handles
        that scenario.

        Args:
            time_step: Current time step
        """
        for machine in self.machine_list:
            if not machine.is_empty() and machine.run_completed(time_step):
                self.populate_results_in_machine(time_step)
                self.release_results(time_step)
                break

    def add_machine(self,
                    machine_name: str,
                    cost: int,
                    false_positive_rate: float,
                    false_negative_rate: float,
                    turnaround_time: int,
                    capacity: int,
                    valid_period: int,
                    num: int = 1) -> None:
        """
        This function enables the user to add a machine in the ``Generate_policy.py`` file. A machine must be defined as
        it performs the testing procedure on testtubes. It defines parameters of the testing policy.

        .. code-block:: python
            :linenos:

            Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2, 2)

        Args:
            machine_name: Name of machine
            cost: Cost for a single test in the machine
            false_positive_rate: False positive rate of the machine
            false_negative_rate: False negative rate of the machine
            turnaround_time: Time taken for a test result
            capacity: Capacity of the machine for tests
            valid_period: Number of time steps the test is considered to be valid
            num: Number of instances of this machine
        """
        if machine_name in self.current_machines.keys():
            if ([
                    cost, false_positive_rate, false_negative_rate,
                    turnaround_time, capacity
            ] == self.current_machines[machine_name]['parameters']):
                self.current_machines[machine_name]['number'] += num

                for i in range(num):
                    self.machine_list.append(
                        Machine(machine_name, cost, false_positive_rate,
                                false_negative_rate, turnaround_time, capacity,
                                valid_period))

            else:
                raise Exception(
                    'Error! Machine name with different parameters already exists'
                )
        else:
            self.current_machines[machine_name] = {
                'parameters': [
                    cost, false_positive_rate, false_negative_rate,
                    turnaround_time, capacity, valid_period
                ],
                'number':
                num
            }

            for i in range(num):
                self.machine_list.append(
                    Machine(machine_name, cost, false_positive_rate,
                            false_negative_rate, turnaround_time, capacity,
                            valid_period))

    def set_register_agent_testtube_func(self, fn: Callable) -> None:
        """
        Registers the function that determines how agents are mapped to testtubes.
        The user must specify one of the following functions in the ``Generate_policy.py`` file.

        * :meth:`~random_testing`
        * :meth:`~contact_testing`

        The example below illustrates the use of both testing methods.

        .. code-block:: python
            :linenos:

            Normal_Test1.set_register_agent_testtube_func(Normal_Test1.random_testing(1, 1))
            Normal_Test2.set_register_agent_testtube_func(Normal_Test2.contact_testing(1, 1))

        Args:
            fn: Function that determines the type of testing to be performed
        """
        self.register_agent_testtube_func = fn

    def initialize_statistics_logs(self, time_step: int) -> None:
        """
        Initializes statistics dictionary. It contains global information of all tests.

        Args:
            time_step: Current time step
        """
        self.statistics[time_step] = {
            'Total Tests': 0,
            'Total Positive Results': 0,
            'Total Negative Results': 0,
            'Total Agents Tested': 0
        }

        for machine_name in self.current_machines.keys():
            self.statistics[time_step][machine_name] = {
                'Number of Tests': 0,
                'Number of Positive Results': 0,
                'Number of Negative Results': 0,
                'Number of Agents Tested': 0
            }

    def initialize_process_logs(self, time_step: int) -> None:
        """
        Initializes statistics dictionary for each machine. It contains machine-level information.

        Args:
            time_step: Current time step
        """
        self.statistics[time_step]['Process'] = {}
        for machine_name in self.current_machines.keys():
            self.statistics[time_step]['Process'][machine_name] = {}

        for machine in self.machine_list:
            machine_name = machine.get_machine_name()
            self.statistics[time_step]['Process'][machine_name][
                machine.__str__()] = {
                    'Running Status': 'On Standby',
                    'Filled Status': 'Empty'
                }

        self.statistics[time_step]['Process'][
            'All Testubes filled'] = 'Default'
        self.statistics[time_step]['Process'][
            'All Testubes in machine'] = 'Default'
        self.statistics[time_step]['Process'][
            'All Machines running'] = 'Default'
        self.statistics[time_step]['Process']['Ready Queue Length'] = -1

    def new_time_step(self, time_step: int) -> None:
        """
        Initializes statistics of the testing policy.
        Resets the current test tubes and the number of agents to test in the current time step.

        Args:
            time_step: Current time step
        """
        self.initialize_statistics_logs(time_step)
        self.initialize_process_logs(time_step)
        self.cur_testtubes = []
        self.num_agents_to_test = self.agents_per_step_fn(time_step)

    def populate_test_queue(self, agents_to_test: List[Agent],
                            num_agents_per_testtube: int,
                            num_testtubes_per_agent: int,
                            time_step: int) -> None:
        r"""
        Populates the testing ready queue with fully filled testtubes containing agent samples. This method can handle
        both regular testing and pool testing using the parameters :math:`NAPT` (number of agents per testtube) and
        :math:`NTPA` (number of testtubes per agent) passed from the function defining the mapping from agents to
        testtubes. The number of testtubes :math:`N_T` required follow the formula -

        .. math::
            N_T = \lfloor \frac{NTPA \times N_A + NAPT - 1}{NAPT} \rfloor

        where :math:`N_A` denotes the number of agents to test.

        Args:
            agents_to_test: List of :class:`~episimmer.agent.Agent` objects ready for testing
            num_agents_per_testtube: Number of agents per testtube
            num_testtubes_per_agent: Number of testtubes per agent
            time_step: Current time step
        """
        num_testtubes = int(
            (num_testtubes_per_agent * self.num_agents_to_test +
             num_agents_per_testtube - 1) / num_agents_per_testtube)
        for _ in range(num_testtubes):
            testtube = TestTube()
            self.cur_testtubes.append(testtube)

        # Assign agents to testtubes and populate ready queue
        for agent in agents_to_test:
            if len(self.cur_testtubes) > 0:
                cur_list = random.sample(
                    self.cur_testtubes,
                    min(num_testtubes_per_agent, len(self.cur_testtubes)))

                for testtube in cur_list:
                    testtube.register_agent(agent, time_step)

                    if testtube.get_num_agents() >= num_agents_per_testtube:
                        self.ready_queue.append(testtube)
                        self.cur_testtubes.remove(testtube)
            else:
                break

    def full_random_testing(self, num_agents_per_testtube: int,
                            num_testtubes_per_agent: int,
                            only_symptomatic: bool, attribute: Union[str,
                                                                     None],
                            value_list: List[str], agents: Dict[str, Agent],
                            time_step: int, model: BaseModel) -> None:
        """
        Agents are first selected for testing and added to a list based on the number of agents to test in the
        current time step, agent parameters (if given) and symptomatic states (if set to True). Then, the test ready
        queue is populated.

        Args:
            num_agents_per_testtube: Number of agents per testtube (NAPT)
            num_testtubes_per_agent: Number of testtubes per agent (NTPA)
            only_symptomatic: Choose whether to only select symptomatic agents or not (If set to True, you must
                              have symptomatic states set in ``UserModel.py``)
            attribute: Parameter (attribute) type of agents
            value_list: List of attribute values of agents
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            time_step: Current time step
            model: Disease model specified by the user

        """
        agents_copy = copy.copy(list(agents.values()))
        random.shuffle(agents_copy)

        # Get agents for test
        agents_to_test = []
        for agent in agents_copy:

            if len(agents_to_test) == self.num_agents_to_test:
                break

            elif attribute is None or agent.info[attribute] in value_list:
                if not only_symptomatic or agent.state in model.symptomatic_states:
                    if TestPolicy.is_agent_test_ready(agent, time_step):
                        agents_to_test.append(agent)

        self.populate_test_queue(agents_to_test, num_agents_per_testtube,
                                 num_testtubes_per_agent, time_step)

    def random_testing(self,
                       num_agents_per_testtube: int = 1,
                       num_testtubes_per_agent: int = 1,
                       only_symptomatic: bool = False,
                       attribute: Union[str, None] = None,
                       value_list: List[str] = []) -> Callable:
        """
        This function can be used by the user in ``Generate_policy.py`` to test random agents. This
        function can handle normal or pool testing. Normal testing refers to testing a single agent
        once i.e. A single agent's sample present in a single testtube. Pool testing refers to having multiple agents
        in a testtube defined by the num_agents_per_testtube parameter and multiple testtubes for an agent defined by
        the num_testtubes_per_agent parameter. If symptomatic states are defined in the disease model in the
        ``UserModel.py`` file, then you may also only test symptomatic agents. This function returns a partial
        function of :meth:`~full_random_testing`.


        An example of a GeneratePolicy.py file illustrating normally testing and pool testing random agents
        (and locking down positively tested agents) is given below.

        .. code-block:: python
                :linenos:
                :emphasize-lines: 8, 13

                from episimmer.policy import lockdown_policy, testing_policy

                def generate_policy():
                    policy_list=[]

                    Normal_Test = testing_policy.TestPolicy(lambda x:60)
                    Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
                    Normal_Test.set_register_agent_testtube_func(Normal_Test.random_testing(1, 1))
                    policy_list.append(Normal_Test)

                    Pool_Testing = testing_policy.TestPolicy(lambda x:150)
                    Pool_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
                    Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_testing(5,2))
                    policy_list.append(Pool_Testing)

                    ATP = lockdown_policy.TestingBasedLockdown(lambda x:True,10)
                    policy_list.append(ATP)

                    return policy_list

        Args:
            num_agents_per_testtube: Number of agents per testtube (NAPT)
            num_testtubes_per_agent: Number of testtubes per agent (NAPT)
            only_symptomatic: Choose whether to only select symptomatic agents or not (If set to True, you must have
                              symptomatic states set in ``UserModel.py``)
            attribute: Parameter (attribute) type of agents
            value_list: List of attribute values of agents

        Returns:
            Partial function of :meth:`~full_random_testing`
        """
        return partial(self.full_random_testing, num_agents_per_testtube,
                       num_testtubes_per_agent, only_symptomatic, attribute,
                       value_list)

    def full_contact_testing(self, num_agents_per_testtube: int,
                             num_testtubes_per_agent: int,
                             attribute: Union[str, None],
                             value_list: List[str], agents: Dict[str, Agent],
                             time_step: int, model: BaseModel) -> None:
        """
        Agents are first checked for positive history of testing and then contacts of the positive agents are selected
        for testing. They are added to a list based on the number of agents to test in the
        current time step, agent parameters (if given) and symptomatic states (if set to True). Then, the test ready
        queue is populated.

        Args:
            num_agents_per_testtube: Number of agents per testtube (NAPT)
            num_testtubes_per_agent: Number of testtubes per agent (NTPA)
            attribute: Parameter (attribute) type of agents
            value_list: List of attribute values of agents
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            time_step: Current time step
            model: Disease model specified by the user

        """
        agents_copy = copy.copy(list(agents.values()))
        random.shuffle(agents_copy)

        # Get agents for test
        agents_to_test = []
        for agent in agents_copy:

            if len(agents_to_test) == self.num_agents_to_test:
                break

            elif attribute is None or agent.info[attribute] in value_list:
                if TestPolicy.get_agent_test_result(agent,
                                                    time_step) == 'Positive':
                    contacts = []
                    policy_index_list = CTPolicy.get_policy_index_list(agent)
                    for policy_index in policy_index_list:
                        contacts += CTPolicy.get_contact_list(
                            agent, policy_index)
                        contacts = list(dict.fromkeys(contacts))
                    valid_contacts = [
                        agents[c] for c in contacts
                        if TestPolicy.is_agent_test_ready(
                            agents[c], time_step)
                    ]
                    capacity = self.num_agents_to_test - len(agents_to_test)
                    if len(valid_contacts) <= capacity:
                        agents_to_test += valid_contacts
                    else:
                        agents_to_test += valid_contacts[:capacity]

        self.populate_test_queue(agents_to_test, num_agents_per_testtube,
                                 num_testtubes_per_agent, time_step)

    def contact_testing(self,
                        num_agents_per_testtube: int = 1,
                        num_testtubes_per_agent: int = 1,
                        attribute: Union[str, None] = None,
                        value_list: List[str] = []) -> Callable:
        """
        This function can be used by the user in ``Generate_policy.py`` to test contacts of positive agents. This
        function can handle normal or pool testing. Normal testing refers to testing a single agent
        once i.e. A single agent's sample present in a single testtube. Pool testing refers to having multiple agents
        in a testtube defined by the num_agents_per_testtube parameter and multiple testtubes for an agent defined by
        the num_testtubes_per_agent parameter. This function returns a partial
        function of :meth:`~full_contact_testing`.

        An example of a GeneratePolicy.py file illustrating normally testing random agents along with testing their
        contacts in case they are positive (and locking down positively tested agents) is given below. Here, we need
        to also include a contact tracing policy to save contacts each time step.

        .. code-block:: python
                :linenos:
                :emphasize-lines: 14

                from episimmer.policy import (contact_tracing_policy, lockdown_policy,
                                              testing_policy)


                def generate_policy():
                    policy_list=[]
                    Normal_Test1 = testing_policy.TestPolicy(lambda x: 2)
                    Normal_Test1.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2, 2)
                    Normal_Test1.set_register_agent_testtube_func(Normal_Test1.random_testing(1, 1))
                    policy_list.append(Normal_Test1)

                    Normal_Test2 = testing_policy.TestPolicy(lambda x: 2)
                    Normal_Test2.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2, 2)
                    Normal_Test2.set_register_agent_testtube_func(Normal_Test2.contact_testing(1, 1))
                    policy_list.append(Normal_Test2)

                    CT_object = contact_tracing_policy.CTPolicy(7)
                    policy_list.append(CT_object)

                    Lockdown_object = lockdown_policy.TestingBasedLockdown(lambda x:1, 2)
                    policy_list.append(Lockdown_object)

                    return policy_list

        Args:
            num_agents_per_testtube: Number of agents per testtube (NAPT)
            num_testtubes_per_agent: Number of testtubes per agent (NAPT)
            attribute: Parameter (attribute) type of agents
            value_list: List of attribute values of agents

        Returns:
            Partial function of :meth:`~full_contact_testing`
        """
        return partial(self.full_contact_testing, num_agents_per_testtube,
                       num_testtubes_per_agent, attribute, value_list)

    def add_partial_to_ready_queue(self) -> None:
        """
        Since the :meth:`~populate_test_queue` method only populates fully filled testtubes, this function adds
        partially filled testtubes to the test ready queue.
        """
        for testtube in self.cur_testtubes:
            if not testtube.is_empty():
                self.ready_queue.append(testtube)

    def register_testtubes_to_machines(self) -> None:
        """
        Registers the testtubes to all empty/partially filled non-running machines defined by user.
        """
        for machine in self.machine_list:
            while self.ready_queue:
                if machine.is_running() or machine.is_full():
                    break

                else:
                    testtube = self.ready_queue.popleft()
                    machine.register_testtube(testtube)

    def run_tests(self, model: BaseModel, time_step: int) -> None:
        """
        Runs the tests for all non-empty non-running machines.

        Args:
            model: Disease model specified by the user
            time_step: Current time step
        """
        for machine in self.machine_list:
            if not machine.is_empty() and not machine.is_running():
                machine.run_tests(model.infected_states, time_step)

    def populate_results_in_machine(self, time_step: int) -> None:
        """
        Populates the results of each test in the machines (if test is complete).

        Args:
            time_step: Current time step
        """
        for machine in self.machine_list:
            if machine.is_running():
                machine.populate_machine_results(time_step)

    def release_results_to_agents(self, results: List[TestResult]) -> None:
        """
        Results are released to the agents and the policy history of the agent is updated.

        Args:
            results: Collection of :class:`TestResult` objects
        """
        for result_obj in results:
            self.update_agent_policy_history(result_obj.agent, result_obj)

    def release_results_to_policy(self, results: List[TestResult],
                                  time_step: int) -> None:
        """
        Results are released to the policy i.e. stored in the statistics dictionary.

        Args:
            results: Collection of :class:`TestResult` objects
            time_step: Current time step
        """
        for result_obj in results:
            machine_name = result_obj.get_machine_name()
            self.statistics[time_step][machine_name]['Number of Tests'] += 1
            self.statistics[time_step]['Total Tests'] += 1

            if result_obj.get_result() == 'Positive':
                self.statistics[time_step][machine_name][
                    'Number of Positive Results'] += 1
                self.statistics[time_step]['Total Positive Results'] += 1

            elif result_obj.get_result() == 'Negative':
                self.statistics[time_step][machine_name][
                    'Number of Negative Results'] += 1
                self.statistics[time_step]['Total Negative Results'] += 1

            self.statistics[time_step][machine_name][
                'Number of Agents Tested'] += 1
            self.statistics[time_step]['Total Agents Tested'] += 1

    def release_results(self, time_step: int) -> None:
        """
        Results are released to the agents and policy once the machine has been populated with results. The machine is
        then reset.

        Args:
            time_step: Current time step
        """
        results = []
        for machine in self.machine_list:
            if not machine.has_empty_results():
                results += machine.get_results()
                machine.reset_machine()

        self.release_results_to_agents(results)
        self.release_results_to_policy(results, time_step)

    def update_process_logs(self, time_step: int) -> None:
        """
        Machine-level logging done here

        Args:
            time_step: Current time step
        """
        for machine in self.machine_list:
            machine_name = machine.get_machine_name()

            if machine.is_running():
                self.statistics[time_step]['Process'][machine_name][
                    machine.__str__()]['Running Status'] = 'Running'
            else:
                self.statistics[time_step]['Process'][machine_name][
                    machine.__str__()]['Running Status'] = 'On Standby'

            if machine.is_empty():
                self.statistics[time_step]['Process'][machine_name][
                    machine.__str__()]['Filled Status'] = 'Empty'
            elif machine.is_full():
                self.statistics[time_step]['Process'][machine_name][
                    machine.__str__()]['Filled Status'] = 'Completely Filled'
            else:
                self.statistics[time_step]['Process'][machine_name][
                    machine.__str__()]['Filled Status'] = 'Partly filled'

        all_testtubes_filled = True
        all_testtubes_in_machines = True
        all_machines_running = True

        for testtube in self.cur_testtubes:
            if testtube.is_empty():
                all_testtubes_filled = False
                break

        if self.ready_queue:
            all_testtubes_in_machines = False

        for machine in self.machine_list:
            if not machine.is_running():
                all_machines_running = False
                break

        self.statistics[time_step]['Process'][
            'All Testubes filled'] = all_testtubes_filled
        self.statistics[time_step]['Process'][
            'All Machines running'] = all_machines_running
        self.statistics[time_step]['Process'][
            'All Testubes in machine'] = all_testtubes_in_machines
        self.statistics[time_step]['Process']['Ready Queue Length'] = len(
            self.ready_queue)

    def end_time_step(self, time_step: int) -> None:
        """
        At the end of the time step, process logs are updated and stored as a json.

        Args:
            time_step: Current time step
        """
        self.update_process_logs(time_step)
        with open('testing_stats.json', 'w') as outfile:
            json.dump(self.statistics, outfile, indent=4)

    @staticmethod
    def get_accumulated_test_result(history: List[TestResult],
                                    last_time_step: int) -> str:
        """
        Method to get the most recent test result of an agent. In the case of pool
        testing, if even one of the pool tests return negative, he is a negatively tested
        agent, otherwise, if all pool tests return positive, he is a positively tested agent.

        Args:
            history: Test history of the agent
            last_time_step: Most recent time step in which agent was tested

        Returns:
            A string either "Positive" or "Negative" representing the most recent test result of the agent
        """
        index = len(history) - 1
        while index >= 0 and history[index].time_step == last_time_step:
            if history[index].result == 'Negative':
                return 'Negative'
            index -= 1
        return 'Positive'

    @staticmethod
    def get_agent_test_result(agent: Agent,
                              time_step: int) -> Union[str, None]:
        """
        Returns the most recent test result of an agent (if it exists).

        Args:
            agent: Current Agent
            time_step: Current time step

        Returns:
            A string either "Positive" or "Negative" representing the most recent test result of the agent. None if no
            tests done for the agent.
        """
        history = agent.get_policy_history('Testing')
        if len(history):
            last_time_step = history[-1].time_step
            validity_period = history[-1].valid_period
            if time_step - last_time_step < validity_period:
                result = TestPolicy.get_accumulated_test_result(
                    history, last_time_step)
                return result
        return None

    @staticmethod
    def is_agent_test_ready(agent: Agent, time_step: int) -> bool:
        """
        Returns a boolean representing whether an agent can test. If the agent has tested before, he can only test
        once the validity of the latest test has expired.

        Args:
            agent: Current Agent
            time_step: Current time step

        Returns:
            A boolean representing agent's ability to test
        """
        if TestPolicy.get_agent_test_result(agent, time_step) is None:
            return True

        return False
