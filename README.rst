Web Scraping in Python using Bobik
==================================

This is a community-supported Bobik SDK for web scraping in Python.

Installing
**********

You can install the SDK using ``pip`` directly from this repository::

	pip install -e git+https://github.com/emirkin/bobik_python_sdk#egg=bobik_python_sdk

Using
*****

Here's a quick example to get you started

.. code-block:: python

	from bobik import Bobik
	bobik_api = Bobik(YOUR_AUTH_TOKEN, debug=True)

	def success_handler(response):
		for site in response['results']:
			print 'Results for %s' % site
			for query in response['results'][site]:
				print '\tQuery: %s' % query
				 for result in response['results'][site][query]:
					 print '\t\t%s' % result
	
	def error_handler(error_list):
		for err in error_list:
			print err

	query = {
		'urls' : ['amazon.com', 'zynga.com', 'http://finance.yahoo.com'],
		'queries' : ['//th', '//img/@src', 'return document.title', "return $('script').length"]
	}

	bobik_api.scrape(query, success_handler, error_handler)

Documentation
*************

Documentation can be found at http://usebobik.com/sdk.

The docs are generated with `Sphinx <http://sphinx.pocoo.org/>`_. To generate
the docs, enter the ``docs`` folder and run::

    $ make html

The documentation will be generated inside the ``_build`` directory.

Contributing
************

Write to support@usebobik.com to become a collaborator.

Bugs
****

Submit issues with the SDK `here <https://github.com/emirkin/bobik_python_sdk/issues>`_ on Github.
