
Examples
==================

All the current data and python files for the examples in the main episimmer repository exists here. Do note that due to the large number of files, we have limited each file's
length to 200 lines.

.. warning::
    This page is created only for reference to the examples. Please do not copy them and try running them in your simulation
    until you are sure of what you are doing. Copying them may lead to errors due to the files being incomplete. Go to the `examples/ <https://github.com/healthbadge/episimmer/tree/master/examples>`_ directory
    in the `Episimmer repository <https://github.com/healthbadge/episimmer>`_ to get the complete files.

.. contents:: Contents
  :local:
  :depth: 2

{#
{% for top_key in examples %}
########################################
{{ top_key }}
########################################
  {% for example in examples[top_key] %}
    {% if example != 'read_me_path' %}

{{ example }}
--------------------------------------------------------
      {% for file in examples[top_key][example] %}
        {% if file != 'read_me_path' %}
{{ examples[top_key][example][file]['name'] }}

.. literalinclude:: {{ examples[top_key][example][file]['path'] }}
    :linenos:

        {% endif %}
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endfor %}
#}

{% for top_key in examples %}
########################################
{{ top_key }}
########################################
.. include:: {{ examples[top_key]['read_me_path'] }}
    :parser: myst_parser.sphinx_
    :start-line: 1

  {% for example in examples[top_key] %}
    {% if example != 'read_me_path' %}
.. include:: {{ examples[top_key][example]['read_me_path'] }}
    :parser: myst_parser.sphinx_

      {% for file in examples[top_key][example] %}
        {% if file != 'read_me_path' %}
{{ examples[top_key][example][file]['name'] }}

.. literalinclude:: {{ examples[top_key][example][file]['path'] }}
    :linenos:

        {% endif %}
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endfor %}
