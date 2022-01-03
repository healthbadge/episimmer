# Scheduled_SEYAR_custom_distribution
This example builds over the basic Scheduled SEYAR model by introducing the concept of custom distributions.

Custom distribution provides flexibility in terms of scheduling changes in state for user defined distributions.

In real life scenarios, not all distributions are symmetric about a mean (not all are Normal distributions). Thus, for Scheduled models, Custom distributions provide flexibility in terms of scheduling changes in state for user defined distributions.

## Additional Information

It helps us understand that there may exist a population in which, for instance, there is a greater chance of a person recovering in x number of days and a lower chance of them recovering in y or z number of days. We are essentially including a likelihood factor with respect to the duration of recovery. This is in comparison to stating that the person essentially recovers in x days with a variation of 1 day.

This way, the user has the liberty of customising the distribution in the number of time steps to represent the population under consideration in the best possible way.

More on custom distributions in [Tutorial 2.1](https://docs.google.com/document/d/1vn8xc95bCQ7K09lMuc3ijHfSeDPa6Nd28tko-19SlnQ/edit).
