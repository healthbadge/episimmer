# Contact_Tracing2

This example showcases the second kind of Contact Tracing policy in Episimmer. It first performs testing on random
agents and then trace their contacts. The traced contacts are then tested for potential lock down, unlike the first kind
where they are directly lock down. Only if the contacts test positive are they lock down for a fixed period of time.
Once again, You can run multiple contact tracing policies concurrently for different types of agents.
