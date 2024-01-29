import urllib.request, json

try:
    url = "https://api.sky.blackbaud.com/alt-conmg/constituents/search"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'Authorization': '',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)