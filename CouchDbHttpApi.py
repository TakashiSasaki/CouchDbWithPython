import http.cookiejar, urllib.request
class CouchDbHttpApiBase():
    def __init__(self):
        self.cookieJar = http.cookiejar.LWPCookieJar()
        self.cookieProcessor = urllib.request.HTTPCookieProcessor(self.cookieJar)
        self.openerDirector = urllib.request.build_opener(self.cookieProcessor)
        print(self.openerDirector)
        self.cookieJar.load("cookie.txt")

    def saveCookie(self):
        self.cookieJar.save("cookie.txt")

    def getMotd(self):
        r = self.openerDirector.open("http://127.0.0.1:5984/")
        print (r.status)
        print (r.read())
        print (r.getheaders())
        print (self.cookieJar)

    def getAllDbs(self):
        r = self.openerDirector.open("http://127.0.0.1:5984/_all_dbs")
        print (r.status)
        print (r.read())
        print (r.getheaders())
        print (self.cookieJar)
        
    def getUuids(self):
        r = self.openerDirector.open("http://127.0.0.1:5984/_uuids")
        print (r.status)
        print (r.read())
        print (r.getheaders())
        print (self.cookieJar)

    def getStats(self):
        r = self.openerDirector.open("http://127.0.0.1:5984/_stats")
        print (r.status)
        print (r.read())
        print (r.getheaders())

    def getLog(self):
        r = self.openerDirector.open("http://127.0.0.1:5984/_log")
        print (r.status)
        print (r.read())
        print (r.getheaders())

if __name__=="__main__":
    couch_db_http_api_base = CouchDbHttpApiBase()
    couch_db_http_api_base.getMotd()
    couch_db_http_api_base.getAllDbs()
    couch_db_http_api_base.getUuids()
    couch_db_http_api_base.getStats()
    couch_db_http_api_base.getLog()
    couch_db_http_api_base.saveCookie()
