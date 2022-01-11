
Environment
=====================================

* :ref:`Introduction - Environment`
* :ref:`Building the Environment`
* :ref:`Environment API`

Introduction - Environment
----------------------------
Episimmer is an agent-based simulation tool. An agent-based model simulates a system consisting of individual agents
behaving independently in order to understand this underlying system. In our case, the underlying system is the disease
spreading over a population. We call this system, the *Environment*.

The components of the environment include :

* :ref:`Agents`
* :ref:`Interactions`
* :ref:`Events`
* :ref:`Locations`
* :ref:`One Time Events`
* :ref:`Probabilistic Interactions`

.. note::
        Agents are the people or the population in the simulation and they are the carriers of the disease. All the
        other components exist to facilitate the spread of the disease.

Agents
~~~~~~~~
Agent form the core of the simulation. Without them, there is no simulation possible in Episimmer. Each agent can have
any number of attributes to distinguish them from the others and there are multiple possibilities of using these attributes
to manage their behaviour in the environment and how they are affected by it. For example, an agent can be a student in
a university or an office worker. Their attributes can differ by age, sex, blood type etc. Episimmer can model the agents
with any number of attributes and is only limited by computational resources.


Interactions
~~~~~~~~~~~~~~~~


Events
~~~~~~~~



Locations
~~~~~~~~~~~



.. note::
        Just to drive home this concept, we provide a real-world example.

        1. Agents - A population of residents in an apartment.
        2. Interactions - Couples going for a walk (consider each couple to not interact with other couples).
        3. Locations - Park, Tennis Court, Club House, Swimming pool.
        4. Events - Children (more than two) playing at any of the above locations.

.. note::
        The next two components are derivatives of the Events and Interactions components. We include them as separate
        components as they have important use cases in the real world.

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
