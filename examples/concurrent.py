#import eventlet as soon as possible
import eventlet
eventlet.monkey_patch()
from bobik import Bobik

def success_handler(response):
	print response

def error_handler(error_list):
	print error_list

bobik_api = Bobik(YOUR_AUTH_TOKEN, debug=True) #Replace with your own token

query1 = {
	'urls' : ['dmoz.org', 'google.com', 'amazon.com', 'yahoo.com'],
	'queries' : ['return document.title', 'return $("script").length']
}

thread1 = eventlet.spawn(bobik_api.scrape, query1, success_handler, error_handler)

query2 = {
	'urls' : ['hackaday.com', 'makezine.com', 'http://hakin9.org/'],
	'queries' : ['//img/@src', '//a/@href', 'return document.title']
}

thread2 = eventlet.spawn(bobik_api.scrape, query2, success_handler, error_handler)

thread1.wait()
thread2.wait()
