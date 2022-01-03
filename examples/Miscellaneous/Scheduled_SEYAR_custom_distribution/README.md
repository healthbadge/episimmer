# Scheduled_SEYAR_custom_distribution
This example builds over the basic Scheduled SEYAR model by introducing the concept of custom distributions. 


## Significance of Scheduled_SEYAR_custom_distribution
Custom distribution provides flexibility in terms of scheduling changes in state for user defined distributions. 

Episimmer uses this example to prove that in reality, not all distributions are symmetric about a mean (Normal distribution). By using a random variable we can probabalistically determine the state that an agent will persist in, rather than assuming that all populations adhere to symmetry about a mean with some deviation. 

It helps us understand that there may exist a population in which, for instance, there is a greater chance of a person recovering in x number of days and a lower chance of them recovering in y or z number of days. We are essentially including a likelihood factor with respect to the duration of recovery. This is in comparison to stating that the person essentially recovers in x days with a variation of 1 day.
 
This way, the user has the liberty of customising the distribution in the number of time steps to represent the population under consideration in the best possible way. 


## Running Scheduled_SEYAR_custom_distribution
To run code from current directory :

		cd examples/Miscellaneous
		python ../src/Main.py Scheduled_SEYAR_custom_distribution






