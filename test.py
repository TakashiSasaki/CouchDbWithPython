def testHttpClient():
    import http.client
    http_connection = http.client.HTTPConnection("www.yahoo.co.jp")
    http_connection.request("GET", "/index.html")
    http_response = http_connection.getresponse()
    print (http_response.status)
    #print (http_response.read())
    print (http_response.getheaders())

def testUrllib():
    import urllib.request
    http_response = urllib.request.urlopen("http://www.yahoo.co.jp/index.html")
    print (http_response.status)
    #print (http_response.read())
    print (http_response.getheaders())

def testCookieJar():
    import http.cookiejar, urllib.request
    cj = http.cookiejar.MozillaCookieJar()
    cp = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cp)
    #r = opener.open("http://yahoo.co.jp/index.html")
    r = opener.open("http://www.google.co.jp/")
    print (r.status)
    #print (r.read())
    print (r.getheaders())
    print (cj)
    cj.save("cookie.txt")

if __name__=="__main__":
    import sys
    print ("Python %s.%s.%s"
           % (sys.version_info.major, sys.version_info.minor,
              sys.version_info.micro))
    testHttpClient()
    testUrllib()
    testCookieJar()
