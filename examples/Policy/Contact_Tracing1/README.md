# Contact_Tracing1

This example showcases the first kind of Contact Tracing policy in Episimmer. It first performs testing on random
agents and then trace their contacts to lock them down. You can run multiple contact tracing policies concurrently for different
types of agents. Since we want mitigation of disease spread, we implement a lockdown policy with contact tracing enabled
to not only lock down the contacts of the positive agents but even the positive agents themselves.
