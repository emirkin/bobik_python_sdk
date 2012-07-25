from bobik import Bobik

def success_handler(response):
	print response

def error_handler(error_list):
	print error_list

bobik_api = Bobik(YOUR_AUTH_TOKEN, debug=True) #Replace with your own token

query = {
	'urls' : ['9gag.com', 'xkcd.com', 'www.amazingsuperpowers.com'],
	'queries' : ['//img/@src', 'return document.title', 'return $("script").length']
}

bobik_api.scrape(query, success_handler, error_handler)
