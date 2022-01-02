# Stochastic_SEYAR
This example has been built by extending the Stochastic SIR model by introducing the additional states "Asymptomatic" and "Symptomatic". 


## Significance of Stochastic_SEYAR
Episimmer uses this example to explore a different type of compartmentalised model. This helps ascertain the fact that the simulation works for more complex state transitions as well (Exposed to Asymptomatic and Symptomatic).

This example proves that we can have multiple transitions from a single state and each of these transitions can be chosen with a certain probability. 


## Running Stochastic_SEYAR
To run code from current directory :

		cd examples/Basic_Disease_Models
		python ../src/Main.py Stochastic_SEYAR

		