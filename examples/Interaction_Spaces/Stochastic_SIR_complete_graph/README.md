# Stochastic_SIR_complete_graph
This example is a variation of the Stochastic SIR model. Instead of having the disease spread in O(n) time using the concept of ambient infections as seen in Stochastic_SIR, it spreads between each pair of agents in O(n^2) time using interactions.

This is why Events as a disease spread module is very important in Episimmer. It is a very efficient way of modelling interactions between the agents where we have no information on single agent-agent interactions.

Here, each agent interacts with every other agent bidirectionally and all of these interactions are listed in the complete_interactions_list.txt file.


## Additional Information

It considers the agents to be vertices of a complete graph with each edge being an interaction between the two connecting agent vertices.

Episimmer uses this example to give a different perspective of disease flow and can be used where all the considered agents are part of an event.
