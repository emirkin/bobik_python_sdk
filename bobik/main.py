#!/usr/bin/python
import urllib
import urllib2
import json
import eventlet
eventlet.monkey_patch()

class Bobik:
    BOBIK_URL = 'https://usebobik.com/api/v1/jobs/'

    def __init__(self, auth_token, logger=None, debug=):
        self.auth_token = auth_token
        if logger is not None:
            self.logger = logger
        else:
            self.logger = None
        self.debug = debug

    def call_api(self, query, http_method):
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
        response = self.call_api(query, 'POST')
        json_obj = json.loads(response)
        if json_obj.has_key('errors'):
            return error_handler('error')

        self.wait_and_collect_results(json_obj['job'], success_handler)
        return json_obj['job']

    def check_progress(self, response):
        jsonObj = json.loads(response)
        if self.debug:
            self.log_message('INFO', 'Progress - %d%%'% (float(json_obj['progress'])*100))
        if float(json_obj['progress']) < 1.0:
            return False
        else:
            return True


    def wait_and_collect_results(self, job_id, handler):
        if self.debug:
            self.log_message('INFO', 'Waiting for job %s to complete' % job_id)
        json_obj = {}
        json_obj['job'] = job_id
        response = self.call_api(json_obj, 'GET')
        job_done = self.check_progress(response)
        while not job_done:
            eventlet.sleep(1)
            response = self.call_api(json_obj, 'GET')
            job_done = self.check_progress(response)

        return handler(response)

    def log_message(self, level, message):
        if self.logger is None:
            print ('%s : %s')%(level, message)

