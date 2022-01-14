Disease Model
=====================================

* :ref:`Introduction - Disease Modelling`
* :ref:`Building the Disease Model`
* :doc:`Disease Model API<../modules/model>`

Introduction - Disease Modelling
-----------------------------------

Disease models are used to model the spread of disease across agents in the environment. Agents are the disease carriers and all the different types of interactions present facilitate the spread of infection.

In Episimmer, There are two basic types of disease models -

1. *Stochastic Model*

2. *Scheduled Model*


Before we detail the two models, we shall first look into standard compartmental model theory

Compartmental Models
^^^^^^^^^^^^^^^^^^^^^^^

Both models in Episimmer follow the `compartmental style of disease modelling <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology>`_ i.e. they have compartments or states that define the agent's disease state and
each state contains a proportion of the entire population.

Consider the SIR compartmental model where S, I and R represent the Susceptible, Infectious and Recovered populations.


.. image:: https://www.freecodecamp.org/news/content/images/2020/03/Screenshot-2020-03-30-at-01.23.52.png
    :width: 400


New infections occur as a result of contact between Infectious and Susceptible agents. In this simple model the rate at which new infections occur is :math:`\beta S I` for some positive constant :math:`\beta`. When a new infection occurs, the individual infected moves from the susceptible class to the infective class.

The other process that can occur is that infective individuals can enter the Recovered compartment. We assume that this happens at the rate :math:`\gamma I` for some positive constant :math:`\gamma`. Thus we have our three differential equations:


.. image:: https://wikimedia.org/api/rest_v1/media/math/render/svg/c2a8fd2e93bfcf1092a44cfec7ef32c1a80a26f4
    :width: 150

The two transitions between states differ because the first is a dependent transition while the second is independent. Dependent transitions are transitions that are directly dependent on the population of Infectious states while Independent
transition do not depend on the population of other states.


Example of a dependent and independent transition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assume an SIR compartmental model with :math:`\beta = 0.2` and :math:`\gamma = 0.3`,

For the Dependent Transition :math:`S \rightarrow I`, If we have a population of 90 agents in Susceptible state and 10 agents in Infectious state at :math:`T_n`,

An expectation of :math:`90 \times 0.02 \times 10 = 18` agents will transition to the Infectious compartment at :math:`T_{n+1}`.

For the Independent Transition :math:`I \rightarrow R`, If we have a population of 30 agents in Infectious state at :math:`T_n`,

An expectation of :math:`30 \times 0.3 = 9` agents will transition to the Recovered compartment at :math:`T_{n+1}`.



Difference between Stochastic and Scheduled Models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To reiterate, both these models have compartments associated with them. They only differ by the transition rules.

Stochastic model allows us to implement compartmental models with probabilistic changes in state. A stochastic epidemic model can be used to understand disease transmission dynamics. Consider a disease that
is stable in its prevalence due to a constant supply of susceptible individuals. At some point in time, by chance, the disease may fail to be passed on before dying out, resulting in a disease-free population.
This can be captured by embedding stochasticity within the model.

Scheduled models have transitions that are scheduled based on a distribution. For example in the real world an infected person might take on average 10 days with a variance of 2 days to recover.

.. note ::
        The platform’s simulations are not continuous as in, it does not solve the differential equations but simulates it out in discrete time steps using agents. As the time step becomes smaller and the number of agents increases the plot will tend towards a continuous one as produced by the equations.


.. note ::
        While Scheduled model's independent transitions are solely based on scheduled times, dependent transitions are dependent on probability of change (infection) just as in the Stochastic models.


Building the Disease Model
----------------------------
