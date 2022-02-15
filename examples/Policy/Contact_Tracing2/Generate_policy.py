import random

from episimmer.policy import (contact_tracing_policy, lockdown_policy,
                              testing_policy)


def agents_per_step_fn(cur_time_step):
    return 2

def generate_policy():
    policy_list=[]
    Normal_Test1 = testing_policy.TestPolicy(agents_per_step_fn)
    Normal_Test1.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
    Normal_Test1.set_register_agent_testtube_func(Normal_Test1.random_agents(1,1))

    Normal_Test2 = testing_policy.TestPolicy(agents_per_step_fn)
    Normal_Test2.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
    Normal_Test2.set_register_agent_testtube_func(Normal_Test2.contacts_agents(1,1))

    # Num of timesteps to store agents
    CT_object = contact_tracing_policy.CTPolicy(7)


    # do lockdown function, Num of days to lockdown based on test result, Contact tracing boolean
    Lockdown_object = lockdown_policy.TestingBasedLockdown(lambda x:1, 2)
    policy_list.append(Normal_Test1)
    policy_list.append(Normal_Test2)
    policy_list.append(CT_object)
    policy_list.append(Lockdown_object)

    return policy_list
