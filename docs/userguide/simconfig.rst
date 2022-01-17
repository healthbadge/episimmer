
Simulation Configuration
=====================================

The basic configuration of the simulation along with connecting the appropriate files required for execution are passed in the config.txt file.
The files specified here describe the Episimmer Environment i.e. The agents, interactions, locations, events etc.

All the parameters of the configuration can be set in the mandatory config.txt file. The structure is defined as follows :

.. code-block:: text
    :caption: config.txt structure

    Random Seed <>
    Number of worlds <>
    Number of Days <>
    Agent Parameter Keys <>
    Agent list filename <>
    Interaction Info Keys <>
    Interaction Files list filename <>
    Probabilistic Interaction Files list filename <>
    Location Parameter Keys <>
    Location list filename <>
    Event Parameter Keys <>
    Event Files list filename <>
    One Time Event filename <>


1. **Random seed (integer)** : Random seed refers to initializing the random number generator. When initialized with the same value, you get deterministic outputs in a stochastic setting. This can be used to get reproducible simulation results.

.. code-block:: text
    :caption: Random Seed set to 1
    :emphasize-lines: 1

    Random Seed <1>
    Number of worlds <>
    Number of Days <>
    Agent Parameter Keys <>
    Agent list filename <>
    Interaction Info Keys <>
    Interaction Files list filename <>
    Probabilistic Interaction Files list filename <>
    Location Parameter Keys <>
    Location list filename <>
    Event Parameter Keys <>
    Event Files list filename <>
    One Time Event filename <>

2. **Number of Worlds (integer) [Required parameter]** : The number of worlds allows the user to create ‘n’ independent simulations and obtain the averaged result at the end of all simulations. It is important to pass more worlds or run more simulations to obtain a more accurate representation of the disease spread for a given environment. It can effectively smoothen the epidemic trajectory.

.. code-block:: text
    :caption: Number of worlds set to 10
    :emphasize-lines: 2

    Random Seed <1>
    Number of worlds <10>
    Number of Days <>
    Agent Parameter Keys <>
    Agent list filename <>
    Interaction Info Keys <>
    Interaction Files list filename <>
    Probabilistic Interaction Files list filename <>
    Location Parameter Keys <>
    Location list filename <>
    Event Parameter Keys <>
    Event Files list filename <>
    One Time Event filename <>

3. **Number of days (integer) [Required parameter]** : The number of days allows the user to determine the number of timesteps to run the simulations.

.. code-block:: text
    :caption: Number of days set to 30
    :emphasize-lines: 3

    Random Seed <1>
    Number of worlds <10>
    Number of Days <30>
    Agent Parameter Keys <>
    Agent list filename <>
    Interaction Info Keys <>
    Interaction Files list filename <>
    Probabilistic Interaction Files list filename <>
    Location Parameter Keys <>
    Location list filename <>
    Event Parameter Keys <>
    Event Files list filename <>
    One Time Event filename <>

4. **Agent Parameter Keys (string) [Required parameter]** : In order to ensure consistency with respect to the data stored in agents.txt, it is required to enter the appropriate parameter keys that are used to describe the agents in the agent.txt file. Multiple keys are separated by a ‘:’.

5. **Agents list File Name (string) [Required parameter]**: This field is the name of the file, typically called agents.txt in our examples, containing all the information pertaining to the participating agents. The previous field ensures that the keys mentioned there match the keys present in this file. You may also provide a .csv file instead of a .txt file.

.. code-block:: text
    :caption: Agent parameters with Agents list file
    :emphasize-lines: 4,5

    Random Seed <1>
    Number of worlds <10>
    Number of Days <30>
    Agent Parameter Keys <Agent Index:Age>
    Agent list filename <agents.txt>
    Interaction Info Keys <>
    Interaction Files list filename <>
    Probabilistic Interaction Files list filename <>
    Location Parameter Keys <>
    Location list filename <>
    Event Parameter Keys <>
    Event Files list filename <>
    One Time Event filename <>


    Location Parameter Keys <Location Index:Type:Ventilation:Roomsize:Capacity>
    Location list filename <locations.txt>
    Event Parameter Keys <Location Index:Agents:Time Interval>
    Event Files list filename <event_files_list.txt>
    One Time Event filename <>

6. **Interaction Info Keys (string)** : This field works in a similar manner as the Agent Info Keys. Any interaction file provided, whether interactions or probabilistic interactions, must have matching parameter keys in the files and the config.txt file.

.. note::
        If you have both types of interactions, you should use Agent Index:Interacting Agent Index key, omitting the Probability:Agents parameter keys. Please note that if you have additional user-defined parameters (like ‘duration’), it must be present in both the interaction files and appended to the Interaction Info Keys. Check out the example - :ref:`Double_Style_Interactions` for an implementation of the same.

7. **Interactions File List filename (string)** : This field takes the interaction file list filename(s). It refers to a text file that contains the list of other individual interaction files that run at each timestep. You may also pass multiple interactions file list filenames separated by a comma.

8. **Probabilistic Interactions Files List filename (string)** : Similar to interactions file list filename but for probabilistic interactions. Single or multiple text files can be passed here.

.. code-block:: text
    :caption: Interaction parameters with corresponding files list file for interactions and probabilistic interactions.
    :emphasize-lines: 6,7,8

    Random Seed <1>
    Number of worlds <10>
    Number of Days <30>
    Agent Parameter Keys <Agent Index:Age>
    Agent list filename <agents.txt>
    Interaction Info Keys <Agent Index:Interacting Agent Index:Time Interval:Intensity>
    Interaction Files list filename <interaction_files_list.txt>
    Probabilistic Interaction Files list filename <probability_interaction_files_list.txt>
    Location Parameter Keys <>
    Location list filename <>
    Event Parameter Keys <>
    Event Files list filename <>
    One Time Event filename <>

9. **Location Parameter Keys (string)** : This field works in a similar manner as the other Info Keys parameters. Parameter Keys are passed to be consistent with the keys used in the locations text file.

10. **Location List filename (string)** : This field takes the name of a single text file containing the list of all the locations present in the environment.

.. code-block:: text
    :caption: Location parameters with locations list file
    :emphasize-lines: 9, 10

    Random Seed <1>
    Number of worlds <10>
    Number of Days <30>
    Agent Parameter Keys <Agent Index:Age>
    Agent list filename <agents.txt>
    Interaction Info Keys <Agent Index:Interacting Agent Index:Time Interval>
    Interaction Files list filename <interaction_files_list.txt>
    Probabilistic Interaction Files list filename <probability_interaction_files_list.txt>
    Location Parameter Keys <Location Index:Type:Ventilation:Roomsize:Capacity>
    Location list filename <locations.txt>
    Event Parameter Keys <>
    Event Files list filename <>
    One Time Event filename <>

11. **Event parameter keys (string)** : This field works in a similar manner as the other Info Keys parameters. Any event file provided, whether regular events or one time events, must have matching parameter keys in the files and the config.txt file.

.. note::
        While using One Time Events, skip the Timestep parameter in the event parameter keys in config.txt. Similar to interactions, if using both types of events, you must have the same keys in both files (excluding the Timestep parameter). Check out the example :ref:`One_Time_Event` for an implementation of the same.

12. **Event Files List Filename (string)** : This field takes the event files list filename. Similar to Interaction and Probabilistic Interactions Files list, it is a text file for events.

13. **One Time Event Filename (string)** : This field contains the name of a single text file that has events that run at time steps specified by the user.

.. code-block:: text
    :caption: Event parameters with event files list file and one time event file
    :emphasize-lines: 11,12,13

    Random Seed <1>
    Number of worlds <10>
    Number of Days <30>
    Agent Parameter Keys <Agent Index:Age>
    Agent list filename <agents.txt>
    Interaction Info Keys <Agent Index:Interacting Agent Index:Time Interval>
    Interaction Files list filename <interaction_files_list.txt>
    Probabilistic Interaction Files list filename <probability_interaction_files_list.txt>
    Location Parameter Keys <Location Index:Type:Ventilation:Roomsize:Capacity>
    Location list filename <locations.txt>
    Event Parameter Keys <Location Index:Agents:Time Interval>
    Event Files list filename <event_files_list.txt>
    One Time Event filename <one_time_event.txt>


Note that one can include multiple lists of file lists that run parallelly. For example in a university some events occur everyday but some occur only on fixed days.
In that case an event like a chemistry class can occur in the 'monday.txt' file of our ‘event_files_list1.txt’ while the mess event which occurs everyday will be a part of ‘mess.txt’ in ‘event_files_list2.txt’.
Both event file lists can be added in the config.txt file separated by a ‘,’. For an implementation, check out the config.txt of the :ref:`List_Of_Lists` example. This implementation shows two sets of cycling events.
One set that cycles every 7 days and another that alternates every 2 days.

This functionality is available to cycling components of the Environment i.e. Events, Individual interactions and Probabilistic Interactions.
