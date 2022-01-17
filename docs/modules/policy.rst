
episimmer.policy
=================

.. contents:: Contents
    :local:

Lockdown Policy API
------------------------------
.. currentmodule:: episimmer.policy
.. autosummary::
   :nosignatures:
   {% for cls in episimmer.policy.lockdown_classes %}
     {{ cls }}
   {% endfor %}

{% for cls in episimmer.policy.lockdown_classes %}
.. autoclass:: {{ cls }}
   :members:
   :undoc-members:
{% endfor %}

Testing Policy API
------------------------------
.. currentmodule:: episimmer.policy
.. autosummary::
   :nosignatures:
   {% for cls in episimmer.policy.test_classes %}
     {{ cls }}
   {% endfor %}

{% for cls in episimmer.policy.test_classes %}
.. autoclass:: {{ cls }}
    :members:
    :undoc-members:
{% endfor %}

Vaccination Policy API
------------------------------
.. currentmodule:: episimmer.policy
.. autosummary::
   :nosignatures:
   {% for cls in episimmer.policy.vaccine_classes %}
     {{ cls }}
   {% endfor %}

{% for cls in episimmer.policy.vaccine_classes %}
.. autoclass:: {{ cls }}
  :members:
  :undoc-members:
{% endfor %}
