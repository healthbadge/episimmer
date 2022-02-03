from episimmer.policy import lockdown_policy, vaccination_policy


def agents_per_step_fn(time_step):

	n=100

	return n

def generate_policy():
	policy_list=[]

	# Single Dose Vaccination
	vp1= vaccination_policy.VaccinationPolicy(agents_per_step_fn)
	vaccines1 = {
		'cov_single_dose': {'cost': 40, 'count': 20, 'efficacy': 0.9, 'decay': 40},
		'cov_single_dose2': {'cost': 50, 'count': 15, 'efficacy': 0.5, 'decay': 30},
	}
	vp1.add_vaccines(vaccines1, 'Single')
	vp1.set_register_agent_vaccine_func(vp1.random_vaccination())

	# Multi Dose Vaccination
	vp2= vaccination_policy.VaccinationPolicy(agents_per_step_fn)
	vaccines2 = {
		'cov_multi_dose': {'cost': 40, 'count': 25, 'efficacy': 0.4, 'decay': [15, 14, 8], 'dose': 3, 'interval': [3, 2]},
		'cov_multi_dose2': {'cost': 30, 'count': 40, 'efficacy': 0.7, 'decay': [20, 25, 17, 5], 'dose': 4, 'interval': [12, 26, 14]},
		'cov_multi_dose3': {'cost': 30, 'count': 15, 'efficacy': 0.7, 'decay': [8], 'dose': 1, 'interval': []}
	}
	vp2.add_vaccines(vaccines2, 'Multi')
	vp2.set_register_agent_vaccine_func(vp2.multi_dose_vaccination())


	policy_list.append(vp1)
	policy_list.append(vp2)

	return policy_list
