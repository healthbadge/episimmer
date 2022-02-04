from episimmer.policy import lockdown_policy


def generate_policy():
    policy_list = []

    def lockdown_fn(time_step):
        return False

    policy_list.append(lockdown_policy.FullLockdown(lockdown_fn))

    return policy_list
