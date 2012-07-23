from bobik import Bobik
import eventlet
eventlet.monkey_patch()

def success_handler(response):
        print response

def error_handler(error_list):
        print error_list

bobik_api = Bobik(YOUR_AUTH_TOKEN) #Replace with your own token

query1 = {
        'urls' : 'http://www.dmoz.org/',
        'queries' : '//div//span/a/text()'
}

thread1 = eventlet.spawn(bobik_api.scrape, query1, success_handler, error_handler)

query2 = {
        'urls' : 'http://www.dmoz.org/Computers/Computer_Science/Research_Institutes/',
        'queries' : '//ul[@class="directory-url"]/li/a/@href'
}

thread2 = eventlet.spawn(bobik_api.scrape, query2, success_handler, error_handler)

thread1.wait()
thread2.wait()
