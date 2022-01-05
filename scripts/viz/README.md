# Visualization


## 1. view_interaction_graph.py
Saves a HTML file with a graphic interaction graph.<br>
-n *no_of_agents*<br>
-f *file_name* <br>
Example : 1000 agents with interaction filename "interaction_list.txt"
```python
python3 view_interaction_graph.py -n 1000 -f interactions.txt
```

## 2. view_model.py
Saves a HTML file with a graphic user defined disease model. [NOTE : Currently works only for Stochastic Models]<br>
-f *file_name* <br>
Example : Usermodel filename -f "UserModel.py"
```python
python3 view_model.py -f UserModel.py
```
