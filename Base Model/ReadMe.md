# Epidemic Simulation Platform

## Running
To run code from current directory : python Main.py \<path to folder containing required files\> 
<br>
<br>
The required files are as follows <br>
  -config.txt <br>
  -agents.txt <br>
  -interaction_files_list.txt <br>
  -All files specified in interaction_files_list.txt <br>
  -Generate_model.py (user defined script) <br>
<br>

### config.txt <br>
The format is shown with an example with values given in \<...\> and comments in {...}
<br>

    Number of worlds <30>   {Refers to the number of times simulation is avergaed on}
  
    Number of Days <30>     {Refers to the duration of a single simulation}
  
    Starting Exposed Percentage <0.3>   {Starting percentage of population that is exposed}
    
    Agent Parameter Keys <Agent Index:Type:Residence:HLA Type>                        {Refers to input parametrs in Agent}

    Contact Info Keys <Agent Index:Interacting Agent Index:Time Interval:Intensity>   {Refers to input parameters in Interaction list}
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

### interaction_files_list.txt <br>
This is a file containg a names of interaction files in order. The filenames must be enclosed in \<\> <br>
    
    Example 
    
    <monday.txt> <br>
    <tuesday.txt> <br>
    <wednesday.txt> <br>
    <thursday.txt> <br>
    <friday.txt> <br>
    <saturday.txt> <br>
    <sunday.txt> <br>

### Generate_model.py <br>
This will soon be changed. Models can be user defined here using library Model.py
On calling function generate_model(), corresponding model object should be returned.




    
