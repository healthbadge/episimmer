
episimmer.utils
================
.. contents:: Contents
    :local:

ArgParse API
------------------------------

.. currentmodule:: episimmer.utils
{% for func in episimmer.utils.ap_funcs %}
.. autofunction:: {{ func }}
{% endfor %}

Module Handling API
------------------------------

.. currentmodule:: episimmer.utils
{% for func in episimmer.utils.module_funcs %}
.. autofunction:: {{ func }}
{% endfor %}

Time API
------------------------------
.. currentmodule:: episimmer.utils
.. automodule:: episimmer.utils.time
    :members:
    :undoc-members:

Statistics API
--------------------

.. currentmodule:: episimmer.utils
.. autosummary::
   :nosignatures:
   {% for cls in episimmer.utils.stats_classes %}
     {{ cls }}
   {% endfor %}
   {% for func in episimmer.utils.stats_funcs %}
     {{ func }}
   {% endfor %}


{% for cls in episimmer.utils.stats_classes %}
.. autoclass:: {{ cls }}
   :members:
   :undoc-members:
{% endfor %}
{% for func in episimmer.utils.stats_funcs %}
.. autofunction:: {{ func }}
{% endfor %}

Visualization API
------------------
.. currentmodule:: episimmer.utils
.. autosummary::
   :nosignatures:
   {% for func in episimmer.utils.viz_funcs %}
     {{ func }}
   {% endfor %}

{% for func in episimmer.utils.viz_funcs %}
.. autofunction:: {{ func }}
{% endfor %}


Math API
----------
.. currentmodule:: episimmer.utils
.. autosummary::
   :nosignatures:
   {% for func in episimmer.utils.math_funcs %}
     {{ func }}
   {% endfor %}

{% for func in episimmer.utils.math_funcs %}
.. autofunction:: {{ func }}
{% endfor %}
