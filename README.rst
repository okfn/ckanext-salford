===============
ckanext-salford
===============

CKAN extension for https://www.salforddataquay.uk/


------------
Installation
------------

To install ckanext-salford:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-salford Python package into your virtual environment::

     pip install ckanext-salford

3. Add ``salford`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Add the ``licenses_group_url`` setting to your CKAN config file.
   For development use::

     licenses_group_url = http://127.0.0.1:5000/licenses.json

   For production use::

     licenses_group_url = https://www.salforddataquay.uk/licenses.json

5. Install the Bower components::

     cd /ckanext/salford/fanstatic
     bower install

6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


-----------------------------------
Importing Datasets from data.gov.uk
-----------------------------------

The ``etl.py`` script can import datasets from the
`Salford City Council publisher on data.gov.uk <http://data.gov.uk/publisher/salford-city-council>`_
into a development or production CKAN instance. Usage::

  pip install ckanapi
  ./etl.py -u 'http://127.0.0.1:5000' -a <your_api_key>
  ./etl.py -u 'https://www.salforddataquay.uk/' -a <your_api_key>
