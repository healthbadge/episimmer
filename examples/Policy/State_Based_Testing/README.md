# State Based Lockdown
This example shows the use of the state-based Testing policy. The state-based testing method gives the agents of the simulation a chance to test themselves as they develop visible conditions of having the disease. The agent states passed in state_testing method must correspond to the disease model states in the UserModel.py file to work. It will be ignored if the correct states are not passed. Be careful while using this method because you should not pass the disease states that do not represent agents with visible symptoms. For example, asymptomatic agents do not show any symptoms of the disease and must not be passed in this list.

This example shows this use case with the SEYAR model representing the Susceptible, Exposed, Symptomatic, Asymptomatic and Recovered
states. Our state list passed to the state_testing method contains the list with a single element "Symptomatic".
