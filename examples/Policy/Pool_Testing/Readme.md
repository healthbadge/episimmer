# Testing Policy
The Testing Policy in episimmer has a high degree of flexibility and the user can define several factors of how the testing procedure is implemented in the simulator. Several parameters must be passed by the user to enforce flexibility - First, the relationship between the agents and the test tubes must be defined. There can be multiple agents in a test tube, multiple test tubes for a single agent or a mix of these two types. Next, the relationship between the test tubes and the machines must be defined. A machine has a capacity and a turnaround time. The capacity determines the number of test tubes the machine can test on every time step. The turnaround time decides the number of time steps the machine takes to complete one round of testing. Since machines decide how tests are performed, there is a false positive and false negative rate associated with each machine. The number of tests performed each time step is also a function that can be passed as a function of time step.

## Running
To run code from current directory :

		cd examples/Policy
		python ../../src/Main.py Pool_Testing
<br>