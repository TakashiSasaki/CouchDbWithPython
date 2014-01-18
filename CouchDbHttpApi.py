import http.cookiejar, urllib.request
class CouchDbHttpApiBase():
    def __init__(self):
        self.cookieJar = http.cookiejar.LWPCookieJar('cookie.txt')
        self.cookieProcessor = urllib.request.HTTPCookieProcessor(self.cookieJar)
        self.openerDirector = urllib.request.build_opener(self.cookieProcessor)
        print(self.openerDirector)
        try:
            self.cookieJar.load()
        except FileNotFoundError:
            pass

    def saveCookie(self):
        self.cookieJar.save(ignore_discard=True, ignore_expires=True)

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

    def open(self, path, dict_or_list_of_tuple=None):
        if dict_or_list_of_tuple is not None:
            data = urllib.parse.urlencode(dict_or_list_of_tuple)
            self.httpResponse = self.openerDirector.open("http://127.0.0.1:5984/%s" % path, data=data.encode("utf-8"))
        else:
            self.httpResponse = self.openerDirector.open("http://127.0.0.1:5984/%s" % path)
        return self.httpResponse

    def status(self):
        return self.httpResponse.status()

    def read(self):
        return self.httpResponse.read()

    def getLog(self):
        self.open("_log")
        #print (self.read())

    def postSession(self):
        self.open("_session", {'name': "admin", 'password': 'adminpass'})
        #print(self.httpResponse.read())

if __name__=="__main__":
    couch_db_http_api_base = CouchDbHttpApiBase()
    couch_db_http_api_base.getMotd()
    #couch_db_http_api_base.getAllDbs()
    #couch_db_http_api_base.getUuids()
    #couch_db_http_api_base.getStats()
    print (couch_db_http_api_base.cookieJar)
    #couch_db_http_api_base.cookieJar.load("cookie.txt")
    print (couch_db_http_api_base.cookieJar)
    couch_db_http_api_base.postSession()
    print (couch_db_http_api_base.cookieJar)
    couch_db_http_api_base.getLog()
    couch_db_http_api_base.saveCookie()
    couch_db_http_api_base.cookieJar.load()
    print (couch_db_http_api_base.cookieJar)
