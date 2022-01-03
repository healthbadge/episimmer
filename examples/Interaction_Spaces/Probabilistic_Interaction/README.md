# Probabilistic_Interaction

This example showcases the use of probabilistic interactions. The agents can contribute or receive infection based on who they interact with, and these interactions are probabilistically determined.

While configuring the probabilistic interactions file, along with specifying the agents that are interacting with each other, it is necessary to specify the probability with which they interact.

The probabilistic interactions are considered to be bidirectional (as compared to interactions which are unidirectional) and hence can be specified as:
        Probability:Agents
where "Agents" are all the interacting agents separated by commas.

The disease model being used here is the Stochastic Model comprising of the states Susceptible, Infected and Recovered.


## Additional Information

The interaction between a student and a teacher in a university might be considered to be probabilistic taking into account that the student has a consistent 95% attendance.

Hence, probabilistic interactions allow us to specify interactions between agents that are not most definitely bound to happen.
