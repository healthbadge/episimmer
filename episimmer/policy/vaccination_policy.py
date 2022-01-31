import copy
import random
from functools import partial
from typing import Callable, Dict, List, Union, ValuesView

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.model import BaseModel

from .base import AgentPolicy


class VaccineResult():
    """
    Stores the information regarding the result of a vaccination.

    Args:
        vaccine_name: Name of the vaccine used
        agent: Agent that was vaccinated
        result: Vaccination result (Successful or Unsuccessful)
        time_step: Time step when the vaccination was done
        efficacy: Efficacy of the vaccine administered to the agent
        decay_days: Number of days of protection offered by the vaccine
        current_dose: The dose of the vaccine administered to the agent
    """
    def __init__(self, vaccine_name: str, agent: Agent, result: str,
                 time_step: int, efficacy: float, decay_days: int,
                 current_dose: int):
        self.vaccine_name: str = vaccine_name
        self.agent: Agent = agent
        self.result: str = result
        self.time_stamp: int = time_step
        self.protection: int = decay_days
        self.current_dose: int = current_dose


class VaccineType():
    """
    Class for Vaccine.

    Args:
        name: Vaccine name
        cost: Cost of the vaccine
        decay: Number of days of protection offered by the vaccine, a list of each dose in case of multi-dose vaccine
        efficacy: Efficacy of the vaccine
        dosage: Number of doses of the vaccine, applies only for multi-dose vaccine
        interval: List specifying minimum days to pass before the administration of the next dose, for each dose of a multi-dose vaccine
    """
    def __init__(self,
                 name: str,
                 cost: int,
                 decay: Union[List[int], int],
                 efficacy: float,
                 dosage: Union[int, None] = None,
                 interval: Union[List[int], None] = None):

        self.vaccine_name: str = name
        self.vaccine_cost: int = cost
        self.decay_days: Union[List[int], int] = decay
        self.efficacy: float = efficacy
        self.dosage: Union[int, None] = dosage
        self.interval: Union[List[int], None] = interval

    def vaccinate(self,
                  agent: Agent,
                  time_step: int,
                  dose: int = 1) -> VaccineResult:
        """
        Administers the specified dose of the current vaccine to the agent.
        Updates the protection days according to the dose administered.

        Args:
            agent: Agent to vaccinate
            time_step: Time step when the vaccination is performed
            dose: The dose of the vaccine to be administered to the agent

        Returns:
            Result object of vaccination
        """
        result = agent.get_policy_history(
            'Vaccination')[-1].result if dose > 1 else self.inject_agent(agent)
        if result == 'Successful':
            decay_days = self.decay_days[dose -
                                         1] if self.dosage else self.decay_days
        else:
            decay_days = 0
        result_obj = VaccineResult(self.vaccine_name, agent, result, time_step,
                                   self.efficacy, decay_days, dose)

        return result_obj

    def inject_agent(self, agent: Agent) -> str:
        """
        Applies the current vaccine to the agent and returns the result based on its efficacy.

        Args:
            agent: Agent to vaccinate

        Returns:
            Result of vaccination (Successful or Unsuccessful)
        """
        if (random.random() < self.efficacy):
            return 'Successful'
        else:
            return 'Unsuccessful'


class VaccinationPolicy(AgentPolicy):
    """
    Class for implementing the vaccination policy.
    Inherits :class:`~episimmer.policy.base.AgentPolicy` class.

    Args:
        agents_per_step_fn: User-defined function to specify the number of agents to vaccinate per time step
    """
    def __init__(self, agents_per_step_fn: Union[Callable, None] = None):
        super().__init__()

        self.num_agents_to_vaccinate: int = 0
        self.results: List[VaccineResult] = []
        self.policy_type: str = 'Vaccination'
        self.available_vaccines: Dict[str, Dict[str,
                                                Union[int, float, List[int],
                                                      str]]] = {}
        self.vaccines: List[VaccineType] = []
        self.statistics: Dict[str, Dict[str, List[int]]] = {}
        self.statistics_total: Dict[str, List[int]] = {
            'Total Vaccination': [],
            'Total Successful': [],
            'Total Unsuccessful': []
        }
        self.registered_agent_vaccine_func: Union[Callable, None] = None
        assert callable(agents_per_step_fn)
        self.agents_per_step_fn: Union[Callable, None] = agents_per_step_fn

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None] = None,
                     policy_index: int = None) -> None:
        """
        Executes vaccination policy for the given time step.

        Args:
            time_step: Time step in which the policy is enacted
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies.
        """
        self.newday(time_step)
        self.set_protection(agents.values())
        self.registered_agent_vaccine_func(agents.values(), time_step)
        self.populate_results()
        self.restrict_agents(agents.values())
        self.get_stats()

    def newday(self, time_step: int) -> None:
        """
        Creates a list in which vaccine objects are added according to the user’s specification.
        Resets the results of the policy enacted in previous time step and the number of agents to vaccinate in the
        current time step.

        Args:
            time_step: Current time step
        """
        self.vaccines = []
        self.results = []
        self.num_agents_to_vaccinate = self.agents_per_step_fn(time_step)

        for name, vaccine in self.available_vaccines.items():
            for i in range(int(vaccine['count'])):
                vaccine_obj = VaccineType(name, vaccine['cost'],
                                          vaccine['decay'],
                                          vaccine['efficacy'],
                                          vaccine.get('dose', 0),
                                          vaccine.get('interval', []))
                self.vaccines.append(vaccine_obj)

    def set_register_agent_vaccine_func(self, func: Callable) -> None:
        """
        Registers the function that determines the type of vaccination to be performed.
        The user must specify one of the following functions

        * :meth:`~random_vaccination`

        * :meth:`~multi_dose_vaccination`

        Args:
            func: Function that determines the type of vaccination to be performed
        """
        self.registered_agent_vaccine_func = func

    def random_vaccination(self,
                           parameter: Union[str, None] = None,
                           value_list: List[str] = []) -> Callable:
        """
        This function can be used by the user in ``Generate_policy.py`` to specify randomized vaccination to be performed for the agents.
        This function returns a partial function of :meth:`~full_random_vaccination`.

        Args:
            parameter: Parameter (attribute) type of agents
            value_list: List of attribute values of agents

        Returns:
            Partial function of :meth:`~full_random_vaccination`
        """
        assert isinstance(value_list, list)
        return partial(self.full_random_vaccination,
                       parameter=parameter,
                       value_list=value_list)

    def full_random_vaccination(self, agents: ValuesView[Agent],
                                time_step: int, parameter: Union[str, None],
                                value_list: List[str]) -> None:
        """
        If the number of agents vaccinated is less than the maximum number of agents to vaccinate per time step,
        for every unvaccinated agent this function randomly chooses a vaccine from the list of vaccines and performs
        vaccination on the agent. This function is valid only for single dose vaccines.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            time_step: Current time step
            parameter: Parameter (attribute) of agents
            value_list: List of attribute values of agents
        """
        agents_copy = copy.copy(list(agents))
        random.shuffle(agents_copy)
        curr_agents_to_vaccinate = self.num_agents_to_vaccinate

        for agent in agents_copy:
            if curr_agents_to_vaccinate <= 0:
                break

            if parameter is None or agent.info[parameter] in value_list:
                if agent.get_policy_state(
                        'Vaccination') is None and self.vaccines:
                    current_vaccine = random.choice(self.vaccines)
                    result = current_vaccine.vaccinate(agent, time_step)
                    self.results.append(result)
                    self.vaccines.remove(current_vaccine)
                    curr_agents_to_vaccinate -= 1

    def multi_dose_vaccination(self,
                               parameter: Union[str, None] = None,
                               value_list: List[str] = []) -> Callable:
        """
        This function can be used by the user in ``Generate_policy.py`` to specify multi-dose vaccination to be performed for the agents.
        This function returns a partial function of :meth:`~full_multi_dose_vaccination`.

        Args:
            parameter: Parameter (attribute) of agents
            value_list: List of attribute values of agents

        Returns:
            Partial function of :meth:`~full_multi_dose_vaccination`
        """
        return partial(self.full_multi_dose_vaccination,
                       parameter=parameter,
                       value_list=value_list)

    def full_multi_dose_vaccination(self, agents: ValuesView[Agent],
                                    time_step: int, parameter: Union[str,
                                                                     None],
                                    value_list: List[str]) -> None:
        """
        If the number of agents vaccinated is less than the maximum number of agents to vaccinate per time step,
        for every unvaccinated agent this function randomly chooses a vaccine from the list of vaccines and performs
        vaccination on the agent, and for every vaccinated agent if it is time for next dose, the next dose of the same vaccine
        is vaccinated for the agent.
        This function is valid only for multi dose vaccines.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            time_step: Current time step
            parameter: Parameter (attribute) of agents
            value_list: List of attribute values of agents
        """
        agents_copy = copy.copy(list(agents))
        random.shuffle(agents_copy)
        curr_agents_to_vaccinate = self.num_agents_to_vaccinate

        for agent in agents_copy:
            if curr_agents_to_vaccinate <= 0:
                break

            if parameter is None or agent.info[parameter] in value_list:
                history = self.get_agent_policy_history(agent)
                lh = history[-1] if history else None

                if agent.get_policy_state(
                        'Vaccination') is None and self.vaccines:
                    current_vaccine = random.choice(self.vaccines)
                    result = current_vaccine.vaccinate(agent, time_step)
                    self.results.append(result)
                    self.vaccines.remove(current_vaccine)
                    curr_agents_to_vaccinate -= 1

                elif (lh is not None
                      and lh.vaccine_name in self.available_vaccines
                      and self.available_vaccines[lh.vaccine_name]['type']
                      == 'Multi'):
                    if (lh.current_dose <
                            self.available_vaccines[lh.vaccine_name]['dose']
                            and time_step - lh.time_stamp >=
                            self.available_vaccines[lh.vaccine_name]
                        ['interval'][lh.current_dose - 1]):
                        current_vaccine = None
                        for vaccine in self.vaccines:
                            if vaccine.vaccine_name == lh.vaccine_name:
                                current_vaccine = vaccine
                                break
                        if current_vaccine is not None:
                            result = current_vaccine.vaccinate(
                                agent, time_step, lh.current_dose + 1)
                            self.results.append(result)
                            self.vaccines.remove(current_vaccine)
                            curr_agents_to_vaccinate -= 1

    def add_vaccines(self,
                     vaccines: Dict[str, Dict[str, Union[int, float, List[int],
                                                         str]]],
                     dosage: str = 'Single') -> None:
        """
        This function enables the user to add vaccines.

        Parameters to be specified for single dose vaccines:

        * cost: Cost of vaccine.
        * count: Number of vaccine available.
        * efficacy: Vaccine efficacy.
        * decay: Number of days of protection offered by the vaccine.

        Parameters to be specified for multi dose vaccines:

        * cost: Cost of vaccine.
        * count: Number of vaccine available.
        * efficacy: Vaccine efficacy.
        * decay: A list of number of days of protection offered by each dose of the vaccine.
        * dose: Number of doses of the vaccine.
        * interval: A list specifying minimum days to pass before the administration of the next dose for each dose.

        Args:
            vaccines: A dictionary mapping vaccine names to its parameters
            dosage: Specifies if the vaccines are either ``Single`` dose or ``Multi`` dose
        """
        if dosage == 'Single':
            for name, vaccine in vaccines.items():
                if not isinstance(vaccine['decay'], int):
                    raise TypeError('Vaccine decay must be a type integer')
                self.available_vaccines[name] = vaccine
                self.available_vaccines[name]['type'] = dosage
                self.statistics[name] = {
                    'Total Vaccination': [],
                    'Total Successful': [],
                    'Total Unsuccessful': []
                }
        elif dosage == 'Multi':
            for name, vaccine in vaccines.items():
                if not isinstance(vaccine['decay'], list):
                    raise TypeError('Vaccine decay must be a list')
                if vaccine.get('dose') is None:
                    raise Exception('Dose parameter missing')

                if vaccine.get('interval') is None:
                    raise Exception('Interval parameter missing')

                if not isinstance(vaccine['interval'], list):
                    raise TypeError('Interval must be a list')
                if len(vaccine['decay']) != vaccine['dose']:
                    raise ValueError(
                        'Vaccine decay must be a list of length equal to the count of vaccine dosage'
                    )
                if len(vaccine['interval']) != vaccine['dose'] - 1:
                    raise ValueError(
                        'Vaccine interval must be a list of length one less than the count of vaccine dosage'
                    )
                self.available_vaccines[name] = vaccine
                self.available_vaccines[name]['type'] = dosage
                self.statistics[name] = {
                    'Total Vaccination': [],
                    'Total Successful': [],
                    'Total Unsuccessful': []
                }

    def set_protection(self, agents: ValuesView[Agent]) -> None:
        """
        For every vaccinated agent the protection days offered by the vaccine in agent history is decremented by 1.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
        """
        for agent in agents:
            history = self.get_agent_policy_history(agent)
            # dict of result objects
            if len(history
                   ) == 0 or history[-1].result == 'Unsuccessful' or history[
                       -1].protection == 0:
                continue
            else:
                history[-1].protection -= 1

    def populate_results(self) -> None:
        """
        Updates agent policy history and state from the list of results.
        """
        for result_obj in self.results:
            agent = result_obj.agent
            self.update_agent_policy_history(agent, result_obj)
            self.update_agent_policy_state(agent, result_obj.result)

    def restrict_agents(self, agents: ValuesView[Agent]) -> None:
        """
        Restricts the ability of a vaccinated agent to receive an infection.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
        """
        for agent in agents:
            history = self.get_agent_policy_history(agent)
            if (len(history) != 0):
                if (history[-1].result == 'Successful'):
                    if (history[-1].protection >= 1):
                        agent.protect()

    def get_stats(self) -> None:
        """
        Calculates the overall statistics of the vaccines administered.
        """
        self.statistics_total['Total Vaccination'].append(0)
        self.statistics_total['Total Successful'].append(0)
        self.statistics_total['Total Unsuccessful'].append(0)
        for name in self.available_vaccines.keys():
            self.statistics[name]['Total Vaccination'].append(0)
            self.statistics[name]['Total Successful'].append(0)
            self.statistics[name]['Total Unsuccessful'].append(0)

        for result_obj in self.results:
            self.statistics_total['Total Vaccination'][-1] += 1
            name = result_obj.vaccine_name
            self.statistics[name]['Total Vaccination'][-1] += 1
            result = result_obj.result
            if result == 'Successful':
                self.statistics[name]['Total Successful'][-1] += 1
                self.statistics_total['Total Successful'][-1] += 1
            elif result == 'Unsuccessful':
                self.statistics[name]['Total Unsuccessful'][-1] += 1
                self.statistics_total['Total Unsuccessful'][-1] += 1
