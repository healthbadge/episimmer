# Stochastic_SIRID_variable_rates
This example has been built by extending the Stochastic SIR model by introducing the additional states "ICU" and "Dead".


## Additional Information
This example demonstrates the flexibility that can be achieved while working with different compartmentalised models.

During the outbreak of an infection, the agents of the population may adapt to the changing environments by inventing new and better medication. Such behavioural approaches may influence the rate at which the population progresses to a state.

This shows that it is not always necessary to have a constant rate of transition between states. The variable rates of state transition may be defined as a function of the current time step (as seen in UserModel.py).
