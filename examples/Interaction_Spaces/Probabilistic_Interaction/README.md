# Probabilistic_Interaction
This example uses the Stochastic Model comprising of the states Susceptible, Infected and Recovered.

The agents can contribute or receive infection based on who they interact with, and these interactions are probabilistically determined.

While configuring the probabilistic interactions file, along with specifying the agents that are interacting with each other, it is necessary to specify the probability with which they interact.

The probabilistic interactions are considered to be bidirectional (as compared to interactions which are unidirectional) and hence can be specified as:
        Probability:Agents
where "Agents" are all the interacting agents seperated by commas.


## Significance of Probabilistic_Interaction
When two agents from the population space are known to interact, they might not necessarily interact with a 100% surity at each time step.

For instance, the interaction between a student and a teacher in a university might be considered to be probabilistic taking into account that the student has a consistent 95% attendance. 

Hence, probabilistic interactions allow us to specify interactions between agents that are not most definitely bound to happen.


## Running Probabilistic_Interaction
To run code from current directory :

		cd examples/Interaction_Spaces
		python ../src/Main.py Probabilistic_Interaction

		
