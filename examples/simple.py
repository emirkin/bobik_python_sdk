from bobik import Bobik

def success_handler(response):
	print response

def error_handler(error_list):
	print error_list

bobik_api = Bobik(YOUR_AUTH_TOKEN, debug=True) #Replace with your own token

query = {
	'urls' : ['http://www.dmoz.org/', 'http://www.dmoz.org/Computers/', 'http://www.dmoz.org/Computers/Programming/'],
	'queries' : '//div//span/a/text()'
}

bobik_api.scrape(query, success_handler, error_handler)
