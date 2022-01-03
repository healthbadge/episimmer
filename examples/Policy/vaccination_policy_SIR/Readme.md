# Vaccination Policy SIR
The disease model used in this example is the Stochastic SIR model.A vaccination policy in Episimmer is a user defined intervention policy being able to cater to various vaccination strategies.This policy, derived from agent based policy has high flexibility giving high liberty with respect to user input.The success and failure rates of each vaccine type are recorded. Users can add vaccination type(name), cost, efficacy and quantity. Users can also define functions to determine the number of agents to be vaccinated in every time step.(Templates have been made for the same.)
People are vaccinated to ensure they have immunity for a certain number of days starting from the time step they’re vaccinated. Vaccination has two outcomes, “ Successful” or “ Unsuccessful”. 

# Running 
To run code from current directory :

		cd examples/Policy
		python ../../src/Main.py vaccination_policy_SIR