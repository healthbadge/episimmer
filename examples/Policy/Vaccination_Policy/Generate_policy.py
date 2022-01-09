from episimmer.policy import lockdown_policy, vaccination_policy


def agents_per_step_fn(time_step):

	n=100

	return n

def generate_policy():
	policy_list=[]


	vp= vaccination_policy.VaccinationPolicy(agents_per_step_fn)

	# Single Dose Vaccination
	vaccines = {
		'cov_single_dose': {'cost': 40, 'count': 20, 'efficacy': 0.9, 'decay': 40},
		'cov_single_dose2': {'cost': 50, 'count': 15, 'efficacy': 0.5, 'decay': 30},
	}
	vp.add_vaccines(vaccines, 'Single')
	vp.set_register_agent_vaccine_func(vp.random_vaccination())

	# Multi Dose Vaccination
	vaccines = {
		'cov_multi_dose': {'cost': 40, 'count': 25, 'efficacy': 0.4, 'decay': [15, 14, 8], 'dose': 3, 'interval': [3, 2]},
		'cov_multi_dose2': {'cost': 30, 'count': 40, 'efficacy': 0.7, 'decay': [20, 25, 17, 5], 'dose': 4, 'interval': [12, 26, 14]},
		'cov_multi_dose3': {'cost': 30, 'count': 15, 'efficacy': 0.7, 'decay': [8], 'dose': 1, 'interval': []}
	}
	vp.add_vaccines(vaccines, 'Multi')
	vp.set_register_agent_vaccine_func(vp.multi_dose_vaccination())


	policy_list.append(vp)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
