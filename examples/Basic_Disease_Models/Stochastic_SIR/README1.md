# Stochastic_SIR
This example has been built using the Stochastic Model consisting of three states Susceptible, Infected and Recovered.

The agents are allowed to interact in an event at a location where they can contribute to or receive from an ambient infection.

As output, it plots a graph that helps us visualize disease spread over a specified number of time steps and a specified number of worlds.<br>


## Significance of Stochastic_SIR
This example has been included in Episimmer as it might be appropriate when the rates of movement between compartments, and hence the evolution of the disease, are fast enough so that the life span of an individual does not need to be taken into account.

This is supported by the fact that the population of agents is initially assigned to one of the three compartments, which is defined by their initial proportions. 

The rate at which an agent changes its state is then probabilistically determined and by the end of the specified number of time steps, the total population remains unchanged.


## Running Stochastic_SIR
To run code from current directory :

		cd examples/Basic_Disease_Models
		python ../src/Main.py Stochastic_SIR

		
