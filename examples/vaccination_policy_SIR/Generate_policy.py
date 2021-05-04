import Vaccination_policy
import Lockdown_Policy

def agents_per_step_fn(time_step):

	n=100

	return n

def generate_policy():
	policy_list=[]


	vp= Vaccination_policy.Vaccination_policy(agents_per_step_fn)
	# vp.add_vaccination("cov",250,30,0.7,50)
	vp.add_vaccination("cov2",500,40,0.5,20)

	vp.add_vaccination("cov22",500,40,1,20)
	vp.add_vaccination("cov32",500,40,0.5,20)

	policy_list.append(vp)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn