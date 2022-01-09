import copy
import random
from functools import partial

from .base import AgentPolicy


class VaccineResult():
    def __init__(self, vaccine_name, agent, result, time_step, efficacy,
                 decay_days, current_dose):
        self.vaccine_name = vaccine_name
        self.agent = agent
        self.result = result
        self.time_stamp = time_step
        self.protection = decay_days
        self.current_dose = current_dose


class VaccineType():
    def __init__(self,
                 name,
                 cost,
                 decay,
                 efficacy,
                 dosage=None,
                 interval=None):

        self.vaccine_name = name
        self.vaccine_cost = cost
        self.decay_days = decay
        self.efficacy = efficacy
        self.dosage = dosage
        self.interval = interval

    def vaccinate(self, agent, time_step, dose=1):

        # vaccinate agents
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

    def inject_agent(self, agent):

        if (random.random() < self.efficacy):
            return 'Successful'
        else:
            return 'Unsuccessful'


class VaccinationPolicy(AgentPolicy):
    def __init__(self, agents_per_step_fn=None):
        super().__init__()

        self.num_agents_to_vaccinate = None
        self.results = None
        self.policy_type = 'Vaccination'
        self.available_vaccines = {}
        self.vaccines = []
        self.statistics = {}
        self.statistics_total = {
            'Total Vaccination': [],
            'Total Successful': [],
            'Total Unsuccessful': []
        }
        self.registered_agent_vaccine_func = None
        assert callable(agents_per_step_fn)
        self.agents_per_step_fn = agents_per_step_fn

    def enact_policy(self, time_step, agents, locations, model=None):

        self.newday(time_step)
        self.set_protection(agents)
        self.registered_agent_vaccine_func(agents, time_step)
        self.populate_results()
        self.restrict_agents(agents)
        self.get_stats()

    def newday(self, time_step):

        self.vaccines = []
        self.results = []
        self.num_agents_to_vaccinate = self.agents_per_step_fn(time_step)

        for name, vaccine in self.available_vaccines.items():
            for i in range(int(self.available_vaccines[name]['count'])):
                vaccine_obj = VaccineType(name, vaccine['cost'],
                                          vaccine['decay'],
                                          vaccine['efficacy'],
                                          vaccine.get('dose', 0),
                                          vaccine.get('interval', []))
                self.vaccines.append(vaccine_obj)

    def set_register_agent_vaccine_func(self, func):
        self.registered_agent_vaccine_func = func

    def random_vaccination(self, parameter=None, value_list=[]):
        assert isinstance(value_list, list)
        return partial(self.full_random_vaccination,
                       parameter=parameter,
                       value_list=value_list)

    def full_random_vaccination(self, agents, time_step, parameter,
                                value_list):
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

    def multi_dose_vaccination(self, parameter=None, value_list=[]):
        return partial(self.full_multi_dose_vaccination,
                       parameter=parameter,
                       value_list=value_list)

    def full_multi_dose_vaccination(self, agents, time_step, parameter,
                                    value_list):
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

    def add_vaccines(self, vaccines, dosage='Single'):
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

    def set_protection(self, agents):
        for agent in agents:
            history = self.get_agent_policy_history(agent)
            # dict of result objects
            if len(history
                   ) == 0 or history[-1].result == 'Unsuccessful' or history[
                       -1].protection == 0:
                continue
            else:
                history[-1].protection -= 1

    def populate_results(self):
        for result_obj in self.results:
            agent = result_obj.agent
            self.update_agent_policy_history(agent, result_obj)
            self.update_agent_policy_state(agent, result_obj.result)

    def restrict_agents(self, agents):
        for agent in agents:
            history = self.get_agent_policy_history(agent)
            if (len(history) != 0):
                if (history[-1].result == 'Successful'):
                    if (history[-1].protection >= 1):
                        agent.update_recieve_infection(0.0)

    def get_stats(self):
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
