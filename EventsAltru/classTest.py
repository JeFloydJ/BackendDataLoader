import requests
import ssl
import json
import csv
from simple_salesforce import Salesforce

class DataProcessor:
    def __init__(self):
        self.client_id = "14ff689a-1054-43ef-a3ec-e3137c3c4a3e"
        self.client_secret = "Y/YJK4+22KtLQt4CTkA3cwVtOXh7B+jpCUQolXYdLfo="
        self.token_url = "https://oauth2.sky.blackbaud.com/token"
        self.subscription_key = 'fa43a7b522a54b718178a4af6727392f'
        ssl._create_default_https_context = ssl._create_stdlib_context

    def refresh_token(self):
        with open('../serverAltru/refresh_token.txt', 'r') as f:
            refresh_token = f.read().strip()

        token_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        token_response = requests.post(self.token_url, data=token_data)

        if token_response.status_code == 200:
            new_access_token = token_response.json()["access_token"]
            print(f"Nuevo token de acceso: {new_access_token}")

            with open('../serverAltru/token.txt', 'w') as f:
                f.write(new_access_token)
        else:
            print(f"Error al actualizar el token de acceso: {token_response.content}")

    def get_id(self):
        report_name = 'test1'
        url = f"https://api.sky.blackbaud.com/alt-anamg/adhocqueries/id/{report_name}"

        with open('../serverAltru/token.txt', 'r') as f:
            access_token = f.read().strip()

        headers = {
            'Cache-Control': 'no-cache',
            'Authorization': f'Bearer {access_token}',
            'Bb-Api-Subscription-Key': self.subscription_key
        }

        try:
            response = requests.request("GET", url, headers=headers)

            if response.status_code == 401:  # Unauthorized
                print("El token de acceso ha expirado. Actualizando el token...")
                self.refresh_token()
                return self.get_id()  # Llama a la función de nuevo después de actualizar el token

            response_json = json.loads(response.text)
            id_value = response_json.get('id', None)

            return id_value

        except requests.exceptions.RequestException as e:
            print(e)

    def get_query(self, id):
        url = f"https://api.sky.blackbaud.com/alt-anamg/adhocqueries/{id}"

        with open('../serverAltru/token.txt', 'r') as f:
            access_token = f.read().strip()

        headers = {
            'Cache-Control': 'no-cache',
            'Authorization': f'Bearer {access_token}',
            'Bb-Api-Subscription-Key': self.subscription_key
        }

        try:
            response = requests.request("GET", url, headers=headers)

            if response.status_code == 401:  # Unauthorized
                print("El token de acceso ha expirado. Actualizando el token...")
                self.refresh_token()
                return self.get_query(id)  # Llama a la función de nuevo después de actualizar el token

            response_json = json.loads(response.text)

            # Guardar la respuesta en un archivo JSON
            with open('response.json', 'w') as f:
                json.dump(response_json, f)

        except requests.exceptions.RequestException as e:
            print(e)

    def json_to_csv(self, json_file_path, csv_file_path):
        # Abre y carga el archivo JSON
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Abre el archivo CSV en modo escritura
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # Escribe los nombres de los campos en la primera fila
            writer.writerow(data['field_names'])

            # Escribe las filas de datos
            for row in data['rows']:
                writer.writerow(row)

    def eliminar_columnas(self, csv_input, headers_eliminar, csv_output):
        # Leer el archivo CSV
        with open(csv_input, 'r') as f:
            rows = list(csv.reader(f))
        
        headers = rows[0]
        
        # Encontrar los índices de las columnas a eliminar
        indices_eliminar = [headers.index(header) for header in headers_eliminar if header in headers]
        
        # Eliminar las columnas
        rows = [[value for i, value in enumerate(row) if i not in indices_eliminar] for row in rows]
        
        # Guardar las filas en un nuevo archivo CSV
        with open(csv_output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def process_data(self):
        id_value = self.get_id()
        self.get_query(id_value)
        self.json_to_csv('response.json', 'output.csv')
        headers_eliminar = ["Lookup ID", "QUERYRECID"]
        self.eliminar_columnas('output.csv', headers_eliminar, 'output.csv')


class SalesforceProcessor:
    def __init__(self, csv_file_path):
        self.client_id = '3MVG9zeKbAVObYjPODek1PYnJW15VxHyhGPUOe1vzfHcg89tL_3Xyj_DCZQql_RL4Gjdnmk7EpfFk4DGDulnz'
        self.client_secret = '6003041383007768349'  
        self.redirect_uri = "http://localhost:8000"
        self.token_url = "https://login.salesforce.com/services/oauth2/token"
        self.csv_file_path = csv_file_path
        with open('../serverSalesforce/token.txt', 'r') as f:
            self.access_token = f.read().strip()
        self.sf = Salesforce(instance='veevartdevstage.my.salesforce.com', session_id=self.access_token)

    def contar_registros_grande(self, nombre_archivo):
        with open(nombre_archivo, 'r') as f:
            reader = csv.reader(f)
            num_registros = sum(1 for row in reader) - 1  # Restamos 1 para excluir el encabezado
        return num_registros

    def refresh_token(self):
        with open('../serverSalesforce/refresh_token.txt', 'r') as f:
            refresh_token = f.read().strip()

        token_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        token_response = requests.post(self.token_url, data=token_data)

        if token_response.status_code == 200:
            new_access_token = token_response.json()["access_token"]
            print(f"Nuevo token de acceso: {new_access_token}")

            with open('../serverSalesforce/token.txt', 'w') as f:
                f.write(new_access_token)
            return new_access_token
        else:
            print(f"Error al actualizar el token de acceso: {token_response.content}")
            return None

    def process_csv(self):
        num_registros = self.contar_registros_grande(self.csv_file_path)
        print(f'El archivo tiene {num_registros} registros.')

        with open(self.csv_file_path, 'r') as f:
            reader = csv.DictReader(f)
            contact_info_list = []
            for row in reader:
                contact_info = {
                    'LastName': row['Name'],
                    'Email': row['Email Addresses\\Email address']
                }
                contact_info_list.append(contact_info)

            try:
                results = self.sf.bulk.Contact.insert(contact_info_list, batch_size=num_registros)
                for result in results:
                    if result['success']:
                        print(f"Registro con ID {result['id']} insertado exitosamente.")
                    else:
                        print(f"Error al insertar el registro: {result['errors']}")
            except Exception as e:
                if 'INVALID_SESSION_ID' in str(e):  # El token de acceso ha expirado
                    print("El token de acceso ha expirado. Actualizando el token...")
                    access_token = self.refresh_token()
                    if access_token is None:
                        print("No se pudo actualizar el token de acceso. Por favor, verifica tus credenciales y vuelve a intentarlo.")
                    else:
                        self.sf = Salesforce(instance='veevartdevstage.my.salesforce.com', session_id=access_token)
                else:
                    print(e)
class Adapter:
    def __init__(self, csv_file_path):
        self.data_processor = DataProcessor()
        self.salesforce_processor = SalesforceProcessor(csv_file_path)

    def process_data(self):
        self.data_processor.process_data()
        self.salesforce_processor.process_csv()

# Uso de la clase
adapter = Adapter('../EventsAltru/output.csv')
adapter.process_data()

###########################################################################
#Uso de las clases por separado
###########################################################################
#class SalesforceProcessor:
# Uso de la clase
#processor = SalesforceProcessor('../EventsAltru/output.csv')
#processor.process_csv()



# Uso de la clase
#class DataProcessor
#processor = DataProcessor()
#processor.process_data()

###########################################################################