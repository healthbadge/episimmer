
Miscellaneous
=====================================

How are Events modelled?
---------------------------

Events

Agent-Based models (ABM) vs Equation-Based models (EBM)
--------------------------------------------------------

The most popular epidemic modelling paradigms are Agent-Based models and Equation-Based models. This section compares the two and gives more context on
Episimmer's modelling principles.

EBM
~~~~~

EBMs are built using a set of equations that express relationships among observables. Solving these equations
using numerical techniques produces the evolution of the
observables over time. These equations may be algebraic, time varying ordinary differential equations (ODE), or space-time
varying partial differential equations.

EBMs tends to focus the modeller’s attention on the overall behaviour of the system rather than the micro-level behaviour of individual agents.
It suggests a system as a whole in the first place and does not support an explicit representation of components (agents). Thus, it is regarded as a Top-down strategy.

In the case of compartmental models modelled using EBMs, The population is assigned to compartments with labels – for example, S, I, or R, (Susceptible, Infectious, or Recovered).
All entities/agents in a compartment are identical in nature. The entities will always interact with every other entity, forming a complete graph
of interactions between the entities (Like an Event in Episimmer).

These entities have no memory of what states they were in previously or how long they were in their previous states. The probability of each transition depends only on the state attained in the previous transition (like Markov Chains).
These models are much easier to solve as they involve only the population of each compartment and the assumption that all entities are identical in a compartment. Due to this assumption, we are generalising the population and hence the model itself.


ABM
~~~~~

ABM usually starts out with modelling properties and behaviour of individual agents and only thereafter considers macro-level effects to emerge from the aggregation of agents’ behaviour. i.e. The system is expected to emerge from the interaction of individual agents.

ABM now complement traditional compartmental models, the usual type of epidemiological models, and are used to simulate the simultaneous operations and interactions of multiple agents, in an attempt to re-create and predict the appearance of complex phenomena.

ABM might seem intuitively more appropriate for modelling social systems, since it allows, and even necessitates, considering individual decisions, dispositions and inclinations. Unlike ODE, ABMs have a Bottom-up strategy.
This type of modelling uses the concept of autonomous agents that need not be identical to each other. Every agent has an identity and can be made different from every other agent. The agent can be given attributes like Blood Type, Immunity levels, Age, etc. These agents can also hold memory of what states they were in previously.
A key difference is that the interactions now need not be a complete graph but any type of interaction can be modelled. These interactions can be any static graph(need not be complete) or dynamic graph that changes over time. Thus, each agent can have different probabilities of gaining or recovering the disease. Due to these added
complexities, the agent based model is more complex and will require more processing time than the EBM based model.

Some differences between an Equation Based Model (EBM) and an Agent Based Model (ABM) are given below.


.. image:: https://ieeexplore.ieee.org/mediastore_new/IEEE/content/media/6515923/6516413/6516432/6516432-table-1-source-large.gif
    :width: 400


Taken from `Agent-Based vs. Equation-Based Epidemiological Models: A Model Selection Case Study. <https://ieeexplore.ieee.org/document/6516432>`_
This paper has a nice introduction and comparison between the two types of models.

.. note ::
      Episimmer is strictly an ABM.
