def testHttpClient():
    import http.client
    http_connection = http.client.HTTPConnection("www.yahoo.co.jp")
    http_connection.request("GET", "/index.html")
    http_response = http_connection.getresponse()
    print (http_response.status)
    print (http_response.read())
    print (http_response.getheaders())

def testUrllib():
    import urllib
    f = urllib.request.urlopen("http://www.yahoo.co.jp/index.html")
    for x in f:
        print (x)

if __name__=="__main__":
    import sys
    print ("Python %s.%s.%s"
           % (sys.version_info.major, sys.version_info.minor,
              sys.version_info.micro))
    testHttpClient()
    testUrllib()
