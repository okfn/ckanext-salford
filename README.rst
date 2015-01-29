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

4. Install the Bower components::

     cd /ckanext/salford/fanstatic
     bower install

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload
