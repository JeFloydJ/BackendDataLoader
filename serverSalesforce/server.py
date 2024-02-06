# server.py
import http.server
import socketserver
import urllib.parse
import requests

# Tus credenciales de Salesforce
client_id = '3MVG9zeKbAVObYjPODek1PYnJW15VxHyhGPUOe1vzfHcg89tL_3Xyj_DCZQql_RL4Gjdnmk7EpfFk4DGDulnz'
client_secret = '6003041383007768349'  
redirect_uri = "http://localhost:8000"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&") if "=" in qc)

        if "code" in query_components:
            code = query_components["code"]
            print(f"Código de autorización recibido: {code}")
            access_token = query_components["code"]
            access_token = access_token.replace("%3D%3D", "==")
            with open('token.txt', 'w') as f:
                f.write(access_token)
             # Solicitar un token de acceso
            token_url = "https://login.salesforce.com/services/oauth2/token"
            token_data = {
                "grant_type" : "authorization_code",
                "code": access_token,
                "client_id" : client_id,
                "client_secret" : client_secret,
                "redirect_uri" : redirect_uri
            }
            token_response = requests.post(token_url, data=token_data)
            
            if token_response.status_code == 200:
                access_token = token_response.json()["access_token"]
                refresh_token = token_response.json()["refresh_token"]
                print(f"Token de acceso recibido: {access_token}")
                with open('token.txt', 'w') as f:
                    f.write(access_token)
                with open('refresh_token.txt', 'w') as f:
                    f.write(refresh_token)
            else:
                print(f"Error al solicitar el token de acceso: {token_response.content}")
                          
        self.send_response(200)
        self.end_headers()

PORT = 8000
handler = socketserver.TCPServer(("", PORT), MyHttpRequestHandler)

print("Sirviendo en el puerto", PORT)
handler.serve_forever()
