import http.cookiejar, urllib.request, json
class CouchDbHttpApiBase():
    def __init__(self, dbname):
        self.dbname = dbname
        self.cookieJar = http.cookiejar.LWPCookieJar('cookie.txt')
        self.cookieProcessor = urllib.request.HTTPCookieProcessor(self.cookieJar)
        self.openerDirector = urllib.request.build_opener(self.cookieProcessor)
        print(self.openerDirector)
        try:
            self.cookieJar.load(ignore_discard=True, ignore_expires=True)
        except FileNotFoundError:
            pass
        
        try:
            self.getLog()
        except urllib.error.HTTPError as e:
            print (e)
            username=input("username > ")
            password=input("password > ")
            self.postSession(username, password)
            
        try:
            self.putDb(self.dbname)
        except urllib.error.HTTPError as e:
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

    def open(self, path, dict_or_list_of_tuple=None, method=None):
        if isinstance(dict_or_list_of_tuple, list):
            data = urllib.parse.urlencode(dict_or_list_of_tuple)
            data = data.encode("utf-8")
            method="POST"
            req = urllib.request.Request(url="http://127.0.0.1:5984%s" % path, data=data, method=method)
        elif isinstance(dict_or_list_of_tuple, dict):
            data = json.dumps(dict_or_list_of_tuple)
            data = data.encode("utf-8")
            assert(method is not None)
            req = urllib.request.Request(url="http://127.0.0.1:5984%s" % path, data=data, method=method)
            req.add_header("Content-Type","application/json")
        else:
            if method is None: method="GET"
            data = None
            req = urllib.request.Request(url="http://127.0.0.1:5984%s" % path, data=data, method=method)

        #req = urllib.request.Request(url="http://127.0.0.1:5984%s" % path, data=data, method=method)
        self.httpResponse = self.openerDirector.open(req)
        #self.httpResponse = self.openerDirector.open("http://127.0.0.1:5984%s" % path, data)

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
        self.open("/_session", [('name', username), ('password', password)])
        #print(self.httpResponse.read())

    def putDb(self, dbname):
        self.open("/%s/" % dbname, method="PUT")

    def deleteDb(self, dbname):
        self.open("/%s/" % dbname, method="DELETE")

    def put(self, json_object, id):
        self.open("/%s/%s" % (self.dbname, id), dict_or_list_of_tuple=json_object, method="PUT")

    def post(self, json_object):
        self.open("/%s/" % self.dbname, dict_or_list_of_tuple=json_object, method="POST")
        return json.loads(self.read().decode("utf-8"))

    def putDesignDocument(self, design_name, json_object):
        self.open("/%s/_design/%s" % (self.dbname, design_name), dict_or_list_of_tuple=json_object, method="PUT")
        return json.loads(self.read().decode("utf-8"))
        
    def deleteDesignDocument(self, design_name, rev):
        self.open("/%s/_design/%s?rev=%s" % (self.dbname, design_name, rev), method="DELETE")
        return json.loads(self.read().decode("utf-8"))

    def getDesignDocument(self, design_name):
        self.open("/%s/_design/%s" % (self.dbname, design_name), method="GET")
        return json.loads(self.read().decode("utf-8"))


if __name__=="__main__":
    x = CouchDbHttpApiBase("mydb")
    x.getMotd()
    print(x.read())
    x.getAllDbs()
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
    x.getAllDbs()
    #x.deleteDb("mydb")
    r = x.post({"aa":1})
    print(r)
    r = x.post({"b":2, "_id":r["id"], "_rev":r["rev"]})
    try:
        r = x.put({"a":1}, id="12345")
    except: pass
    r = x.getDesignDocument("dd2")
    r = x.deleteDesignDocument("dd2", r["_rev"])
    print (r)
    #r = x.putDesignDocument("dd2", {
    #   "language"    : "javascript" ,
    #   "views"       : {
    #      "view1"  : {
    #         "map"    : "function(doc){ ... }",
    #         "reduce" : "function(key, values, rereduce){ ... }"
    #      },
    #      "view2" : {
    #         "map"    : "function(doc){ ... }",
    #         "reduce" : "function(key, values, rereduce){ ... }"
    #      }
    #   }})
    #print(r)
    r = x.getDesignDocument("dd2")
    print (r)
    x.saveCookie()
