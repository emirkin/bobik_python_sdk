import Bobik
import eventlet
eventlet.monkey_patch()

if __name__ == '__main__':
    def successHandler(response):
        print 'Success Handler'
        print response
        # do something here for your application
    def errorHandler(response):
        print 'Error Handler'
        print response
        # raise error and bail

    b = Bobik.Bobik(YOUR_AUTH_TOKEN, None, True)
    gt1 = eventlet.spawn_after(1, b.scrape, {'urls':'http://google.com', 'queries': '//div'}, successHandler, errorHandler)
    print 'foo bar baz'
    gt2 = eventlet.spawn_after(1, b.scrape, {'urls':'http://yahoo.com', 'queries': '//div'}, successHandler, errorHandler)

    gt1.wait()
    gt2.wait()
