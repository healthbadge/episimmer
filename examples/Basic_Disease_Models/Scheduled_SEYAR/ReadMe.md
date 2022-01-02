# Scheduled_SEYAR
This example has been built by introducing two additional states to the Scheduled SIR disease model- "Asymptomatic" and "Symptomatic". 

It includes one event where the agents either contribute to or receive from ambient infection.   


## Significance of Scheduled_SEYAR
This is a basic example which is used as a baseline for building more complex Scheduled models by introducing complexity in events, interactions, policies and restrictions.

This example helps in showing disease spread through an event where all agents are likely to interact with each other, and where transition from one state to another, for a population, may be symmetric about a mean. This is important for scenariois in which the population under consideration collectively shows a state transition that averages to a mean with some deviation.

The SEYAR model has four independent state transitions which may utilise this schedule change in state.


## Running Scheduled_SEYAR
To run code from current directory :

		cd examples/Basic_Disease_Models
		python ../src/Main.py Scheduled_SEYAR

		





