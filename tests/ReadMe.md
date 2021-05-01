This folder contains all the tests we perform on Episimmer. We use the [unittest](https://docs.python.org/3/library/unittest.html) library to perform the tests.

The two types of tests here are :

1. Unit Tests : A unit test checks a small component in the simulator.
2. Integration Tests : An integration test checks that components in the simulator operate with each other.


To run all the tests, run the command below in the top directory /episimmer  

      python3 -m unittest discover -s tests
