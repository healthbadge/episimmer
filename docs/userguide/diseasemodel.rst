Disease Model
=====================================

* :ref:`Introduction - Disease Modelling`
* :ref:`Building the Disease Model`
    * :ref:`Stochastic Model`
    * :ref:`Scheduled Model`
    * :ref:`Additional Functionality`
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

Mathematical modelling in epidemiology provides understanding of the underlying mechanisms that influence the spread of disease and, in the process, it suggests control strategies/policies.
Both models in Episimmer follow the compartmental style of disease modelling. In compartmental models, the population under study is divided
into compartments and assumptions are made about the nature and time rate of transfer from one compartment to another.

Consider the SIR compartmental model where S, I and R represent the Susceptible, Infectious and Recovered (or Removed) populations.


.. figure:: ../_figures/SIR.png
    :width: 400
    :align: center

    SIR Compartmental model

When a new infection occurs, the individual infected moves from the susceptible class to the infectious class. The other process that occurs is that infectious individuals can enter the Recovered compartment.
Assume that β is the proportion of the population that every agent makes contact with per unit time. Then, the number of agents contacted by a single agent per unit time is βN, where N = S + I + R.  Since the
probability that a random contact by an infectious agent is with a susceptible is S/N, the number of new infections in unit time per infectious agent is (βN)(S/N), giving a rate of new infections (βN)(S/N)I = βSI.
This model also assumes that the time scale of the disease is much faster than the time scale of births and deaths so we shall not consider them. With all these assumptions, we have our differential equations for
all the states.

.. math::
        \frac{dS}{dt} &= - \beta S I

        \frac{dI}{dt} &= \beta S I - \gamma I

        \frac{dR}{dt} &= \gamma I


In this simple model the rate at which new infections occur is :math:`\beta S I` for some positive constant :math:`\beta` and recovery occurs at a rate :math:`\gamma I` for some positive constant :math:`\gamma`.


Refer these links for more information on Compartmental models

1. `Compartmental Models - Chapter 2 ~ Fred Brauer <https://link.springer.com/content/pdf/10.1007/978-3-540-78911-6_2.pdf>`_

2. `Compartmental Models - Wikipedia <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology>`_

The two transitions :math:`S \rightarrow I` and :math:`I \rightarrow R` differ because the first is a dependent transition while the second is independent. Dependent transitions are transitions that are directly dependent
on the population of Infectious states while Independent transition do not depend on the population of other states.


Example of a dependent and independent transition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assume an SIR compartmental model with :math:`\beta = 0.2` and :math:`\gamma = 0.3`,

For the Dependent Transition :math:`S \rightarrow I`, If we have a population of 90 agents in Susceptible state and 10 agents in Infectious state at :math:`T_n`,

An expectation of :math:`90 \times 0.02 \times 10 = 18` agents will transition to the Infectious compartment at :math:`T_{n+1}`.

For the Independent Transition :math:`I \rightarrow R`, If we have a population of 30 agents in Infectious state at :math:`T_n`,

An expectation of :math:`30 \times 0.3 = 9` agents will transition to the Recovered compartment at :math:`T_{n+1}`.



Difference between Stochastic and Scheduled Models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To reiterate, both types of models in Episimmer have compartments associated with them. They only differ by the transition rules.

Stochastic model allows us to implement compartmental models with probabilistic changes in state.
Stochastic model allows us to implement compartmental models with probabilistic changes in state. For example, an infected agent can recover with a probability of 0.2. A stochastic epidemic model can be used to understand disease transmission dynamics. Consider a disease that
is stable in its prevalence due to a constant supply of susceptible individuals. At some point in time, by chance, the disease may fail to be passed on before dying out, resulting in a disease-free population.
This can be captured by embedding stochasticity within the model.

Scheduled models have transitions that are scheduled based on a distribution. For example in the real world an infected person might take on average 10 days with a variance of 2 days to recover i.e. :math:`\mathcal{N}(\mu,\,\sigma^{2})` where :math:`\mu = 10` and :math:`\sigma^{2} = 2`.

.. note ::
        The platform’s simulations are not continuous as in, it does not solve the differential equations but simulates it out in discrete time steps using agents. As the time step becomes smaller and the number of agents increases the plot will tend towards a continuous one as produced by the equations.


.. note ::
        While Scheduled model's independent transitions are solely based on scheduled times, dependent transitions are dependent on probability of change (infection) just as in the Stochastic models.


Building the Disease Model
----------------------------

Both Stochastic and Scheduled models can be implemented by the user using the UserModel.py file. They must define compartments and transitions between compartments. Additionally, user defined functions must be created for Events (common for both regular Events and One-Time
Events) and Interactions (common for Individual Interactions and Probabilitic Interactions). These functions are relevant when we need to define Dependent transitions.

.. note ::
        This file is a mandatory file required for any simulation in Episimmer.



Stochastic Model
^^^^^^^^^^^^^^^^^^^

Let us look at how the Stochastic SIR model is implemented in Episimmer.

1. Create UserModel.py

First create a UserModel.py file with the class UserModel, inheriting the model.Stochastic Model (with relevant imports).

.. code-block:: python

    import episimmer.model as model

    class UserModel(model.StochasticModel):
      def __init__(self):
        pass

2. Create Compartments

Now, we shall create the compartments of the model. Let us take the SIR model. The states are then - Susceptible, Infected and Recovered.

.. code-block:: python
    :emphasize-lines: 5-12

    import episimmer.model as model

    class UserModel(model.StochasticModel):
      def __init__(self):
        individual_types=['Susceptible','Infected','Recovered']  # These are the states that will be used by the compartmental model
        infected_states=['Infected']  # These are the states that can infect
        state_proportion={        # This is the starting proportions of each state
                  'Susceptible':0.99,
                  'Infected':0.01,
                  'Recovered':0
                }
        model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)  # We use the inbuilt model in the package

We see all the states being defined in individual_types list, the infected states in infected_states list and the proportions of all states in the state_proportion dictionary.
Since 'Infected' is the only infected state, we shall add only the 'Infected' state in this list. We shall also start with a proportion of 99% of the agents in Susceptible
and 1% in Infected state. Then, we can pass these parameters to the parent's init function.

3. Handling Interactions in the Environment

Inter we need additional user-defined functions, particularly the probability of infection function for Individual and Probabilistic interactions. We shall handle both event types later.

.. code-block:: python

    # This function represents the probability of getting infected during a single interaction/contact

    def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
    	if contact_agent.state=='Infected':
    		return 0.1  #This is the probability of getting infected from contact in a time step if contact is infected
    	return 0 # If contact is not infected then the probability of them infecting you is 0

For every agent the current agent is in contact with, this function will be used to obtain a probability of infection.

We need to concern ourselves with only the first parameter p_infected_states_list as it is a list that can be used to return probabilities of infection for each state. This list will come from the UserModel class. The user must unpack the probabilities himself and then use them.

.. note::
        If you do not have any of the two kinds of Individual Interactions, you need not define this function

4. Defining transitions

We define the transitions using the function set_transition function which takes three parameters -

:code:`set_transition(from_state, to_state, transition_fn)`

It contains the from and the to states, along with a transition function defining whether it is a dependent or independent transition.

The transition functions available are

    * p_standard : Defines an independent transition. Takes and returns a fixed probability of transition.

    * p_function : Defines an independent transition. Takes a user-defined function and returns a probability of transition. This user defined function only takes current time step as parameter.

    * p_infection : Defines a dependent transition. Takes two parameters, the list of probabilities and the user-defined function corresponding to both types of Interactions and returns a probability of transition based on all the underlying interactions. The user-defined function is the function we created in step 3.


.. code-block:: python
    :emphasize-lines: 20-21

    import episimmer.model as model

    # This function represents the probability of getting infected during a single interaction/contact

    def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
    	if contact_agent.state=='Infected':
    		return 0.1  #This is the probability of getting infected from contact in a time step if contact is infected
    	return 0 # If contact is not infected then the probability of them infecting you is 0

    class UserModel(model.StochasticModel):
      def __init__(self):
        individual_types=['Susceptible','Infected','Recovered']  # These are the states that will be used by the compartmental model
        infected_states=['Infected']  # These are the states that can infect
        state_proportion={        # This is the starting proportions of each state
                  'Susceptible':0.99,
                  'Infected':0.01,
                  'Recovered':0
                }
        model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)  # We use the inbuilt model in the package
        self.set_transition('Susceptible', 'Infected', self.p_infection([0.1],probabilityOfInfection_fn))  # Adding S-> I transition which is redundant in this case as we use the event_contribute and event_recieve function
        self.set_transition('Infected', 'Recovered', self.p_standard(0.2))  # Adding the I->R transition

p_function may be used instead of p_standard to return probabilities depending on the time step. p_function will take a user-defined function with parameter current time step
in contrast with p_standard which takes only a float probability.


5. Handling Events in the Environment

Events are handled slightly differently. As mentioned previously, Events operate in two stages.

    i) All infected agents part of the event contribute to the ambient infection.

    ii) All susceptible agents are affected by the accumulated ambient infection.


Thus, we must define two user-defined functions for each step.

Let us define both here.

.. code-block:: python

    # The two functions event_contribute_fn and event_recieve_fn together control the spread of infection

    # This function states the amount an agent contributes to ambient infection in the region
    # note that only infected agents contibute to the ambient infection
    def event_contribute_fn(agent,event_info,location,current_time_step):
        if agent.state=='Infected':
          return 1
        return 0

    #This function states the probability of an agent becoming infected from the ambient infection
    def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
      beta=0.001
      return ambient_infection*beta

As shown above, we see that both functions return a value for a single agent. In the event_contribute_fn, if the agent is Infected,
he returns 1. This value will be accumulated and finally represent the ambient infection of the event. When it is 1, it actually represents the
total number of infected agents in the Event. In the event_recieve_fn, a probability of infection is returned based on the ambient infection.


.. note::
        Just like the user-defined function for Interactions, If you do not have any of the two kinds of Events, you need not define these functions.

6. Bringing them all together

Now, we can link the user-defined functions for Events using the set_event_contribution_fn() and set_event_recieve_fn(). Finally combining all these elements will form our UserModel.py

.. code-block:: python
    :emphasize-lines: 37-38

    import episimmer.model as model

    # The two functions event_contribute_fn and event_recieve_fn together control the spread of infection

    # This function states the amount an agent contributes to ambient infection in the region
    # note that only infected agents contibute to the ambient infection
    def event_contribute_fn(agent,event_info,location,current_time_step):
        if agent.state=='Infected':
          return 1
        return 0

    #This function states the probability of an agent becoming infected from the ambient infection
    def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
      beta=0.001
      return ambient_infection*beta

    # This function represents the probability of getting infected during a single interaction/contact

    def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
    	if contact_agent.state=='Infected':
    		return 0.1  #This is the probability of getting infected from contact in a time step if contact is infected
    	return 0 # If contact is not infected then the probability of them infecting you is 0

    class UserModel(model.StochasticModel):
      def __init__(self):
        individual_types=['Susceptible','Infected','Recovered']  # These are the states that will be used by the compartmental model
        infected_states=['Infected']  # These are the states that can infect
        state_proportion={        # This is the starting proportions of each state
                  'Susceptible':0.99,
                  'Infected':0.01,
                  'Recovered':0
                }
        model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)  # We use the inbuilt model in the package
        self.set_transition('Susceptible', 'Infected', self.p_infection([0.1],probabilityOfInfection_fn))  # Adding S-> I transition which is redundant in this case as we use the event_contribute and event_recieve function
        self.set_transition('Infected', 'Recovered', self.p_standard(0.2))  # Adding the I->R transition

        self.set_event_contribution_fn(event_contribute_fn)	#Setting the above defined fucntion into the model
        self.set_event_recieve_fn(event_recieve_fn)	#Setting the above defined fucntion into the model

        self.name='Stochastic SIR'


We can also provide a name for the model which would be used in visualization.


Scheduled Model
^^^^^^^^^^^^^^^^^^^



Additional Functionality
^^^^^^^^^^^^^^^^^^^^^^^^^^^
