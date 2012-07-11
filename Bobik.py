#!/usr/bin/python
import urllib
import urllib2
import json
import eventlet
eventlet.monkey_patch()

class Bobik:
    BOBIK_URL = 'https://usebobik.com/api/v1/jobs/'

    def __init__(self, authToken, logger, enableDebug):
        self.authToken = authToken
        if logger is not None:
            self.logger = logger
        else:
            self.logger = None
        self.enableDebug = enableDebug

    def callAPI(self, query, httpMethod):
        query['auth_token'] = self.authToken
        request = None
        if httpMethod == 'GET':
            data = urllib.urlencode(query)
            url = self.BOBIK_URL + '?' + data
            request = urllib2.Request(url, None)
        else:
            url = self.BOBIK_URL
            request = urllib2.Request(url, urllib.urlencode(query))

        request.add_header('Accept', 'application/json')
        response = urllib2.urlopen(request)
        return response.read()
            
    def scrape(self, query, successHandler, errorHandler):
        response = self.callAPI(query, 'POST')
        jsonObj = json.loads(response)
        if jsonObj.has_key('errors'):
            return errorHandler('error')

        self.waitAndCollectResults(jsonObj['job'], successHandler)
        return jsonObj['job']

    def checkProgress(self, response):
        jsonObj = json.loads(response)
        if(self.enableDebug):
            self.logMessage('INFO', 'Progress - %d%%'% (float(jsonObj['progress'])*100))
        if float(jsonObj['progress']) < 1.0:
            return False
        else:
            return True


    def waitAndCollectResults(self, jobId, handler):
        if(self.enableDebug):
            self.logMessage('INFO', 'Waiting for job %s to complete' % jobId)
        jsonObj = {}
        jsonObj['job'] = jobId
        response = self.callAPI(jsonObj, 'GET')
        jobDone = self.checkProgress(response)
        while jobDone != True:
            eventlet.sleep(1)
            response = self.callAPI(jsonObj, 'GET')
            jobDone = self.checkProgress(response)

        return handler(response)

    def logMessage(self, level, message):
        if self.logger is None:
            print ('%s : %s')%(level, message)


