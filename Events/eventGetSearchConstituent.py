import urllib.request, json
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

try:
    url = "https://api.sky.blackbaud.com/alt-conmg/constituents/search"

    hdr = {
    # Request headers
        'Cache-Control': 'no-cache',
        'Bb-Api-Subscription-Key': 'fa43a7b522a54b718178a4af6727392f',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjREVjZzVkxIM0FtU1JTbUZqMk04Wm5wWHU3WSIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbmlkIjoiMTRmZjY4OWEtMTA1NC00M2VmLWEzZWMtZTMxMzdjM2M0YTNlIiwiZW52aXJvbm1lbnRpZCI6InAtRGRYVTFmdXdBVS1YQjdsbHpkODA1QSIsImVudmlyb25tZW50bmFtZSI6IkhhcnQgU3F1YXJlIEZvdW5kYXRpb24sIEluYy4gRW52aXJvbm1lbnQgMSIsImxlZ2FsZW50aXR5aWQiOiJwLW5OQ3JIV3pDcWtTZzF4ZGhBRWdNbkEiLCJsZWdhbGVudGl0eW5hbWUiOiJIYXJ0IFNxdWFyZSBGb3VuZGF0aW9uLCBJbmMuIiwibW9kZSI6IkZ1bGwiLCJ6b25lIjoicC11c2EwMSIsIm5hbWVpZCI6ImQ0NzU2OGRkLTJmMzItNGRmMi04MjZhLTA5MGU4ZjdhYjNiYiIsImp0aSI6ImE0NDM3NGM1LWMxN2YtNDVmZS05ZjRmLTQyMGMwYjI3ZTk1NiIsImV4cCI6MTcwNjY0NDE3MCwiaWF0IjoxNzA2NjQwNTcwLCJpc3MiOiJodHRwczovL29hdXRoMi5za3kuYmxhY2tiYXVkLmNvbS8iLCJhdWQiOiJibGFja2JhdWQifQ.C_-swHRJebk3e7h32rrvapo2JcOdtjl0V46rftkjkTTS49xCbHsg2S5bAIhDXJDNrRpGxDx59o26RmOH2DsUNU8UwCGE53x7JqtnuJvI2P6iNcSJIRvlUov24mvI_LPt47zzkD0_4BRkYYnSFvouWs9jzEDV4IGHQsgAM4y8vddwy5SZHjF6BA-OVJ0CGJpHkZjpLxuUvZxSD1IjnGeQSEDqfRJyS5lDzw7DoJ7ugbC2gPEzKqZpCFqPjGPi_QuH8C-Mn9Io2uNm35UcxKbpL3DxR1rX4p78LRcEUZyV-BVJVg5jYDuu8umtK5tHE2aF50rbGppFEpAhHT4N57CgPA'
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)