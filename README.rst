########
PlanToPI
########

A PM2.5 project using PlanTower sensors connected to a RaspberryPI board


Architecture
============

The data flow from Plantower sensor to reliable API end point is broken down as follow:

* Plantower sensor generates air quality data
* RaspberryPI fetches data via serial port
* Robust python code packs data and post to API end point

Configuration
=============


Install
=======

First we need to install setuptools with:

.. code:: sh

    $ pip install -U setuptools pip

To compile requirements use:

.. code:: sh

    $pip-compile --output-file requirements.txt requirements.in

Install the requirements via:

.. code:: sh

    $ pip install -r requirements.txt

Development
===========


Test
----


License
=======

This software is licensed under the Apache License 2.0. See the LICENSE file in the top distribution directory for the full license text.