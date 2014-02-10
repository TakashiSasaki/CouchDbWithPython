"""
CouchDbHttpApi
"""
__author__="Takashi SASAKI"

import http.cookiejar, urllib.request, json
from CouchDbHttpApiBase import CouchDbHttpApiBase
class CouchDbHttpApi(CouchDbHttpApiBase):
    def __init__(self, dbname):
        CouchDbHttpApiBase.__init__(self,dbname)

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

    def getDesignDocumentInfo(self, design_name):
        self.open("/%s/_design/%s/_info" % (self.dbname, design_name), method="GET")
        return json.loads(self.read().decode("utf-8"))        

    def getDesignDocumentView(self, design_name, view_name):
        self.open("/%s/_design/%s/_view/%s" % (self.dbname, design_name, view_name), method="GET")
        return json.loads(self.read().decode("utf-8"))        

design_document = {
       "language"    : "javascript" ,
       "views"       : {
          "sum"  : {
             "map"    : """function(doc){
                 //emit(doc.x, doc.y);
                 emit(1,1);
                 }
             """,
             "reduce" : """function(key, values, rereduce){
                 if(rereduce){
                   var sum = 0;
                   for(v in values){
                     sum += v;
                   }//for
                   return v;
                 }//if
                 sum=0;
                 for(v in values){
                   sum += v;
                 }//for
                 return v;
             }"""
          },
          "view2" : {
             "map"    : "function(doc){}",
             "reduce" : "function(key, values, rereduce){}"
          }
       }}

import unittest
class TestMisc(unittest.TestCase):

    def test(self):
        x = CouchDbHttpApi("mydb")
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
        try:
            r = x.getDesignDocument("dd2")
            r = x.deleteDesignDocument("dd2", r["_rev"])
        except urllib.error.HTTPError as e: pass
        r = x.putDesignDocument("dd2", design_document)
        r = x.getDesignDocument("dd2")
        r = x.getDesignDocumentInfo("dd2")
        r = x.getDesignDocumentView("dd2", "sum")
        print(r)
        x.saveCookie()

if __name__=="__main__":
    unittest.main()
