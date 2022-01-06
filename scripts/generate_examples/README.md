# Utility Files For Generating Examples

## 1. agents.py
Creates a *agent_file.txt/csv* file for the user with input specifications.

-n *no_of_agents*<br>
Example : creates a new file *filename* with 10 agents.<br>
```python
python3 agents.py filename -n 10
```
-p *Field "Propotions Dictionary of Field Types"* <br>
Example : creates a new file *filename* of 10 agents with HLA types A, B, C in 0.1 : 0.7 : 0.2 ratio.<br>
```python
python3 agents.py filename -n 10 -p HLA "{'A': 0.1, 'B': 0.7, 'C': 0.2}"
```
> NOTE: For multiple agent parameters just add another *-p Field2 "Propotions Dictionary of Field2 Types"*

-a *"add_line"*<br>
Example : appends the line *12:C* to the file *filename*. Creates a new file if it does not exist.
```python
python3 agents.py filename -a "12:C"
```
-c <br>
Example : clears the file *filename*
```python
python3 agents.py filename -c
```

---

## 2. config.py
Creates a config.txt template file for the user.
```python
python3 config.py
```

---

## 3. locations.py
Creates a *location_file.txt/csv* file for the user with input specifications.

-n *no_of_locations*<br>
Example : creates a new file *filename* with 10 locations.<br>
```python
python3 locations.py filename -n 10
```
-p *Field* *"Propotions Dictionary of Field Types"* <br>
Example : creates a new file *filename* of 10 locations with Ventilation types Good, Average, Poor in 0.1 : 0.7 : 0.2 ratio.<br>
```python
python3 locations.py filename -n 10 -p Ventilation "{'Good': 0.1, 'Average': 0.7, 'Poor': 0.2}"
```
> NOTE: For multiple location parameters just add another *-p Field2 "Propotions Dictionary of Field2 Types"* <br>

> -a *"add_line"* and -c function as mentioned in agents.py.

---

## 4. events.py
Creates a *events_file.txt/csv* file for the user with input specifications.

-ag *agent_indices* -loc *location_indices*<br>
Example : appends to file *filename* events where all *agent_indices* were present in the event at all *location_indices*<br>
```python
python3 events.py filename -ag "1,2" -loc "3,4"
```
>NOTE : you may put agents/location files made above as arguments as well.
```python
python3 events.py filename -ag agents.txt -loc locations.csv
```

>-a *"ADD_LINE"* and -c function as mentioned in agents.py.

> You need to add -c in the python command if you want to overwrite an existing file.<br>

-nh doesn't add a header at top of the events file filename. Can be used as follows:<br>
```python
python3 events.py filename.csv -ag "1,3,4" -loc "0,1,2"
python3 events.py filename.csv -ag agents.csv -loc "10" -nh
```

---

## 5. interactions.py
Creates a *interactions_file.txt/csv* file for the user with input specifications.

-from *agent1_indices* -to *agent2_indices*<br>
Example : appends to file *filename* interactions from all *agent1_indices* to *agent2_indices*<br>
```python
python3 interactions.py filename -from "1,2" -to "3,4"
```
>NOTE : you may put agents/location files made above as arguments as well.
```python
python3 interactions.py filename -from agents1.txt -to agents2.csv
```
>-a *"ADD_LINE"* and -c function as mentioned in agents.py

>You need to add -c in the python command if you want to overwrite an existing file.<br>

-nh doesn't add a header at top of the events file filename. Can be used as follows:<br>
```python
python3 interactions.py filename.csv -from "1,3,4" -to "0,1,2"
python3 interactions.py filename.csv -from agents.csv -to "10" -nh
```
-b adds interactions both ways i.e. from agent1_indices to agent2_indices and from agent2_indices to agent1_indices.<br>
```python
python3 interactions.py filename.csv -from "1,3,4" -to "0,1,2" -b
```
---
