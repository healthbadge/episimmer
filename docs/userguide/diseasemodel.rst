Disease Model
=====================================

* `Introduction - Disease Modelling`_
* `Building the Disease Model`_
* :doc:`Disease Model API<../modules/model>`

Introduction - Disease Modelling
-----------------------------------

Disease models are used to model the spread of disease across agents in the environment. Agents are the disease carriers and all the different types of interactions present facilitate the spread of infection.

Agents have a disease state associated with them to represent whether they are infectious or not. According to a user-defined
disease model, an agent transitions across states depending on his contacts.


In Episimmer, There are two basic types of disease models -

1. **Stochastic Model**

2. **Scheduled Model**


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

*Stochastic models* allows us to implement compartmental models with probabilistic changes in state. For example, an infected agent can recover with a probability of 0.2. A stochastic epidemic model can be used to understand disease transmission dynamics. Consider a disease that
is stable in its prevalence due to a constant supply of susceptible individuals. At some point in time, by chance, the disease may fail to be passed on before dying out, resulting in a disease-free population.
This can be captured by embedding stochasticity within the model.


Probabilistic transitions are simple and easy to analyse and understand. But in the real world there is a schedule change in states. For example, people recover as a distribution in the number of days after getting infected. It is not directly a probability of the total number of people infected.

In the case of Covid-19, one usually starts showing symptoms at around 4-5 days after getting infected. This can also be seen in delayed spikes in cases after certain events. If we consider a probabilistic model we cannot accurately capture such phenomena and thus we introduce the *Scheduled model* where
one can schedule changes in state based on distributions. For example in the real world an infected person might take on average 10 days with a variance of 2 days to recover i.e. :math:`\mathcal{N}(\mu,\,\sigma^{2})` where :math:`\mu = 10` and :math:`\sigma^{2} = 2`.

.. note ::
        The platform’s simulations are not continuous as in, it does not solve the differential equations but simulates it out in discrete time steps using agents. As the time step becomes smaller and the number of agents increases the plot will tend towards a continuous one as produced by the equations.


.. note ::
        While Scheduled model's independent transitions are solely based on scheduled times, dependent transitions are dependent on probability of change (infection) just as in the Stochastic models.

.. note::
    Internally in Episimmer, for an agent, the probabilities of infection from Individual interactions, Probabilistic interactions, Events and One-Time Events are
    all stored with the agent for a time step. The agent's next disease state at the time step is then calculated based on these stored probabilities.



Building the Disease Model
----------------------------

Both Stochastic and Scheduled models can be implemented by the user using the UserModel.py file. They must define compartments and transitions between compartments. Additionally, user defined functions must be created for Events (common for both regular Events and One-Time
Events) and Interactions (common for Individual Interactions and Probabilitic Interactions). These functions are relevant when we need to define Dependent transitions.

.. note ::
        This file is a mandatory file required for any simulation in Episimmer.

* `Stochastic Model`_
* `Scheduled Model`_
* `Additional Functionality`_

Stochastic Model
^^^^^^^^^^^^^^^^^^^

Let us look at how the Stochastic SIR model is implemented in Episimmer.

1. **Create UserModel.py**

First create a UserModel.py file with the class UserModel, inheriting the model.Stochastic Model (with relevant imports).

.. code-block:: python
    :linenos:

    import episimmer.model as model

    class UserModel(model.StochasticModel):
      def __init__(self):
        pass

2. **Create Compartments**

Now, we shall create the compartments of the model. Let us consider the SIR model. The states are then - Susceptible, Infected and Recovered.

.. code-block:: python
    :linenos:
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


3. **Defining transitions**

We define the transitions using the function set_transition function which takes three parameters -

:code:`set_transition(from_state, to_state, transition_fn)`

It contains the from and the to states, along with a transition function defining whether it is a dependent or independent transition.

The transition functions available are

    * p_standard : Defines an independent transition. Takes and returns a fixed probability of transition.

    * p_function : Defines an independent transition. Takes a user-defined function and returns a probability of transition. This user defined function only takes current time step as parameter.

    * p_infection : Defines a dependent transition. Takes two parameters, the list of probabilities and the user-defined function, corresponding to Individual and Probabilistic Interactions. Returns a probability of transition based on all the underlying interactions.


.. code-block:: python
    :linenos:
    :emphasize-lines: 13-14

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
        self.set_transition('Susceptible', 'Infected', self.p_infection(None, None))  # Adding S-> I transition which is redundant in this case as we use the event_contribute and event_recieve function
        self.set_transition('Infected', 'Recovered', self.p_standard(0.2))  # Adding the I->R transition


For now, just pass None, None as the two parameters in p_infection.

p_function may be used instead of p_standard to return probabilities depending on the time step. It takes a user-defined function with parameter current time step
in contrast with p_standard which takes only a float probability. For example -


.. code-block:: python
    :linenos:

    def fn2(current_time_step): #People going into ICU decreases due to better drugs
      return max(0.02,0.1-current_time_step*0.001)
    .
    .
    .
    .

    self.set_transition('Infected', 'ICU', self.p_function(fn2))




4. **Handling Interactions in the Environment**

For interactions, we need additional user-defined functions, particularly the probability of infection function for Individual and Probabilistic interactions.

.. code-block:: python
    :linenos:

    # This function represents the probability of getting infected during a single interaction/contact

    def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
      if contact_agent.state=='Infected':
        return 0.1  #This is the probability of getting infected from contact in a time step if contact is infected
      return 0 # If contact is not infected then the probability of them infecting you is 0

For every agent the current agent is in contact with, this function will be used to obtain a probability of infection.

We need to concern ourselves with only the first parameter p_infected_states_list as it is a list that can be used to return probabilities of infection for each state. This list will come from the UserModel class. The user must unpack the probabilities himself and then use them.

.. note::
        If you do not have any of the two kinds of Individual Interactions, you need not define this function

5. **Handling Events in the Environment**

Events are handled slightly differently. As mentioned previously, Events operate in two stages.

    i) All infected agents part of the event contribute to the ambient infection.

    ii) All susceptible agents are affected by the accumulated ambient infection.


Thus, we must define two user-defined functions for each step.

Let us define both here.

.. code-block:: python
    :linenos:

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

6. **Bringing them all together**

Now, we can link the user-defined functions for both Interactions and Events. Finally combining all these elements will form our UserModel.py

.. code-block:: python
    :linenos:
    :emphasize-lines: 21, 34, 37-38

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
        return p_infected_states_list[0]  #This is the probability of getting infected from contact in a time step if contact is infected
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

        self.set_event_contribution_fn(event_contribute_fn)  #Setting the above defined fucntion into the model
        self.set_event_recieve_fn(event_recieve_fn)  #Setting the above defined fucntion into the model

        self.name='Stochastic SIR'

We link the probability of interaction function and the optional list of probabilities in the p_infection function. Since we pass a list, we might as well use it. Thus, in line 21, we see the the first
element of the list being used (Since there is only a single infectious state, we pass only a single value in the list).

Then, we link the event functions with the set_event_contribution_fn() and set_event_recieve_fn() functions.

We can also provide a name for the model which would be used in visualization.

.. note::
    You are now equipped with the right tools to implement your own Stochastic Model. Try it out yourself!
    Check out the :doc:`examples page<examples>` to get some ideas.


Scheduled Model
^^^^^^^^^^^^^^^^^^^
Now, let us look at how the Scheduled SIR model is implemented in Episimmer.

1. **Create UserModel.py**

First create a UserModel.py file with the class UserModel, inheriting the model.ScheduledModel Model (with relevant imports).

.. code-block:: python
    :linenos:

    import episimmer.model as model

    class UserModel(model.ScheduledModel):
      def __init__(self):
        model.ScheduledModel.__init__(self)


2. **Inserting States - Defining Compartments and Transitions**

Let us consider the SIR model. The states are then - Susceptible, Infected and Recovered.

We use the insert_state function to add a compartment and define the transitions from this state. As we are dealing with the Scheduled model,
we must schedule the number of days for an agent to reside/stay in the state. We use the Normal distribution here to specify the scheduled days.
Hence, we must pass the mean and variance as parameters to this function to set up the Normal distribution.

:code:`insert_state(state, mean, vary, transition_fn, infected_state, proportion)`

* state : State name

* mean, vary : Parameters of normal distributions defining number of days to remain in state

* transition_fn : Transition function from current state to next state. Defines whether it is a dependent or independent transition.

* infected_state : Boolean representing whether the state is an infectious state.

* proportion : Initial proportion of state

The transition functions available are

    * scheduled : Defines an independent transition. Takes a dictionary with the keys as the next states and the values as the probability of transitioning to that state. Returns a state and scheduled time based on mean and variance passed to the insert_state function.

    * p_infection : Defines a dependent transition. Takes three parameters. First two parameters are the list of probabilities and the user-defined function, corresponding to Individual and Probabilistic Interactions. The third parameter is a dictionary with the keys as the next states and the values as the probability of transitioning to that state. Returns a state and scheduled time based on mean and variance passed to the insert_state function and also depends on the underlying interactions.



Let us consider the SIR model. The states are then - Susceptible, Infected and Recovered.

.. code-block:: python
    :linenos:
    :emphasize-lines: 6-8

    import episimmer.model as model

    class UserModel(model.ScheduledModel):
      def __init__(self):
        model.ScheduledModel.__init__(self)
        self.insert_state('Susceptible',None, None,self.p_infection(None,None,{'Infected':1}),False,0.99)
        self.insert_state('Infected',6,3,self.scheduled({'Recovered':1}),True,0.01)
        self.insert_state('Recovered',0, 0,self.scheduled({'Recovered':1}),False,0)


insert_state in lines 6-8 have both the compartments and the transitions defined unlike how we define them separately

As shown, the first transition is dependent and thus we use the p_infection function. For now, just pass None, None as the two parameters in p_infection.

In real life scenarios, not all distributions are symmetric about a mean (not all are Normal distributions). Custom distributions provide flexibility in terms of scheduling changes in state for user defined distributions. We can implement this using the insert_state_custom function instead of the insert_state function.

:code:`insert_state_custom(state, fn, transition_fn, infected_state, proportion)`

Instead of passing mean and variance, we pass a user-defined function. This function takes the current time step as parameter.

.. code-block:: python
    :linenos:

    def fn1(current_time_step):
      r=random.random()
      if r<0.2:
        return 2
      elif r<0.8:
        return 3
      else:
        return 4
    .
    .
    .
    .

    self.insert_state_custom('Recovered',fn1,self.scheduled({'Recovered':1}),False,0)


3. **Handling Interactions in the Environment**

For interactions, we need additional user-defined functions, particularly the probability of infection function for Individual and Probabilistic interactions.

.. code-block:: python
    :linenos:

    # This function represents the probability of getting infected during a single interaction/contact

    def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
      if contact_agent.state=='Infected':
        return 0.1  #This is the probability of getting infected from contact in a time step if contact is infected
      return 0 # If contact is not infected then the probability of them infecting you is 0

For every agent the current agent is in contact with, this function will be used to obtain a probability of infection.

We need to concern ourselves with only the first parameter p_infected_states_list as it is a list that can be used to return probabilities of infection for each state. This list will come from the UserModel class. The user must unpack the probabilities himself and then use them.

.. note::
        If you do not have any of the two kinds of Individual Interactions, you need not define this function

4. **Handling Events in the Environment**

Events are handled slightly differently. As mentioned previously, Events operate in two stages.

    i) All infected agents part of the event contribute to the ambient infection.

    ii) All susceptible agents are affected by the accumulated ambient infection.


Thus, we must define two user-defined functions for each step.

Let us define both here.

.. code-block:: python
    :linenos:

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

5. **Bringing them all together**

Now, we can link the user-defined functions for both Interactions and Events. Finally combining all these elements will form our UserModel.py


.. code-block:: python
    :linenos:
    :emphasize-lines: 21, 27, 31-32

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
        return p_infected_states_list[0]  #This is the probability of getting infected from contact in a time step if contact is infected
      return 0 # If contact is not infected then the probability of them infecting you is 0

    class UserModel(model.ScheduledModel):
      def __init__(self):
        model.ScheduledModel.__init__(self)
        self.insert_state('Susceptible',None, None,self.p_infection([0.1],probabilityOfInfection_fn,{'Infected':1}),False,0.99)
        self.insert_state('Infected',6,3,self.scheduled({'Recovered':1}),True,0.01)
        self.insert_state('Recovered',0, 0,self.scheduled({'Recovered':1}),False,0)

        self.set_event_contribution_fn(event_contribute_fn)
        self.set_event_recieve_fn(event_recieve_fn)

        self.name='Scheduled SIR'

We link the probability of interaction function and the optional list of probabilities in the p_infection function. Since we pass a list, we might as well use it. Thus, in line 21, we see the the first
element of the list being used (Since there is only a single infectious state, we pass only a single value in the list).

Then, we link the event functions with the set_event_contribution_fn() and set_event_recieve_fn() functions.


We can also provide a name for the model which would be used in visualization.

.. note::
    You are now equipped with the right tools to implement your own Scheduled Model. Try it out yourself!
    Check out the :doc:`examples page<examples>` to get some ideas.


Additional Functionality
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**External Prevalence**

In the real world, infections can occur due to agents going outside the community that is being simulated. It is not possible to model all the interactions for a community of agents that is not completely
closed. This can be accounted for with external prevalence.

For either of the two models, we have the function set_external_prevalence_fn function.

:code:`set_external_prevalence_fn(fn)`

fn is the user-defined function for external prevalence. It takes the current agent and time step as parameters.


One can also set up conditions as to who gets infected and how much as well. This example shows external prevalence based on the compliance of the agent.

.. code-block:: python
    :linenos:
    :emphasize-lines: 3-9, 18

    import episimmer.model as model

    def external_prevalence(agent, current_time_step):
      if(agent.info['Compliance'] == 'High'):
        return 0.1
      elif(agent.info['Compliance'] == 'Medium'):
        return 0.2
      elif(agent.info['Compliance'] == 'Low'):
        return 0.35

    class UserModel(model.ScheduledModel):
      def __init__(self):
        model.ScheduledModel.__init__(self)
        self.insert_state('Susceptible',None, None,self.p_infection([None,None],None,{'Infected':1}),False,0.99)
        self.insert_state('Infected',6,3,self.scheduled({'Recovered':1}),True,0.01)
        self.insert_state('Recovered',0, 0,self.scheduled({'Recovered':1}),False,0)

        self.set_external_prevalence_fn(external_prevalence)


**Symptomatic States**

You may also set the states that represent the symptomatic states of the disease model.

.. code-block:: python
    :linenos:
    :emphasize-lines: 21

    class UserModel(model.StochasticModel):
      def __init__(self):
        individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']
        infected_states=['Asymptomatic','Symptomatic']
        state_proportion={
                  'Susceptible':0.99,
                  'Exposed':0,
                  'Recovered':0,
                  'Asymptomatic':0,
                  'Symptomatic':0.01
                }
        model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
        self.set_transition('Susceptible', 'Exposed', self.p_infection(None,None))
        self.set_transition('Exposed', 'Symptomatic', self.p_standard(0.15))
        self.set_transition('Exposed', 'Asymptomatic', self.p_standard(0.2))
        self.set_transition('Symptomatic', 'Recovered', self.p_standard(0.1))
        self.set_transition('Asymptomatic', 'Recovered', self.p_standard(0.1))

        self.set_event_contribution_fn(event_contribute_fn)
        self.set_event_recieve_fn(event_recieve_fn)
        self.set_symptomatic_states(['Symptomatic'])

This is useful for modules such as the Testing Policy. You may choose to test the agents that are only symptomatic
(showing visible signs of having the disease) rather than random agents. More on how to setup these policies :doc:`here<policy>`.
