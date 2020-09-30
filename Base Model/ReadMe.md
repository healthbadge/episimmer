# Epidemic Simulation Platform


## Dependencies

To install dependencies using pipenv run ```pipenv install```.

## Running
To run code from current directory : 

		python Main.py \<path to folder containing required files\> 
<br>
<br>
The required files are as follows <br>
  -config.txt <br>
  -agents.txt <br>
  -interaction_files_list.txt <br>
  -All files specified in interaction_files_list.txt <br>
  -Generate_model.py (user defined script) <br>
<br>
For example :  

		python Main.py Examples/Example_1/ <br>
will result in simulation of 100 agents being cycled through a weekly schedule for 30 days and averaged 10 times.
<br>


### config.txt <br>
The format is shown with an example with values given in \<...\> and comments in {...}
<br>

    Number of worlds <30>   {Refers to the number of times simulation is avergaed on}
  
    Number of Days <30>     {Refers to the duration of a single simulation}
  
    Starting Exposed Percentage <0.3>   {Starting percentage of population that is exposed} 
    
    Agent Parameter Keys <Agent Index:Type:Residence:HLA Type> 				{Refers to input parametrs in Agent}
	
    Agent list filename <agents.txt>							
	
    Interaction Info Keys <Agent Index:Interacting Agent Index:Time Interval:Intensity>	{Refers to input parameters in Interaction list}
	
    Interaction Files list filename <interaction_files_list.txt>
	
    Location Parameter Keys <Location Index:Type:Ventilation:Roomsize:Capacity>		{Refers to input parametrs for Locations}
	
    Location list filename <locations.txt>
	
    Event Parameter Keys <Location Index:Agents:Time Interval>				{Refers to input parametrs in Event list}
	
    Event Files list filename <event_files_list.txt>
<br>
Agent parameter Keys has to match with agent.txt and Contact Info Keys has to match with the files mentione din interaction_files_list.txt
<br>

### agents.txt
The format is show with an example where comments given in {...}
The code is can take in an infinite number of parameters. Only requirment is 'Agent Index' which must be unique for every agent.
<br>

    100 {integer referring to number agents}
    
    Agent Index:Type:Residence:HLA Type     {Refers to input parametrs for agent separated by ':' and must match config.txt}
    
    12:Student:Dorm A:A1
    
    7:Teacher:Outside:B3
    
    ...

<br>

### locations.txt
The format is show with an example where comments given in {...}
The code is can take in an infinite number of parameters. Only requirment is 'Location Index' which must be unique for every location.
<br>

    10 {integer referring to number of locations}
    
    Location Index:Type:Ventilatione:Room size    {Refers to input parametrs for location separated by ':' and must match config.txt}
    
    12:Classroom:0.6:20
    
    7:Lab:0.4:10
    
    3:Cafeteria:120
    
    ...

<br>

### interaction_files_list.txt and event_files_list.txt<br>
This is a file containg a names of interaction files in order. The filenames must be enclosed in \<\> . The code cycles throught the files till the number of days run out. <br>
<br> 
Example :
    
    <monday.txt> 
    <tuesday.txt> 
    <wednesday.txt> 
    <thursday.txt> 
    <friday.txt> 
    <saturday.txt> 
    <sunday.txt> 
    
### interaction file <br>
The format of an interaction file has been shown with an example. The interactions are directional and must require keys 'Agent Index' and 'Interacting Agent Index'. An interaction can be user defined provided it is instantianted in config.txt.
<br>
      
      30  {Integer denoting number of interactions}
      
      Agent Index:Interacting Agent Index:Time Interval:Intensity   {Refers to input parameters in Interaction list separated by ':' and must match config.txt}
      
      12:7:10:0.7
      
      12:6:10:0.7

      ...
      
<br>
A simple example would be a class that goes on for 1 hour. Then all agents will require bi-directional(A:B and B:A) interactions with time interval 60. Furthermore class size, ventilation can be parameters. All these parameters can be used in the user defined model.

### event file <br>
The format of an event file has been shown wiht an example. An event must contain 'Location Index' and 'Agents' which corresponds to 'Agent Index' of agents who have participate din the event. An event is a complete intercation of agents at a location. For example a classroom will be the location while Physics 101 will be an event consisting of the studnets and the teacher. An event can be user defined provided it is instantianted in config.txt.
<br>
	
	30 {Integer denoting number of events}
	
	Location Index:Agents:Time Interval {Refers to user defined defintion of an event. oarametrs are separated by ':' and must match config.txt}
	
	10:3,4,34,45,67,81:40
	
	11:2,3,6,44,55,89,29,4:40
	
	...
<br>

### Generate_model.py <br>
This will soon be changed. Models can be user defined here using library Model.py <br>
There are two types of models that can currently be defined
<br>
#### Stochastic Model <br>
Example

	individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']
	infected_states=['Symptomatic','Asymptomatic']
	model=Model.StochasticModel(individual_types,infected_states)
	model.set_transition('Susceptible', 'Exposed', model.p_infection(0.3,0.1,probabilityOfInfection_fn))
	model.set_transition('Exposed', 'Symptomatic', model.p_standard(0.15))
	model.set_transition('Exposed', 'Asymptomatic', model.p_standard(0.2))
	model.set_transition('Symptomatic', 'Recovered', model.p_standard(0.2))
	model.set_transition('Asymptomatic', 'Recovered', model.p_standard(0.2))
	
	model.set_contribution_fn(contribute_fn)
	model.set_recieve_fn(recieve_fn)

	return model
	
	

<br>
#### Scheduled Model  <br>
Example 

	model=Model.ScheduledModel()
	model.insert_state('Susceptible',None, None,model.p_infection(0.3,0.1,probabilityOfInfection_fn,{'Exposed':1}),False)
	model.insert_state('Exposed',5,2,model.scheduled({'Symptomatic':0.7,'Asymptomatic':0.3}),false)
	model.insert_state('Symptomatic',7,1,model.scheduled({'Recovered':0.7, 'ICU':0.3}),True)
	model.insert_state('ICU',10,5,model.scheduled({'Recovered':0.1,'Dead':0.9}),False)
	model.insert_state('Asymptomatic',6,3,model.scheduled({'Recovered':1}),True)
	model.insert_state('Recovered',None, None,model.scheduled({'Recovered':1}),False)
	model.insert_state('Dead',None, None,model.scheduled({'Dead':1}),False)
	
	model.set_contribution_fn(contribute_fn)
	model.set_recieve_fn(recieve_fn)
	
	return model
	
On calling function generate_model(), corresponding model object should be returned.
<br>
Note : User can use all parameters given in agents.txt and intercation files.  <br>
Below is a n example of probabilityOfInfection_fn function. 

   	#Example 1
		if contact_agent.state=='Symptomatic':
			return math.tanh(float(c_dict['Time Interval']))*p_inf_symp
		elif contact_agent.state=='Asymptomatic':
			return math.tanh(float(c_dict['Time Interval']))*p_inf_asymp
		else:
			return 0

	#Example 2
		if contact_agent.state=='Symptomatic':
			return math.tanh(float(c_dict['Time Interval'])*float(c_dict['Intensity']))*p_inf_symp*agent.info_dict['Innate Suscptibility']
		elif contact_agent.state=='Asymptomatic':
			return math.tanh(float(c_dict['Time Interval'])*float(c_dict['Intensity']))*p_inf_asymp*agent.info_dict['Innate Suscptibility']
		else:
			return 0




    
