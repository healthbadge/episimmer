# Stochastic_SEYAR
This example has been built by extending the Stochastic SIR model by introducing the additional states "Asymptomatic" and "Symptomatic". 

The agents are allowed to interact in an event at a location where they can contribute to or receive from an ambient infection.


## Significance of Stochastic_SEYAR
Episimmer uses this fundamental Stochastic model for scenarios in which the rate at which an agent changes its state can be probabilistically determined. By the end of the specified number of time steps, the total population remains unchanged.


## Running Stochastic_SEYAR
To run code from current directory :

		cd examples/Basic_Disease_Models
		python ../src/Main.py Stochastic_SEYAR

		
