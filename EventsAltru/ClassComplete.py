import datetime
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

    def get_id(self, report_name):
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
                return self.get_id(report_name)  # Llama a la función de nuevo después de actualizar el token

            response_json = json.loads(response.text)
            id_value = response_json.get('id', None)

            return id_value

        except requests.exceptions.RequestException as e:
            print(e)

    def get_query(self, id, report_name):
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
                return self.get_query(id, report_name)  # Llama a la función de nuevo después de actualizar el token

            response_json = json.loads(response.text)

            # Guardar la respuesta en un archivo JSON
            with open(f'{report_name}_response.json', 'w') as f:
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

    def modificar_csv_nombres(self, input_csv, output_csv):
        with open(input_csv, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
            email_index = headers.index('Email Addresses\\Email address')
            web_address_index = headers.index('Web address')
            name_index = headers.index('Name')
            last_name_index = headers.index('Last/Organization/Group/Household name')

            for row in data:
                # Dejar solo la primera letra en la columna de nombre
                if row[name_index]:
                    row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                if row[last_name_index]:
                    first_word = row[last_name_index].split()[0]
                    row[last_name_index] = 'x' + first_word + 'x'

                if row[web_address_index]:
                    protocol, rest = row[web_address_index].split('//')
                    domain, path = rest.split('.com', 1)
                    row[web_address_index] = protocol + '//website.com' + path

                # Agregar "@tmail.comx" después del @ en la columna de correo electrónico
                if '@' in row[email_index]:
                    local, domain = row[email_index].split('@')
                    row[email_index] = local + '@tmail.comx'

            with open(output_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)

    def modificar_csv_direcciones(self, input_csv, output_csv):
        with open(input_csv, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
            name_index = headers.index('Name')
            last_name_index = headers.index('Last/Organization/Group/Household name')

            for row in data:
                # Dejar solo la primera letra en la columna de nombre
                if row[name_index]:
                    row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                if row[last_name_index]:
                    first_word = row[last_name_index].split()[0]
                    row[last_name_index] = 'x' + first_word + 'x'


            address_index = headers.index('Addresses\\Address')
            zip_index = headers.index('Addresses\\ZIP')

            for row in data:
                # Dejar solo lo primero antes del primer espacio en la columna de dirección
                if row[address_index]:
                    row[address_index] = row[address_index].split()[0]

                # Dejar solo los dos primeros caracteres en la columna de código postal
                if row[zip_index]:
                    row[zip_index] = row[zip_index][:2]

            with open(output_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)

    def modificar_csv_telefonos(self, input_csv, output_csv):
        with open(input_csv, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
            name_index = headers.index('Name')
            last_name_index = headers.index('Last/Organization/Group/Household name')

            for row in data:
                # Dejar solo la primera letra en la columna de nombre
                if row[name_index]:
                    row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                if row[last_name_index]:
                    first_word = row[last_name_index].split()[0]
                    row[last_name_index] = 'x' + first_word + 'x'


            phone_index = headers.index('Phones\\Number')

            for row in data:
                # Dejar solo los 3 primeros números en la columna de teléfono
                if row[phone_index]:
                    row[phone_index] = row[phone_index][:5]

            with open(output_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)

    def process_data(self):
        report_names = ["Veevart Organizations Report test", "Veevart Organization Addresses Report test", "Veevart Organization Phones Report test"]
        for report_name in report_names:
            id_value = self.get_id(report_name)
            self.get_query(id_value, report_name)
            self.json_to_csv(f'{report_name}_response.json', f'{report_name}_output.csv')
            headers_eliminar = ["QUERYRECID"]
            self.eliminar_columnas(f'{report_name}_output.csv', headers_eliminar, f'{report_name}_output.csv')
            if report_name == "Veevart Organizations Report test":
                self.modificar_csv_nombres(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Organization Addresses Report test":
                self.modificar_csv_direcciones(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Organization Phones Report test":
                self.modificar_csv_telefonos(f'{report_name}_output.csv', f'{report_name}_output.csv')



class SalesforceProcessor:
    def __init__(self, csv_file_path):
        self.client_id = '3MVG9zeKbAVObYjPODek1PYnJW15VxHyhGPUOe1vzfHcg89tL_3Xyj_DCZQql_RL4Gjdnmk7EpfFk4DGDulnz'
        self.client_secret = '6003041383007768349'  
        self.redirect_uri = "http://localhost:8000"
        self.token_url = "https://test.salesforce.com/services/oauth2/token"
        self.csv_file_path = csv_file_path

        with open('../serverSalesforce/token.txt', 'r') as f:
            self.access_token = f.read().strip()
        self.sf = Salesforce(instance='energy-customer-8575-dev-ed.scratch.my.salesforce.com', session_id=self.access_token)

    def contar_registros_grande(self, nombre_archivo):
        with open(nombre_archivo, 'r') as f:
            reader = csv.reader(f)
            num_registros = sum(1 for row in reader) - 1  # Restamos 1 para excluir el encabezado
        return num_registros
    
    def check_custom_object_exists(self, object_name):
        try:
            getattr(self.sf, object_name).describe()
            return True
        except Exception as e:
            return False


    # Modificar el método process_csv para manejar múltiples números de teléfono por cuenta
    def process_csv(self, report_names):

        # if not SalesforceProcessor.check_custom_object_exists(self.sf, "Phone__c"):
        #     mdapi = self.sf.mdapi
        #     custom_object = mdapi.CustomObject(
        #         fullName = "Phone__c",
        #         label = "Phone",
        #         pluralLabel = "Phones",
        #         nameField = mdapi.CustomField(
        #             label = "Name",
        #             type = mdapi.FieldType("Text")
        #         ),
        #         deploymentStatus = mdapi.DeploymentStatus("Deployed"),
        #         sharingModel = mdapi.SharingModel("Read")
        #     )

        #     mdapi.CustomObject.create(custom_object)

        #     # Crear los campos Phone y Do not call
        #     phone_field = mdapi.CustomField(
        #         fullName = "Phone__c.Phone__c",
        #         label = "Phone",
        #         type = mdapi.FieldType("Phone"),
        #         required = False
        #     )

        #     do_not_call_field = mdapi.CustomField(
        #         fullName = "Phone__c.Do_not_call__c",
        #         label = "Do not call",
        #         type = mdapi.FieldType("Checkbox"),
        #         defaultValue = False
        #     )

        #     mdapi.CustomField.create(phone_field)
        #     mdapi.CustomField.create(do_not_call_field)

        for report_name in report_names:
            num_registros = self.contar_registros_grande(f'{report_name}_output.csv')
            print(f'El archivo tiene {num_registros} registros.')

            with open(f'{report_name}_output.csv', 'r') as f:
                reader = csv.DictReader(f)
                account_info_list = []
                for row in reader:
                    # Obtener el ID del RecordType basado en el valor del campo 'Type'
                    ##record_type = self.sf.query(f"SELECT Id FROM RecordType WHERE DeveloperName = '{row['Type']}' AND isActive = TRUE")
                    #record_type_id = record_type['records'][0]['Id'] if record_type['records'] else ''
                    if report_name == 'Veevart Organizations Report test_output.csv':
                        account_info = {
                            'Auctifera__Implementation_External_ID__c': row['Lookup ID'],
                            'Name': row['Name'],
                            'Website': row['Web address'],
                            'vnfp__Email__c': row['Email Addresses\\Email address'],
                        }
                        account_info_list.append(account_info)

                        if report_name == "Veevart Organization Phones Report test_output.csv":
                            # Crear un nuevo objeto de teléfono
                            phone_info = {
                                'Phone__c': row['Phones\\Number'],
                                'Do_not_call__c': row['Phones\\Do not call'].lower() == 'true',
                            }

                            # Verificar si la cuenta ya tiene un número de teléfono
                            account = self.sf.Account.get_by_custom_id('Auctifera__Implementation_External_ID__c', row['Lookup ID'])

                            if account['Phone']:
                                # Si la cuenta ya tiene un número de teléfono, crear un nuevo objeto de teléfono y relacionarlo con la cuenta
                                phone_info['AccountId__c'] = account['Id']
                                self.sf.Phone__c.create(phone_info)
                            else:
                                # Si la cuenta no tiene un número de teléfono, actualizar el número de teléfono de la cuenta
                                self.sf.Account.update(account['Id'], {'Phone': phone_info['Phone__c']})

                        if report_name == "Veevart Organization Addresses Report test_output.csv":
                            # Crear un nuevo objeto de dirección
                            address_info = {
                                'BillingStreet': row['Addresses\\Address'],
                                'BillingCity': row['Addresses\\City'],
                                'BillingState': row['Addresses\\State'],
                                'BillingPostalCode': row['Addresses\\ZIP'],
                                'BillingCountry': row['Addresses\\Country'],
                            }

                            # Verificar si la cuenta ya tiene una dirección
                            account = self.sf.Account.get_by_custom_id('Auctifera__Implementation_External_ID__c', row['Lookup ID'])

                            if account['BillingStreet']:
                                # Si la cuenta ya tiene una dirección, crear un nuevo objeto de dirección y relacionarlo con la cuenta
                                address_info['AccountId__c'] = account['Id']
                                self.sf.Address.create(address_info)
                            else:
                                # Si la cuenta no tiene una dirección, actualizar la dirección de la cuenta
                                self.sf.Account.update(account['Id'], address_info)

            try:
                results = self.sf.bulk.Account.upsert(account_info_list, 'Auctifera__Implementation_External_ID__c', batch_size=num_registros)
                for result in results:
                    if result['success']:
                        print(f"Registro con ID {result['id']} actualizado o insertado exitosamente.")
                    else:
                        print(f"Error al actualizar o insertar el registro: {result['errors']}")

            except Exception as e:
                if 'INVALID_SESSION_ID' in str(e):  # El token de acceso ha expirado
                    print("El token de acceso ha expirado. Actualizando el token...")
                    access_token = self.refresh_token()
                    if access_token is None:
                        print("No se pudo actualizar el token de acceso. Por favor, verifica tus credenciales y vuelve a intentarlo.")
                    else:
                        self.sf = Salesforce(instance='energy-customer-8575-dev-ed.scratch.my.salesforce.com', session_id=access_token)
                else:
                    print(e)

class Adapter:
    def __init__(self, report_names):
        self.data_processor = DataProcessor()
        self.salesforce_processors = [SalesforceProcessor(report_name) for report_name in report_names]

    def process_data(self):
        self.data_processor.process_data()
        for salesforce_processor in self.salesforce_processors:
            salesforce_processor.process_csv(report_names)

report_names = ["Veevart Organizations Report test", "Veevart Organization Addresses Report test", "Veevart Organization Phones Report test"]
adapter = Adapter(report_names)
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
# processor = DataProcessor()
# processor.process_data()

###########################################################################