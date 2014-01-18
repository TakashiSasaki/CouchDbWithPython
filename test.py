def testHttpClient():
    import http.client
    http_connection = http.client.HTTPConnection("www.yahoo.co.jp")
    http_connection.request("GET", "/index.html")
    http_response = http_connection.getresponse()
    print (http_response.status)
    print (http_response.read())
    print (http_response.getheaders())

if __name__=="__main__":
    testHttpClient()
