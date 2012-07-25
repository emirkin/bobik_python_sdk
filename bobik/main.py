#!/usr/bin/python
import urllib
import urllib2
import json
import logging
import time
import requests


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
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = json.dumps(query)
        if http_method == 'GET':
            r = requests.get(Bobik.BOBIK_URL, data=data, headers=headers)
        else:
            r = requests.post(Bobik.BOBIK_URL, data=data, headers=headers)

        return r.json

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
        response_json = self.call_api(query, 'POST')
        if 'errors' in response_json:
            return error_handler(response_json['errors'])

        self.wait_and_collect_results(response_json['job'], success_handler)
        return response_json['job']

    def wait_and_collect_results(self, job_id, handler):
        """
        Queries Bobik to see if a given job was finished. Normally, you don't
        have to call this function directly, as the SDK will do it for you. It
        will wait until the job has finished and will call the handler on the
        response when the job is done.

        :param job_id: The job ID that was received from Bobik
        :param handler: The function to call when the job is finished
        :rtype: The same type as the ``handler`` function return type
        """
        self.logger.info('Waiting for job %s to complete', job_id)
        query = {}
        query['job'] = job_id
        response_json = self.call_api(query, 'GET')
        job_done = self.__check_progress(response_json)
        while not job_done:
            time_left_ms = float(response_json['estimated_time_left_ms'])
            time.sleep(time_left_ms / 1000.0)
            response_json = self.call_api(query, 'GET')
            job_done = self.__check_progress(response_json)

        return handler(response_json)

    def __check_progress(self, response_json):
        """
        Checks the response from Bobik to see if the job was completed.
        The returned data is a tuple (bool, dict), where the first value
        indicates whether the job was completed, and the second is the
        parsed JSON response.

        :param response: The response data from Bobik
        :rtype: tuple
        """
        progress = float(response_json['progress'])
        self.logger.info('Progress - %d%%', progress * 100)
        if progress < 1.0:
            return False
        else:
            return True
