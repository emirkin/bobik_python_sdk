Usage
=====

Quickstart
**********

In order to use Bobik, first be sure to :doc:`install </installation>` it.

Everything is accomplished through the :class:`bobik.Bobik` class. It exposes
a few methods that interact with the `Bobik API`_. A simple use of the API is
as following:

.. literalinclude:: ../examples/simple.py
   :language: python
	
This example lists the categories of a few pages within the `DMOZ`_ directory
listing.  The ``key : value`` pairs in the ``query`` variable may be any pairs
listed within the `function reference
<http://usebobik.com/api/docs#func_ref>`_, except for the ``auth_token``
parameter, which is added automatically.

Note that the URLs passed in the ``url`` query parameter don't have to be of
the same domain, and you can also have multiple ``queries`` per request as well, as the next example shows:

.. literalinclude:: ../examples/multiple-queries.py
   :language: python

.. _Bobik API: http://usebobik.com/api/docs
.. _DMOZ: http://www.dmoz.org

Handlers
********

When you call :func:`bobik.Bobik.scrape`, you have to pass in two functions that will be used as
callbacks for your request, these are the two functions you should pass:

.. function:: success_handler(response)

   Function to be called when the job is successfully completed.

   :param response: The parsed JSON response received from Bobik.

.. function:: error_handler(error_list)
   
   Function to be called when there is an error with the request.

   :param error_list: The errors from the ``errors`` field in the response. It is a list of strings.

Concurrent queries
******************

If you have the need to create multiple requests at once, one such possibility
is by using the `Eventlet`_ library, which allows us to make concurrent
requests easily. For tips on better management of multiple requests, see the
`Eventlet documentation`_.

The example below shows a way to create two concurrent requests to the Bobik
API, and wait for both of them:

.. literalinclude:: ../examples/concurrent.py
   :language: python

.. _Eventlet: http://eventlet.net/
.. _Eventlet documentation: http://eventlet.net/doc/index.html

Debug output
************

The constructor for the :class:`bobik.Bobik` class accepts three arguments:

* Query parameters;
* A :class:`logging.Logger` instance;
* A boolean indicating whether to give debug output.

By default, when using debug (when ``debug=True`` is given) output, messages like the following will be printed to ``stderr``::

	INFO:bobik.main:Waiting for job 500d95aa192f3c713b000040 to complete
	INFO:bobik.main:Progress - 0%
	INFO:bobik.main:Progress - 100%

To instantiate the class using debug output, you can write::

	bobik_api = Bobik(YOUR_AUTH_TOKEN, debug=True)

To pass a custom :class:`logging.Logger` instance, use::

	bobik_api = Bobik(YOUR_AUTH_TOKEN, logger=custom_logger)

Passing both ``logger`` and ``debug`` values causes no changes to the logger
passed in.
