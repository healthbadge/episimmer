# One_Time_Event
This example of a one time event uses the Stochastic SIR model where the agents can interact with each other either via the non empty empty or the one time event.

The one time event has to be configured in a seperate file which then needs to be included in the config.txt file.

While configuring the file containing the one time event, along with specifying the agents that are a part of it, it is also necessary to specify the times steps which are involved in the event.


## Significance of One_Time_Event
In Episimmer, an event is enforced by calling it cyclicly in an order specified in the event_files_list.txt, and these events take place throughout the specified number of time steps.

At times, in realistic scenarios such as in a university, there are some events that do not take place that freqeuntly. For instance, cultural week might be for only one week within a span of two months.

Hence, the concept of one time events has been introduced in this example which helps us specify such infrequent and exceptional events as part of the considered time period. 


## Running One_Time_Event
To run code from current directory :

		cd examples/Interaction_Spaces
		python ../src/Main.py One_Time_Event
		
