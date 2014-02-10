"""
CouchDbHttpApiBase
"""
__author__="Takashi SASAKI"

import http.cookiejar, urllib.request, json
class CouchDbHttpApiBase(object):
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

    def __del__(self):
        self.httpResponse.close()
