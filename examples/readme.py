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

