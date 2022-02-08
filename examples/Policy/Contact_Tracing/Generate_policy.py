import random

from episimmer.policy import (contact_tracing_policy, lockdown_policy,
                              testing_policy)


def agents_per_step_fn(cur_time_step):
    return 7

def generate_policy():
    policy_list=[]
    Normal_Test = testing_policy.TestPolicy(agents_per_step_fn)
    Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)
    Normal_Test.set_register_agent_testtube_func(Normal_Test.random_agents(1,1))

    # Num of timesteps to store agents
    CT_object = contact_tracing_policy.CTPolicy(7, 'Type', ['Teacher'])
    CT_object2 = contact_tracing_policy.CTPolicy(3, 'Type', ['Student'])

    # do lockdown function, Num of days to lockdown based on test result, Contact tracing boolean
    Lockdown_object = lockdown_policy.TestingBasedLockdown(lambda x:random.random()<0.95, 2, True)
    policy_list.append(Normal_Test)
    policy_list.append(CT_object)
    policy_list.append(CT_object2)
    policy_list.append(Lockdown_object)

    return policy_list
