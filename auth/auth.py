
import requests

"""
app de prueba:
client_id = '14ff689a-1054-43ef-a3ec-e3137c3c4a3e'
client_secret = 'Y/YJK4+22KtLQt4CTkA3cwVtOXh7B+jpCUQolXYdLfo='
token_url = 'https://oauth2.sky.blackbaud.com/token'
"""

# Tus credenciales de Blackbaud ID
client_id = "14ff689a-1054-43ef-a3ec-e3137c3c4a3e"
client_secret = "Y/YJK4+22KtLQt4CTkA3cwVtOXh7B+jpCUQolXYdLfo="
redirect_uri = "http://localhost:8000"
response_type = "code"
# URL de autenticación de Blackbaud
url = f"https://app.blackbaud.com/oauth/authorize?redirect_uri={redirect_uri}&client_secret={client_secret}&client_id={client_id}&response_type={response_type}"

payload = {}
headers = {}

# Realizar la solicitud de autenticación
response = requests.request("GET", url, headers=headers, data=payload)

print(response.url)

"""
# Verificar si la autenticación fue exitosa
if response.status_code == 200:
    print("Autenticación exitosa!")
    access_token = response.json()["access_token"]
else:
    print(f"Error en la autenticación: {response.content}")
"""