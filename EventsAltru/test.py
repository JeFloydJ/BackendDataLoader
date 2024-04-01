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

    #parameters: input csv for change information, csv with changed information
    #description: change personal information in csv file
    #return: csv file with changed information
    def modify_csv_households(self, input_csv, output_csv):
            with open(input_csv, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                data = list(reader)
                name_index = headers.index('Name')

                for row in data:
                    # Dejar solo la primera letra en la columna de nombre
                    if row[name_index]:
                        row[name_index] = row[name_index][:5]

                with open(output_csv, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(data)

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
            address_index = headers.index('Addresses\\Address')
            zip_index = headers.index('Addresses\\ZIP')
            
            for row in data:
                # Dejar solo la primera letra en la columna de nombre
                if row[name_index]:
                    row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                if row[last_name_index]:
                    first_word = row[last_name_index].split()[0]
                    row[last_name_index] = 'x' + first_word + 'x'

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
            phone_index = headers.index('Phones\\Number')

            for row in data:
                # Dejar solo la primera letra en la columna de nombre
                if row[name_index]:
                    row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                if row[last_name_index]:
                    first_word = row[last_name_index].split()[0]
                    row[last_name_index] = 'x' + first_word + 'x'

                # Dejar solo los 3 primeros números en la columna de teléfono
                if row[phone_index]:
                    row[phone_index] = row[phone_index][:5]

            with open(output_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)

    #parameters: input csv for change information, csv with changed information
    #description: change personal information in csv file
    #return: csv file with changed information
    def modify_csv_contacs_address(self, input_csv, output_csv):
            with open(input_csv, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                data = list(reader)
                name_index = headers.index('Name')
                last_name_index = headers.index('Last/Organization/Group/Household name')
                
                address_index = headers.index('Addresses\\Address')
                zip_index = headers.index('Addresses\\ZIP')

                for row in data:
                    # Dejar solo lo primero antes del primer espacio en la columna de dirección
                    if row[address_index]:
                        row[address_index] = row[address_index].split()[0]

                    # Dejar solo los dos primeros caracteres en la columna de código postal
                    if row[zip_index]:
                        row[zip_index] = row[zip_index][:2]

                    # Dejar solo la primera letra en la columna de nombre
                    if row[name_index]:
                        row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                    if row[last_name_index]:
                        first_word = row[last_name_index].split()[0]
                        row[last_name_index] = 'x' + first_word + 'x'

                with open(output_csv, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(data)

    #parameters: input csv for change information, csv with changed information
    #description: change personal information in csv file
    #return: csv file with changed information
    def modify_csv_contacs_email(self, input_csv, output_csv):
            with open(input_csv, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                data = list(reader)
                name_index = headers.index('Name')
                last_name_index = headers.index('Last/Organization/Group/Household name')                
                email_index = headers.index('Email Addresses\\Email address')

                for row in data:
                    # Dejar solo la primera letra en la columna de nombre
                    if row[name_index]:
                        row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                    if row[last_name_index]:
                        first_word = row[last_name_index].split()[0]
                        row[last_name_index] = 'x' + first_word + 'x'

                    # Agregar "@tmail.comx" después del @ en la columna de correo electrónico
                    if '@' in row[email_index]:
                        local, domain = row[email_index].split('@')
                        row[email_index] = local + '@tmail.comx'

                with open(output_csv, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(data)

    #parameters: input csv for change information, csv with changed information
    #description: change personal information in csv file
    #return: csv file with changed information
    def modify_csv_contacs(self, input_csv, output_csv):
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


                with open(output_csv, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(data)

    #parameters: input csv for change information, csv with changed information
    #description: change personal information in csv file
    #return: csv file with changed information
    def modify_csv_phones(self, input_csv, output_csv):
        with open(input_csv, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
            name_index = headers.index('Name')
            last_name_index = headers.index('Last/Organization/Group/Household name')
            phone_index = headers.index('Phones\\Number')

            for row in data:
                # Dejar solo la primera letra en la columna de nombre
                if row[name_index]:
                    row[name_index] = row[name_index][:5]

                # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
                if row[last_name_index]:
                    first_word = row[last_name_index].split()[0]
                    row[last_name_index] = 'x' + first_word + 'x'

                # Dejar solo los 3 primeros números en la columna de teléfono
                if row[phone_index]:
                    row[phone_index] = row[phone_index][:5]

            with open(output_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)



    def process_data(self):
        report_names = ["Veevart Organizations Report test", "Veevart Organization Addresses Report test", "Veevart Organization Phones Report test", "Veevart HouseHolds Report test", "Veevart Contacts Report test", "Veevart Contacts Report Address test", "Veevart Contacts Report Email test", "Veevart Contacts Report Email test", "Veevart Contacts Report Phones test"]
        for report_name in report_names:
            id_value = self.get_id(report_name)
            self.get_query(id_value, report_name)
            self.json_to_csv(f'{report_name}_response.json', f'{report_name}_output.csv')
            if report_name == "Veevart Organizations Report test":
                self.modificar_csv_nombres(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Organization Addresses Report test":
                self.modificar_csv_direcciones(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Organization Phones Report test":
                self.modificar_csv_telefonos(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart HouseHolds Report test":
                self.modify_csv_households(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Contacts Report Address test":
                self.modify_csv_contacs_address(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Contacts Report Email test":
                self.modify_csv_contacs_email(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Contacts Report test":
                self.modify_csv_contacs(f'{report_name}_output.csv', f'{report_name}_output.csv')
            elif report_name == "Veevart Contacts Report Phones test":
                self.modify_csv_phones(f'{report_name}_output.csv', f'{report_name}_output.csv')



class SalesforceProcessor:
    def __init__(self, report_name):
        self.client_id = '3MVG9zeKbAVObYjPODek1PYnJW15VxHyhGPUOe1vzfHcg89tL_3Xyj_DCZQql_RL4Gjdnmk7EpfFk4DGDulnz'
        self.client_secret = '6003041383007768349'  
        self.redirect_uri = "http://localhost:8000"
        self.token_url = "https://test.salesforce.com/services/oauth2/token"
        self.report_name = report_name
        self.address_list = []
        self.account_list = []
        self.phone_list = []
        self.phone_act_list = []
        self.address_act_list = []
        self.houseHolds_list = []
        self.contacts_list = []
        self.contacts_phones_list = []
        self.contacts_emails_list = []
        self.contacts_address_list = []
        self.contacts_id_list = []
        self.contacts_accounts_id = {}
        self.contacts_act_phone = []
        self.contacts_act_email = []

        with open('../serverSalesforce/token.txt', 'r') as f:
            self.access_token = f.read().strip()
        self.sf = Salesforce(instance='customer-velocity-9855-dev-ed.scratch.my.salesforce.com', session_id=self.access_token)

        self.organizations_id = self.get_organizations_id() #id of organizations
        self.households_id = self.get_households_id() #id of households

    #parameters: 
    #description: get recordTypeId for households in org
    #return: return Id of households
    def get_households_id(self):
        query = self.sf.query("SELECT Id FROM RecordType WHERE DeveloperName = 'HH_Account' AND IsActive = true")
        Id = query['records'][0]['Id']
        return Id
    
    #parameters: 
    #description: get recordTypeId for organizations in org
    #return: return Id of organizations
    def get_organizations_id(self):
        query = self.sf.query("SELECT Id FROM RecordType WHERE DeveloperName = 'organization' AND IsActive = true")
        Id = query['records'][0]['Id']
        return Id

    def get_account_id(self):
        query = {}
        ans = self.sf.query_all("SELECT Id, AccountId, Auctifera__Implementation_External_ID__c FROM Contact WHERE Auctifera__Implementation_External_ID__c != null")
        print('query:', ans)
        for record in ans['records']:
            query[record['Auctifera__Implementation_External_ID__c']] = record['AccountId']
        return query
    
    def handle_organizations_report(self, row):
        account_info = {
            'RecordTypeId': self.organizations_id,
            'Auctifera__Implementation_External_ID__c': row['Lookup ID'],
            'Name': row['Name'],
            'Website': row['Web address'],
            'vnfp__Do_not_Email__c' : False if row['Email Addresses\\Do not email'] == '' or row['Email Addresses\\Do not email'] == False else True,
        }
        if row['Email Addresses\\Email address'] != '':
            account_info['vnfp__Email__c'] = row['Email Addresses\\Email address']

        self.account_list.append(account_info)  

    def handle_addresses_report(self, row):
        lookup_id = row['Lookup ID']
        addresses_info = {
            'npsp__MailingStreet__c': row['Addresses\\Address'],
            'npsp__MailingCity__c': row['Addresses\\City'],
            'npsp__MailingState__c': row['Addresses\\State'],
            'npsp__MailingPostalCode__c': row['Addresses\\ZIP'],
            'npsp__MailingCountry__c': row['Addresses\\Country'],
            'npsp__Default_Address__c' : False if row['Addresses\\Primary address'] == '' or row['Addresses\\Primary address'] == False else True,
            'npsp__Household_Account__r': {'Auctifera__Implementation_External_ID__c': lookup_id} # upsert
        }
        self.address_list.append(addresses_info)

    def handle_phone_report(self, row):
        lookup_id = row['Lookup ID']
        phone_info = {
            'vnfp__Type__c' : 'Phone',
            'vnfp__value__c' : row['Phones\\Number'],
            #'vnfp__Do_not_call__c' : row['Phones\\Do not call'],
            'vnfp__Account__r': {'Auctifera__Implementation_External_ID__c': lookup_id}
        }
        self.phone_list.append(phone_info)

    def handler_update_phone_organization(self, row):
        valid = row['Phones\\Primary phone number']
        new_info = {
            'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
            'Phone' : row['Phones\\Number']
        }
        if(valid):
            self.phone_act_list.append(new_info)            

    def handler_update_address_organization(self, row):
        valid = row['Addresses\\Primary address']
        new_info = {
            'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
            #'npsp__Default_Address__c' : row['Addresses\\Address']
            'BillingStreet' : row['Addresses\\Address'],
            'BillingCity' : row['Addresses\\City'],
            'BillingState' : row['Addresses\\State'],
            'BillingPostalCode' : row['Addresses\\ZIP'] ,
            'BillingCountry' : row['Addresses\\Country'],
        }
        if(valid):
            self.address_act_list.append(new_info)            

    #parameters: row with information of households
    #description: sent households info to salesforce
    #return: add information in a list for sent
    def handler_households(self, row):
        #object with info to sent 
        households_info = {
            'RecordTypeId': self.households_id,
            'Auctifera__Implementation_External_ID__c': row['QUERYRECID'],
            'Name': row['Name']
        }
        #add info to list
        self.houseHolds_list.append(households_info)

    #parameters: row with information of contacts
    #description: sent contacts info to salesforce
    #return: add information in a list for sent
    def handler_contacts(self, row):
        #object with info to sent
        account = row['Households Belonging To\\Household Record ID'] 
        gender = '' if row['Gender'] == 'Unknown' else row['Gender'] 
        primary_contact = False if row['Households Belonging To\\Is primary contact'] == '' or row['Households Belonging To\\Is primary contact'] == False else True
        contacts_info = {
            #'Salutation' : row['Title'],
            'FirstName' : row['First name'],
            'LastName' : row['Last/Organization/Group/Household name'],
            'Auctifera__Implementation_External_ID__c' : row['Lookup ID'],
            # 'Description' : row['Notes\\Notes']
            #'GenderIdentity' : row['Gender']
        }
        if account != '':
            contacts_info['Account'] = {'Auctifera__Implementation_External_ID__c': account}
        # print(contacts_info)
        self.contacts_list.append(contacts_info)

    #parameters: row with phones information of the contacts
    #description: sent contacts info to salesforce
    #return: add information in a list for sent
    def handle_contacts_phone_report(self, row):
        lookup_id = row['Lookup ID']
        phone_info = {
            'vnfp__Type__c' : 'Phone',
            'vnfp__value__c' : row['Phones\\Number'],
            #'vnfp__Do_not_call__c' : row['Phones\\Do not call'],
            'vnfp__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id}
        }
        self.contacts_phones_list.append(phone_info)

    #parameters: row with emails information of contacts
    #description: sent contacts info to salesforce
    #return: add information in a list for sent
    def handle_contacts_emails_report(self, row):
        lookup_id = row['Lookup ID']
        email_info = {
            'vnfp__Type__c' : 'Email',
            'vnfp__value__c' : row['Email Addresses\\Email address'],
            #'vnfp__Do_not_call__c' : row['Phones\\Do not call'],
            'vnfp__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id}
        }
        self.contacts_emails_list.append(email_info)

    def handle_contacts_addresses_report(self, row, dic):
        print(row)
        lookup_id = row['Lookup ID']
        #print('dic en address', dic)
        #print(dic[lookup_id])
        addresses_info = {
            'npsp__MailingStreet__c': row['Addresses\\Address'],
            'npsp__MailingCity__c': row['Addresses\\City'],
            'npsp__MailingState__c': row['Addresses\\State'],
            'npsp__MailingPostalCode__c': row['Addresses\\ZIP'],
            'npsp__MailingCountry__c': row['Addresses\\Country'],
            'npsp__Household_Account__c': dic[lookup_id],
            'npsp__Default_Address__c' : False if row['Addresses\\Primary address'] == '' or row['Addresses\\Primary address'] == False else True
        }

        self.contacts_address_list.append(addresses_info)
    def handle_contacts_update_phone(self, row):
        valid = False if row['Phones\\Primary phone number'] == '' or row['Phones\\Primary phone number'] == False else True
        new_info = {
            'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
            'Phone' : row['Phones\\Number']
        }
        if(valid):
            self.contacts_act_phone.append(new_info)       

    def handle_contacts_update_email(self, row):
        valid = False if row['Email Addresses\\Primary email address'] == '' or row['Email Addresses\\Primary email address'] == False else True
        new_info = {
            'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
            'Email' : row['Email Addresses\\Email address']
        }
        if(valid):
            self.contacts_act_email.append(new_info)       
   

    def process_organizations(self):
        with open(f'{self.report_name}_output.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Veevart Organizations Report test' == self.report_name: 
                    self.handle_organizations_report(row)
                elif 'Veevart Organization Phones Report test' == self.report_name: 
                    self.handle_phone_report(row)
                    self.handler_update_phone_organization(row)
                elif 'Veevart Organization Addresses Report test' == self.report_name:
                    self.handle_addresses_report(row)
                    self.handler_update_address_organization(row)

            if self.account_list:
                self.sf.bulk.Account.upsert(self.account_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True)  # update info in account object
            
            if self.phone_list:
                #self.sf.bulk.vnfp__Legacy_Data__c.upsert(self.phone_list, 'Auctifera__Implementation_External_ID__c', batch_size = 'auto', use_serial = True) #sent information in address object
                self.sf.bulk.vnfp__Legacy_Data__c.insert(self.phone_list, batch_size='auto',use_serial=True) #sent information in address object            
            
            if self.address_list:
                self.sf.bulk.npsp__Address__c.insert(self.address_list, batch_size='auto',use_serial=True) #sent information in address object

            if self.phone_act_list:
                self.sf.bulk.Account.upsert(self.phone_act_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update information in account object
            
            if self.address_act_list:
                self.sf.bulk.Account.upsert(self.address_act_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update informacion in address object
    
    def process_households(self):
        with open(f'{self.report_name}_output.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Veevart HouseHolds Report test' == self.report_name:
                    self.handler_households(row)
            
            if self.houseHolds_list:
                self.sf.bulk.account.insert(self.houseHolds_list, batch_size='auto',use_serial=True) #sent information in account(household) object            
    
    def process_contacts(self):
        with open(f'{self.report_name}_output.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Veevart Contacts Report test' == self.report_name:
                    self.handler_contacts(row)
                elif 'Veevart Contacts Report Phones test' == self.report_name:
                    self.handle_contacts_phone_report(row)
                    self.handle_contacts_update_phone(row)
                elif 'Veevart Contacts Report Email test' == self.report_name:
                    self.handle_contacts_emails_report(row)
                    self.handle_contacts_update_email(row)

            if(self.contacts_list):
                results = self.sf.bulk.Contact.upsert(self.contacts_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update information in contact object
                for result in results:
                    if result['success']:
                        self.contacts_id_list.append(result['id'])
                
                self.contacts_accounts_id = self.get_account_id()
                print('dic:', self.contacts_accounts_id)

            # if(self.contacts_phones_list):
            #     print('phones contacts:', self.sf.bulk.vnfp__Legacy_Data__c.insert(self.contacts_phones_list, batch_size='auto',use_serial=True)) 
            
            # if(self.contacts_emails_list):
            #     print('emails contacts:', self.sf.bulk.vnfp__Legacy_Data__c.insert(self.contacts_emails_list, batch_size='auto',use_serial=True)) 
            
            # print('update phones', self.contacts_act_phone)
            # if(self.contacts_act_phone):
            #     print('update phones', self.sf.bulk.Contact.upsert(self.contacts_act_phone, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True)) #update information in account object

            # if(self.contacts_act_email):
            #     print('update emails: ', self.sf.bulk.Contact.upsert(self.contacts_act_email, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True)) #update information in account object

        return self.contacts_accounts_id
    
    def process_contact_address(self):
        with open(f'{self.report_name}_output.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Veevart Contacts Report Address test' == self.report_name:
                    self.handle_contacts_addresses_report(row, self.contacts_accounts_id)

            print(self.contacts_address_list)
            if self.contacts_address_list:
                print('address contacts:', self.sf.bulk.npsp__Address__c.insert(self.contacts_address_list, batch_size='auto',use_serial=True)) #sent information in address object


report_names = ["Veevart Organizations Report test","Veevart Organization Addresses Report test", "Veevart Organization Phones Report test", "Veevart HouseHolds Report test", "Veevart Contacts Report test", "Veevart Contacts Report Address test", "Veevart Contacts Report Email test", "Veevart Contacts Report Email test", "Veevart Contacts Report Phones test"]
dic_accounts = {}

# class Adapter:
#     def __init__(self, report_names):
#         self.data_processor = DataProcessor()
#         self.report_names = report_names

#     def process_data(self):
#         self.data_processor.process_data()
#         dic_accounts = {}
#         for report_name in self.report_names:
#             processor = SalesforceProcessor(report_name)
#             print(report_name)
#             processor.process_organizations()
#             processor.process_households()
#             dic = processor.process_contacts()
#             dic_accounts = {**dic_accounts, **dic}
#             processor.contacts_accounts_id = dic_accounts
#             processor.process_contact_address()

# adapter = Adapter(report_names)
# adapter.process_data()

###########################################################################
#Uso de las clases por separado
###########################################################################
#class SalesforceProcessor:
# Uso de la clase
# for report_name in report_names:
#     processor = SalesforceProcessor(report_name)
#     processor.process_organizations()
#     processor.process_households()
#     dic = processor.process_contacts()
#     dic_accounts = {**dic_accounts, **dic}
#     processor.contacts_accounts_id = dic_accounts
#     processor.process_contact_address()

# Uso de la clase
#class DataProcessor
# processor = DataProcessor()
# processor.process_data()

###########################################################################