# Stochastic_SIR_complete_graph
This example is an alteration of the Stochastic SIR model.

Here, each agent interacts with every other agent bidirectionally and all of these interactions are listed in the complete_interactions_list.txt file.

It considers the agents to be vertices in a complete graph with each edge being an interaction between the two connecting agent vertices.


## Significance of Stochastic_SIR_complete_graph
Due to this structural difference, instead of having the disease spread in n time using the concept of ambient infections as seen in Stochastic_SIR, it spreads between each pair of agents in n square time. This reduces the complexity of determining the overall effect of individual interactions, as now, it is a direct squared function of the number of agents involved. 

Episimmer uses this example to give a different perspective of disease flow and can be used where all the considered agents are part of an event. 


## Running Stochastic_SIR_complete_graph
To run code from current directory :

		cd examples/Interaction_Spaces
		python ../src/Main.py Stochastic_SIR_complete_graph

		
