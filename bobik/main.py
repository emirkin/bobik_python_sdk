#!/usr/bin/python
import urllib
import urllib2
import json
import eventlet
eventlet.monkey_patch()
import logging


class Bobik:
    """
    Class used to interface with the Bobik API.

    :param auth_token: The authentication token assigned to your user
    :param logger: A custom :class:`logging.Logger` object to use for \
    logging. May be ``None``, in which case output is controlled by the \
    ``debug`` parameter
    :param debug: whether to give debug output when a custom logger is not used
    """

    BOBIK_URL = 'https://usebobik.com/api/v1/jobs/'

    def __init__(self, auth_token, logger=None, debug=False):
        self.auth_token = auth_token
        if logger is not None:
            self.logger = logger
        else:
            logging.basicConfig()
            self.logger = logging.getLogger(__name__)
            if debug:
                self.logger.setLevel(logging.INFO)

    def call_api(self, query, http_method):
        """
        Submits a given query to the server using the given HTTP method.
        Returns the server response as a string.

        :param query: the query parameters, submitted as a dict
        :param http_method: the method to be used for the request, \
        must be ``"GET"`` or ``"POST"``
        :rtype: string
        """
        query['auth_token'] = self.auth_token
        request = None
        if http_method == 'GET':
            data = urllib.urlencode(query)
            url = Bobik.BOBIK_URL + '?' + data
            request = urllib2.Request(url, None)
        else:
            url = Bobik.BOBIK_URL
            request = urllib2.Request(url, urllib.urlencode(query))

        request.add_header('Accept', 'application/json')
        response = urllib2.urlopen(request)
        return response.read()

    def scrape(self, query, success_handler, error_handler):
        """
        Submits a new job for Bobik. Returns the job ID.

        :param query: the query dict used for the request
        :param success_handler: function to be called when \
        the the scraping process succesfully finishes
        :param error_handler: function to be called if there were any errors \
        while submitting the request
        :rtype: string
        """
        response = self.call_api(query, 'POST')
        json_obj = json.loads(response)
        if 'errors' in json_obj:
            return error_handler(json_obj['errors'])

        self.wait_and_collect_results(json_obj['job'], success_handler)
        return json_obj['job']

    def __check_progress(self, response):
        json_obj = json.loads(response)
        self.logger.info('Progress - %d%%', float(json_obj['progress']) * 100)
        if float(json_obj['progress']) < 1.0:
            return (False, json_obj)
        else:
            return (True, json_obj)

    def wait_and_collect_results(self, job_id, handler):
        self.logger.info('Waiting for job %s to complete', job_id)
        json_obj = {}
        json_obj['job'] = job_id
        response = self.call_api(json_obj, 'GET')
        job_done, response_json = self.__check_progress(response)
        while not job_done:
            time_left_ms = float(response_json['estimated_time_left_ms'])
            eventlet.sleep(time_left_ms / 1000.0)
            response = self.call_api(json_obj, 'GET')
            job_done, response_json = self.__check_progress(response)

        return handler(response)
