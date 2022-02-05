import episimmer.model as model


#This function represents the probability of getting infected during a single interaction/contact
def probabilityOfInfection_fn(p_infected_states_list, contact_agent, c_dict,
                              current_time_step):
    if contact_agent.state == 'Infected':
        return 0.8  #This is the probability of getting infected from contact in a time step isf contact is infected
    return 0  # If contact is not infected then the probability of them infecting you is 0


# This function states the amount an agent contributes to ambient infection in the region
#note that only infected agents contibute to the ambient infection
def event_contribute_fn(agent, event_info, location, current_time_step):
    if agent.state == 'Infected':
        return 1
    return 0


#This fucntion states the probability of an agent becoming infected fromt he ambient infection
def event_receive_fn(agent, ambient_infection, event_info, location,
                     current_time_step):
    beta = 0.001
    return ambient_infection * beta


class UserModel(model.StochasticModel):
    def __init__(self):
        individual_types = [
            'Susceptible', 'Infected', 'Recovered'
        ]  #These are the states that will be used by the compartmental model
        infected_states = ['Infected']  #These are the states that can infect
        state_proportion = {  #This is the starting proportions of each state
            'Susceptible': 0.8,
            'Infected': 0.1,
            'Recovered': 0.1
        }
        model.StochasticModel.__init__(
            self, individual_types, infected_states,
            state_proportion)  #We use the inbuilt model in the package
        self.set_transition(
            'Susceptible', 'Infected',
            self.p_infection(None, probabilityOfInfection_fn)
        )  #Adding S-> I transition which is based on probability)fInfection_fn
        self.set_transition('Infected', 'Recovered',
                            self.p_standard(0.2))  #Adding the I->R transition

        self.set_event_contribution_fn(event_contribute_fn)
        self.set_event_receive_fn(event_receive_fn)

        self.name = 'Stochastic SIR'