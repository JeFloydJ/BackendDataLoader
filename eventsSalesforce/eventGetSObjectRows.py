# eventGetSearchConstituent.py
import urllib.request, json
import ssl
import requests

ssl._create_default_https_context = ssl._create_stdlib_context

def refresh_token():
    # Tus credenciales de salesforce
    client_id = '3MVG9zeKbAVObYjPODek1PYnJW15VxHyhGPUOe1vzfHcg89tL_3Xyj_DCZQql_RL4Gjdnmk7EpfFk4DGDulnz'
    client_secret = '6003041383007768349'  
    redirect_uri = "http://localhost:8000"
    token_url = "https://login.salesforce.com/services/oauth2/token"
    
    # Leer el token de actualización desde el archivo
    with open('../serverSalesforce/refresh_token.txt', 'r') as f:
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
        with open('../serverSalesforce/token.txt', 'w') as f:
            f.write(new_access_token)
    else:
        print(f"Error al actualizar el token de acceso: {token_response.content}")

try:
    sobject_api_name = 'Contact'
    record_id = '0035e00000sERzZAAW'
    url = f"https://veevartdevstage.my.salesforce.com/services/data/v59.0/sobjects/{sobject_api_name}/{record_id}"

    # Leer el token de acceso desde el archivo
    with open('../serverSalesforce/token.txt', 'r') as f:
        access_token = f.read().strip()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Cookie': 'BrowserId=YMuzjK7_Ee6jljdKN2Nu2g; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
    }
    

    req = urllib.request.Request(url, headers=headers)

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
