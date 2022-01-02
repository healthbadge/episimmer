# Stochastic_SIR_random_graph
This example is a variation of the Stochastic_SIR_random_graph model.

Instead of all the agents participating in the interactions, only a random set of agents interact with each other bidirectionally and all of these interactions are listed in the interactions_list.txt file.


## Significance of Stochastic_SIR_random_graph
At times, even in an event, there might be set of agents that will most definitely interact with each other (interaction in both ways). We implement this by randomising this set of agents.


## Running Stochastic_SIR_random_graph
To run code from current directory :

		cd examples/Interaction_Spaces
		python ../src/Main.py Stochastic_SIR_random_graph

		
