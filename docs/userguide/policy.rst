
Intervention Policy
=====================================

* :ref:`Introduction - Intervention Policy`
* :ref:`Implementing Policies`
* :doc:`Policy API<../modules/policy>`


Introduction - Intervention Policy
-------------------------------------

A Intervention Policy, in Epidemic terms, is a user defined intervention method which applies to any activity undertaken with the
objective of improving human health by preventing disease, or reducing the severity or duration of an existing disease.

The mantra of episimmer is to be flexible in all aspects of epidemic simulation. Thus, any kind of policy can be accommodated and
thereby implemented in the system. Nevertheless, we have implemented some standard policies such that non-technical users can
try out simulations and real-world examples can be implemented quickly.

Currently, the policies that can be implemented are:

* :ref:`Lockdown Policy`
* :ref:`Testing Policy`
* :ref:`Vaccination Policy`

Each of these policies have template functions that can be used by the user to run standard simulations. For example, standard testing,
pool testing, standard vaccination, lockdown or restriction policies based on attributes of the agent (like age). Even the way these policies
behave can be molded to the user's wishes.

Lockdown Policy
~~~~~~~~~~~~~~~~

Testing Policy
~~~~~~~~~~~~~~~~

Vaccination Policy
~~~~~~~~~~~~~~~~~~~


Implementing Policies
----------------------
