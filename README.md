# Episimmer : Epidemic Simulation Platform
Powered by [HealthBadge](https://www.healthbadge.org/) <br>

Episimmer is an Epidemic Simulation Platform. It aims to provide Decision and Recommendation Support to help answer your questions related to policies and restrictions during an epidemic. Using simulation techniques widely applied to other fields, we can help schools and colleges discover and hone the opportunities and optimizations they could make to their COVID-19 strategy. From the most simple decisions(Which days to be online or offline) to more complex strategies(What restrictions should I put on library use?, How many times should I test?, Whom do I test?) Episimmer is the tool for the job. <br>

Here is a short video describing Episimmer : [Video link](https://drive.google.com/file/d/1Oo-eG7pNIzaqf1uJ9rIf7DAc7MZwNRVY/view?usp=sharing)

## Requirements

Run the following command

		pip3 install -r requirements.txt

## Running Examples
To run examples :

		python src/Main.py <Path_to_Example>

Flags :

		-np or --noplot : Restrict plotting the time plot after simulation. Default = False
		-vul or --vuldetect : Run Vulnerability Detection on the data folder based on VD_config.txt. Default = False
		-an or --animate : Creates a gif animation of the time plot. Default = False
  	-s or --stats : Choose to store statistics. Default = False
		-vd or --vizdyn : Creates a gif of the simulation environment progressing through the days. Default = False



## Getting started

You can start using Episimmer by  using the following tutorials :

[Tutorial 1 : Getting started with Episimmer](https://docs.google.com/document/d/1PHMlz4W5gl_SpW8u1kWJEqzsAtW6NOWvePSMre9auT4/edit?usp=sharing) <br>
[Tutorial 2.0 : Episimmer Basic Modelling Theory](https://docs.google.com/document/d/1BujPmaEOGoJn6_B0DAhIUUlROKBt4gIlG13Kl9kDRh4/edit?usp=sharing) <br>
[Tutorial 2.1 : Modifications to the compartment model](https://docs.google.com/document/d/1vn8xc95bCQ7K09lMuc3ijHfSeDPa6Nd28tko-19SlnQ/edit?usp=sharing) <br>
[Tutorial 2.2 : Modifications to interaction spaces](https://docs.google.com/document/d/17QNw3BUEclqjtuoN6bd3pFNHsbzNIu2Bo0L1BCPS_A4/edit?usp=sharing) <br>
[Tutorial 3 : Introduction to Intervention and Policy](https://docs.google.com/document/d/121CdfYRg1144kZJoyJMq4xwfuM6vVdLn8bDnMIMMzoY/edit?usp=sharing) <br>


## UI
Our current UI can be found at https://episimmer.herokuapp.com/. Note that it has minimal functionality as compared to running the codebase directly. Yet it competes with the current state of the art systems with multiple novel features. <br>

Episimmer is currently Work in Progress. Check out these point solutions built using the Episimmer codebase. <br>

- [Optimizing Lockdowns](https://optimising-lockdowns.herokuapp.com) <br>
- [Efficient Contact tracing](https://contact-tracing.herokuapp.com) <br>
- [YACHT protocol](https://hb-yacht.herokuapp.com) <br>
- [Custom Stochastic Model on a complete graph](https://share.streamlit.io/inavamsi/custom_epidemic_model/main/Main.py) <br>
- [Testing strategies (Pool testing, Friendship testing)](https://share.streamlit.io/suryadheeshjith/epidemic-testing-ui/main.py) <br>
- [Vaccination with multiple vaccine types](https://share.streamlit.io/ruthushankar/vaccination_ui/main/vac.py) <br>
