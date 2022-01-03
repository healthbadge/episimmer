# Miscellaneous
The examples under this directory showcase additional functionality of episimmer like External Prevalence, List of Lists and Custom Distributions for Scheduled disease models.

* External Prevalence : It refers to the prevalence of disease outside the environment defined by the user. See more in [Tutorial 2.1](https://docs.google.com/document/d/1vn8xc95bCQ7K09lMuc3ijHfSeDPa6Nd28tko-19SlnQ/edit).
* List of Lists capability : Episimmer can handle a list of File lists in the config file and run them concurrently. This is to provide the ability to simulate timetable-like environments. For example, Student Timetables for each class are different but the classes are conducted at the same time.
* Custom Distributions : In real life scenarios, not all distributions are symmetric about a mean (not all are Normal distributions). Thus, for Scheduled models, Custom distributions provide flexibility in terms of scheduling changes in state for user defined distributions. More on custom distributions in [Tutorial 2.1](https://docs.google.com/document/d/1vn8xc95bCQ7K09lMuc3ijHfSeDPa6Nd28tko-19SlnQ/edit).

We also include examples that showcase the level of complexity and creativity that the user can harness with Episimmer.


## Running
To run an example :

		cd examples/Miscellaneous
		python ../../src/Main.py 3D_Cellular_Automaton
