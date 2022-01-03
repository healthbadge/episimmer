# Scheduled_SIR
The disease transmission between states may be defined by schedule change in states. The states are Susceptible, Infected and Recovered.

The mean and variance parameters are used for the independent transitions.


## Significance of Scheduled_SIR
Episimmer has used this example as a fundamental Scheduled model which uses the SIR compartmentalised representation.

In some populations, the agents might show a recovery period of 10 days on an average with a deviation of say 3 days, instead of the whole population recovering at some constant rate. In other words, the transition between states may be symmetric about some mean. In such situations, the transition between the states can be scheduled with some mean and standard deviation.

This provides flexibility in asserting the way the population reacts to disease spread, as we have the liberty to specify different means for different population types or for different time periods.


## Running Scheduled_SIR
To run code from current directory :

		cd examples/Basic_Disease_Models
		python ../src/Main.py Scheduled_SIR

Plots a graph as output representing disease spread for a specified number of time steps and a specified number of worlds.<br>
		





