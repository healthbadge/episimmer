
Environment
=====================================

* :ref:`Introduction - Environment`
* :ref:`Building the Environment`
* :ref:`Environment API`

Introduction - Environment
----------------------------
Episimmer is an agent-based simulation tool. An agent-based model simulates a system consisting of individual agents
behaving independently in order to understand this underlying system. In our case, the underlying system is the disease
spreading over a population of agents. We call this system, the *Environment*.

The components of the environment include :

* :ref:`Agents`
* :ref:`Individual Interactions`
* :ref:`Events and Locations`
* :ref:`One Time Events`
* :ref:`Probabilistic Interactions`


Agents
~~~~~~~~
Agent form the core of the simulation. They represent the human population in the simulation and are the carriers of the disease.
Without them, there is no simulation possible in Episimmer. Each agent can have
any number of attributes to distinguish them from the other agents and there are multiple possibilities of using these attributes
to manage their behaviour in the environment and how they are affected by it. For example, an agent can be a student in
a university or an office worker. Their attributes can differ by age, sex, blood type etc. Episimmer can model the agents
with any number of attributes and is only limited by computational resources.


Individual Interactions
~~~~~~~~~~~~~~~~~~~~~~~~
An Individual/Simple Interaction in Episimmer is the connecting interaction between two agents. If agents are the vertices of a graph,
the interactions represent the edges. These interactions are also directional so keep that in mind while building your Environment.

Events and Locations
~~~~~~~~~~~~~~~~~~~~~~~~

Events are another type of interactions where they occur at a location. When you have a scenario with all agents interacting with each other, you should use Events. In graph terms, they represent a complete graph of Individual interactions.
For example, if Classroom A is a location then Elementary Physics and Elementary Chemistry are events that happen at the location of classroom A. In an event all agents involved interact with each other through
a medium called ambient infection. All infectious agents can contribute to the ambient infection and all susceptible agents can receive infection from the
ambient infection and have a chance of being infected.


.. note::
        While modelling Events as Individual Interactions (all agents connected to each other), the time complexity is of :math:`O(n^{2})` while events
        have time complexity of :math:`O(n)`. Check :doc:`Miscellaneous<misc>` for more details on how Events are handled in Episimmer.


Just to drive home these concept, we provide a real-world example.

1. Agents - A population of residents in an apartment.
2. Interactions - Couples going for a walk (consider each couple to not interact with other couples).
3. Locations - Park, Tennis Court, Club House, Swimming pool.
4. Events - Children (more than two) playing at any of the above locations.

.. note::
        The next two components are derivatives of the Events and Interactions components. We implement them separately
        and treat them as distinct components as they have important use cases in the real world.

One Time Events
~~~~~~~~~~~~~~~~~~
Similar to regular events, but they do not occur periodically.



Probabilistic Interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Building the Environment
--------------------------



Environment API
-----------------
* :doc:`Agent API<../modules/agent>`
* :doc:`Location API<../modules/location>`
* :doc:`Read File API<../modules/read_file>`

Coming soon...
