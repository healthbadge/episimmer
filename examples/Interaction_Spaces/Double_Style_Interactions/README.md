# Double_Style_Interactions

This example showcases the use of both regular and probabilistic interactions.

Since we have both types of interactions, we should use 'Agent Index:Interacting Agent Index' key, omitting the 'Probability:Agents' as the parameter keys. Additional user-defined parameters (like ‘duration’) must be present in both the interaction files and appended to the Interaction Info Keys.

Thus our config.txt has the parameters : 'Agent Index:Interacting Agent Index:duration'

The disease model being used here is the Stochastic Model comprising of the states Susceptible, Infected and Recovered.
