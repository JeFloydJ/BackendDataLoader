# eventGetSearchConstituent.py
import urllib.request, json
import ssl
import requests

ssl._create_default_https_context = ssl._create_stdlib_context

def refresh_token():
    # Tus credenciales de Blackbaud ID
    client_id = "14ff689a-1054-43ef-a3ec-e3137c3c4a3e"
    client_secret = "Y/YJK4+22KtLQt4CTkA3cwVtOXh7B+jpCUQolXYdLfo="
    token_url = "https://oauth2.sky.blackbaud.com/token"

    # Leer el token de actualización desde el archivo
    with open('../server/refresh_token.txt', 'r') as f:
        refresh_token = f.read().strip()

    # Datos para la solicitud de actualización de token
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    # Solicitar un nuevo token de acceso
    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code == 200:
        new_access_token = token_response.json()["access_token"]
        print(f"Nuevo token de acceso: {new_access_token}")

        # Guardar el nuevo token de acceso
        with open('../server/token.txt', 'w') as f:
            f.write(new_access_token)
    else:
        print(f"Error al actualizar el token de acceso: {token_response.content}")

try:
    url = "https://api.sky.blackbaud.com/alt-conmg/constituents/search"

    # Leer el token de acceso desde el archivo
    with open('../server/token.txt', 'r') as f:
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
    
except urllib.error.HTTPError as e:
    if e.code == 401:  # Unauthorized
        print("El token de acceso ha expirado. Actualizando el token...")
        refresh_token()
    else:
        print(e)
except Exception as e:
    print(e)
