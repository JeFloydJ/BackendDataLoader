import requests
import ssl
import json
from eventGetAdhocQueryIdByName import get_id

id = get_id()

ssl._create_default_https_context = ssl._create_stdlib_context

def refresh_token():
    client_id = "14ff689a-1054-43ef-a3ec-e3137c3c4a3e"
    client_secret = "Y/YJK4+22KtLQt4CTkA3cwVtOXh7B+jpCUQolXYdLfo="
    token_url = "https://oauth2.sky.blackbaud.com/token"

    with open('../serverAltru/refresh_token.txt', 'r') as f:
        refresh_token = f.read().strip()

    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code == 200:
        new_access_token = token_response.json()["access_token"]
        print(f"Nuevo token de acceso: {new_access_token}")

        with open('../serverAltru/token.txt', 'w') as f:
            f.write(new_access_token)
    else:
        print(f"Error al actualizar el token de acceso: {token_response.content}")

def get_query():
    url = f"https://api.sky.blackbaud.com/alt-anamg/adhocqueries/{id}"

    with open('../serverAltru/token.txt', 'r') as f:
        access_token = f.read().strip()

    headers = {
        'Cache-Control': 'no-cache',
        'Authorization': f'Bearer {access_token}',
        'Bb-Api-Subscription-Key': 'fa43a7b522a54b718178a4af6727392f'
    }

    try:
        response = requests.request("GET", url, headers=headers)

        if response.status_code == 401:  # Unauthorized
            print("El token de acceso ha expirado. Actualizando el token...")
            refresh_token()
            return get_query()  # Llama a la función de nuevo después de actualizar el token

        response_json = json.loads(response.text)

        # Guardar la respuesta en un archivo JSON
        with open('response.json', 'w') as f:
            json.dump(response_json, f)

    except requests.exceptions.RequestException as e:
        print(e)

# Uso de la función
get_query()
