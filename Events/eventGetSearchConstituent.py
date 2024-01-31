import urllib.request, json
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

try:
    url = "https://api.sky.blackbaud.com/alt-conmg/constituents/search"

    # Leer el token de acceso desde el archivo
    with open('../Server/token.txt', 'r') as f:
        access_token = f.read().strip()

    hdr = {
    # Request headers
        'Cache-Control': 'no-cache',
        'Bb-Api-Subscription-Key': 'fa43a7b522a54b718178a4af6727392f',
        'Authorization': f'Bearer {access_token}'
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())    
except Exception as e:
    print(e)
