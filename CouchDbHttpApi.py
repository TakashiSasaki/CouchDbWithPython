import http.cookiejar, urllib.request
class CouchDbHttpApiBase():
    def __init__(self):
        self.cookieJar = http.cookiejar.LWPCookieJar('cookie.txt')
        self.cookieProcessor = urllib.request.HTTPCookieProcessor(self.cookieJar)
        self.openerDirector = urllib.request.build_opener(self.cookieProcessor)
        print(self.openerDirector)
        try:
            self.cookieJar.load(ignore_discard=True, ignore_expires=True)
        except FileNotFoundError:
            pass

    def saveCookie(self):
        self.cookieJar.save(ignore_discard=True, ignore_expires=True)

    def getMotd(self):
        self.open("/")
        print (self.status())
        print (self.read())
        print (self.getheaders())

    def getAllDbs(self):
        self.open("/_all_dbs")
        print (self.status())
        print (self.read())
        print (self.getheaders())
        
    def getUuids(self):
        self.open("/_uuids")
        print (self.status())
        print (self.read())
        print (self.getheaders())

    def getStats(self):
        self.openerDirector.open("/_stats")
        print (self.status())
        print (self.read())
        print (self.getheaders())

    def open(self, path, dict_or_list_of_tuple=None):
        if dict_or_list_of_tuple is not None:
            data = urllib.parse.urlencode(dict_or_list_of_tuple)
            self.httpResponse = self.openerDirector.open("http://127.0.0.1:5984%s" % path, data=data.encode("utf-8"))
        else:
            self.httpResponse = self.openerDirector.open("http://127.0.0.1:5984%s" % path)
        return self.httpResponse

    def status(self):
        return self.httpResponse.status

    def read(self):
        return self.httpResponse.read()

    def clear_session_cookies(self):
        self.cookieJar.clear_session_cookies()

    def clear(self):
        self.cookieJar.clear()
        
    def getheaders(self):
        return self.httpResponse.getheaders()

    def getLog(self):
        self.open("/_log")
        #print (self.read())

    def postSession(self, username, password):
        self.open("/_session", {'name': username, 'password': password})
        #print(self.httpResponse.read())

if __name__=="__main__":
    x = CouchDbHttpApiBase()
    #x.getMotd()
    #x.getAllDbs()
    #x.getUuids()
    #x.getStats()
    #x.postSession()
    try:
        x.getLog()
    except urllib.error.HTTPError as e:
        print (e)
        username=input("username > ")
        password=input("password > ")
        x.postSession(username, password)
        x.getLog()
    print (x.read())
    x.saveCookie()
