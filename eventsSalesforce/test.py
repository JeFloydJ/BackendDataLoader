import csv
from simple_salesforce import Salesforce
import requests

def refresh_token():
    # Tus credenciales de Salesforce
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
        return new_access_token
    else:
        print(f"Error al actualizar el token de acceso: {token_response.content}")
        return None

# Leer el token de acceso desde el archivo
with open('../serverSalesforce/token.txt', 'r') as f:
    access_token = f.read().strip()

sf = Salesforce(instance='veevartdevstage.my.salesforce.com', session_id=access_token)

# Leer el archivo CSV
with open('../EventsAltru/output.csv', 'r') as f:
    reader = csv.DictReader(f)
    contact_info_list = []
    for row in reader:
        # Crear un contacto en Salesforce con la información del archivo CSV
        contact_info = {
            'LastName': row['Name'],
            'Email': row['Email Addresses\\Email address']
        }
        contact_info_list.append(contact_info)

    try:
        results = sf.bulk.Contact.insert(contact_info_list, batch_size=12288)
        for result in results:
            if result['success']:
                print(f"Registro con ID {result['id']} insertado exitosamente.")
            else:
                print(f"Error al insertar el registro: {result['errors']}")
    except Exception as e:
        if 'INVALID_SESSION_ID' in str(e):  # El token de acceso ha expirado
            print("El token de acceso ha expirado. Actualizando el token...")
            access_token = refresh_token()
            if access_token is None:
                print("No se pudo actualizar el token de acceso. Por favor, verifica tus credenciales y vuelve a intentarlo.")
            else:
                sf = Salesforce(instance='veevartdevstage.my.salesforce.com', session_id=access_token)
        else:
            print(e)
