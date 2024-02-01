import http.server
import socketserver
import urllib.parse
import requests

# Tus credenciales de Blackbaud ID
client_id = "14ff689a-1054-43ef-a3ec-e3137c3c4a3e"
client_secret = "Y/YJK4+22KtLQt4CTkA3cwVtOXh7B+jpCUQolXYdLfo="
redirect_uri = "http://localhost:8000"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&") if "=" in qc)

        if "code" in query_components:
            code = query_components["code"]
            print(f"Código de autorización recibido: {code}")

            # Solicitar un token de acceso
            token_url = "https://oauth2.sky.blackbaud.com/token"
            token_data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret
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
