# Symptomatic Testing
This example shows the use of the Symptomatic Testing. It gives the agents of the simulation a chance to test themselves as they develop visible conditions of having the disease. Be sure to set the symptomatic states in the UserModel.py file for this to work. It will be ignored if the correct states are not passed.

This example shows this use case with the SEYAR model representing the Susceptible, Exposed, Symptomatic, Asymptomatic and Recovered
states. Our symptomatic state is "Symptomatic" state in the disease model. In the testing policy, while registering the agent to a testtube, you can set the only_symptomatic parameter to true. This will choose only the agents that are part of the symptomatic states for testing.


## Additional Information
Be careful while using this method because you should not pass the disease states that do not represent agents with visible symptoms. For example, asymptomatic agents do not show any symptoms of the disease and must not be passed in this list.
