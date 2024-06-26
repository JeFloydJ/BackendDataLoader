import requests
import ssl
import json
import re
from simple_salesforce import Salesforce
import boto3
import csv
import os
from io import StringIO

class DataProcessor:
    def __init__(self, bucket_name):
        pass

    def read_s3_object(self, object_key):
        pass
    def write_s3_object(self, object_key, data):
        pass

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

    def modificar_csv_nombres(self, data):
        headers = data[0]
        print(data)
        data = data[1:]
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

            # Cambiar la dirección web a 'https://website.com'
            if row[web_address_index]:
                row[web_address_index] = 'https://website.com'

            # Agregar "@tmail.comx" después del @ en la columna de correo electrónico
            if '@' in row[email_index]:
                local, domain = row[email_index].split('@')
                row[email_index] = local + '@tmail.comx'

        return [headers] + data

    # def modificar_csv_direcciones(self, data):
    #     headers = data[0]
    #     data = data[1:]
    #     name_index = headers.index('Name')
    #     last_name_index = headers.index('Last/Organization/Group/Household name')
    #     address_index = headers.index('Addresses\\Address')
    #     zip_index = headers.index('Addresses\\ZIP')

    #     for row in data:
    #         # Dejar solo la primera letra en la columna de nombre
    #         if row[name_index]:
    #             row[name_index] = row[name_index][:5]

    #         # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
    #         if row[last_name_index]:
    #             first_word = row[last_name_index].split()[0]
    #             row[last_name_index] = 'x' + first_word + 'x'

    #         # Dejar solo lo primero antes del primer espacio en la columna de dirección
    #         if row[address_index]:
    #             row[address_index] = row[address_index].split()[0]

    #         # Dejar solo los dos primeros caracteres en la columna de código postal
    #         if row[zip_index]:
    #             row[zip_index] = row[zip_index][:2]

    #     return [headers] + data

    # def modificar_csv_telefonos(self, data):
    #     headers = data[0]
    #     data = data[1:]
    #     name_index = headers.index('Name')
    #     last_name_index = headers.index('Last/Organization/Group/Household name')
    #     phone_index = headers.index('Phones\\Number')

    #     for row in data:
    #         # Dejar solo la primera letra en la columna de nombre
    #         if row[name_index]:
    #             row[name_index] = row[name_index][:5]

    #         # Dejar solo la primera palabra en la columna de apellido y agregar 'x' al principio y al final
    #         if row[last_name_index]:
    #             first_word = row[last_name_index].split()[0]
    #             row[last_name_index] = 'x' + first_word + 'x'

    #         # Dejar solo los 3 primeros números en la columna de teléfono
    #         if row[phone_index]:
    #             row[phone_index] = row[phone_index][:5]

    #     return [headers] + data


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

    #parameters: input csv for change information, csv with changed information
    #description: change personal information in csv file
    #return: csv file with changed information
    def modify_csv_relationships(self, input_csv, output_csv):
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


    def process_data(self, report_name):
        data = self.read_s3_object(f'{report_name}.csv')
        if report_name == "Veevart Organizations Report test":
            modified_data = self.modificar_csv_nombres(data)
            self.write_s3_object(f'{report_name}_output.csv', modified_data)
        # elif report_name == "Veevart Organization Addresses Report test":
        #     modified_data = self.modificar_csv_direcciones(data)
        #     self.write_s3_object(f'{report_name}_output.csv', modified_data)
        # elif report_name == "Veevart Organization Phones Report test":
        #     modified_data = self.modificar_csv_telefonos(data)
        #     self.write_s3_object(f'{report_name}_output.csv', modified_data)




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
        self.houseHolds_external_ids_list = []
        self.households_ids = {}
        self.valid_check = {}

        with open('../serverSalesforce/token.txt', 'r') as f:
            self.access_token = f.read().strip()
        self.sf = Salesforce(instance='platform-ability-2600-dev-ed.scratch.my.salesforce.com', session_id=self.access_token)

        self.organizations_id = self.get_organizations_id() #id of organizations
        self.households_id = self.get_households_id() #id of households

    #parameters: 
    #description: get number of registers in csv
    #return: return number of registers
    def count_records(self, file_path):
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                return sum(1 for row in reader)-1
        except FileNotFoundError as e:
            return str(e)
    
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

    # def get_account_id(self, offset=0):
    #     query = {}
    #     count = self.count_records('Veevart Contacts Report test_output.csv')
    #     if offset < count:
    #         ans = self.sf.query_all(f"SELECT Id, AccountId, Auctifera__Implementation_External_ID__c FROM Contact WHERE Auctifera__Implementation_External_ID__c != null LIMIT 100 OFFSET {offset}")
    #         for record in ans['records']:
    #             query[record['Auctifera__Implementation_External_ID__c']] = record['AccountId']
    #         query.update(self.get_account_id(offset + 100))
    #     return query


    # def get_account_id(self):
    #     query = {}
    #     # Ordena la consulta por CreatedDate para implementar la paginación
    #     # Limita la consulta a los primeros 2000 registros
    #     ans = self.sf.query("SELECT Id, AccountId, Auctifera__Implementation_External_ID__c FROM Contact WHERE Auctifera__Implementation_External_ID__c != null ORDER BY CreatedDate LIMIT 2000")
    #     # Procesa los registros devueltos en la primera consulta
    #     for record in ans['records']:
    #         query[record['Auctifera__Implementation_External_ID__c']] = record['AccountId']
        
    #     # Si hay más registros disponibles, continua la paginación
    #     # Utiliza el CreatedDate del último registro para consultar la siguiente página
    #     while not ans['done']:
    #         next_records = self.sf.query_more(ans['nextRecordsUrl'], identifier_is_url=True)
    #         for record in next_records['records']:
    #             query[record['Auctifera__Implementation_External_ID__c']] = record['AccountId']
    #         ans = next_records  # Actualiza la variable 'ans' para procesar la siguiente página de resultados

    #     return query

    #parameters: 
    #description: get AccountId for contacts in org
    #return: return hash table like: {'Auctifera__Implementation_External_ID__c': 'AccountId'}
    def get_account_id(self):
        query = {}
        ans = self.sf.query_all("SELECT Id, AccountId, Auctifera__Implementation_External_ID__c FROM Contact WHERE Auctifera__Implementation_External_ID__c != null")

        for record in ans['records']:
            query[record['Auctifera__Implementation_External_ID__c']] = record['AccountId']
        return query
    
    def find_households_id(self, lst):
        dic = {}
        for element in lst:
            match = re.search(r'(\d+)-households-(.*)', element)
            if match:
                id = match.group(2)
                dic[id] = element
        return dic
    
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

    def handle_addresses_report(self, row, counter):
        lookup_id = row['Lookup ID']
        addresses_info = {
            'npsp__MailingStreet__c': row['Addresses\\Address'],
            'npsp__MailingCity__c': row['Addresses\\City'],
            'npsp__MailingState__c': row['Addresses\\State'],
            'npsp__MailingPostalCode__c': row['Addresses\\ZIP'],
            'npsp__MailingCountry__c': row['Addresses\\Country'],
            'npsp__Default_Address__c' : False if row['Addresses\\Primary address'] == '' or row['Addresses\\Primary address'] == False else True,
            'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'address'+ '-organization' + '-' + row['QUERYRECID']),
            #'Implementation_External_ID__c' : str(str(counter)+ '-' + 'address'+ '-organization' + '-' + row['QUERYRECID']),
            'npsp__Household_Account__r': {'Auctifera__Implementation_External_ID__c': lookup_id} # upsert
        }
        self.address_list.append(addresses_info)

    def handle_phone_report(self, row, counter):
        lookup_id = row['Lookup ID']
        phone_info = {
            'vnfp__Type__c' : 'Phone',
            'vnfp__value__c' : row['Phones\\Number'],
            #'vnfp__Do_not_call__c' : row['Phones\\Do not call'],
            'vnfp__Account__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
            'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'phone' + '-' + row['QUERYRECID'])
            #'Implementation_External_ID__c' : str(str(counter)+ '-' + 'phone' + '-' + row['QUERYRECID'])
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
    def handler_households(self, row, counter):
        #object with info to sent
        self.houseHolds_external_ids_list.append(str( str(counter) + '-' + 'households' +'-'+row['QUERYRECID'])) 
        households_info = {
            'RecordTypeId': self.households_id,
            'Auctifera__Implementation_External_ID__c': str( str(counter) + '-' + 'households' +'-'+row['QUERYRECID']),
            'Name': row['Name']
        }
        #add info to list
        self.houseHolds_list.append(households_info)

    #parameters: row with information of contacts
    #description: sent contacts info to salesforce
    #return: add information in a list for sent
    def handler_contacts(self, row, dic):
        #object with info to sent
        account = row['Households Belonging To\\Household Record ID'] 
        contacts_info = {
            'Salutation' : row['Title'],
            'FirstName' : row['First name'],
            'LastName' : row['Last/Organization/Group/Household name'],
            'Auctifera__Implementation_External_ID__c' : row['Lookup ID'],
            'Description' : row['Notes\\Notes'],
            'GenderIdentity' : row['Gender'],
        }
        if account != '':
            contacts_info['Account'] = {'Auctifera__Implementation_External_ID__c': dic[account]}

        self.contacts_list.append(contacts_info)

    #parameters: row with phones information of the contacts
    #description: sent contacts info to salesforce
    #return: add information in a list for sent
    def handle_contacts_phone_report(self, row, counter):
        lookup_id = row['Lookup ID']
        phone_info = {
            'vnfp__Type__c' : 'Phone',
            'vnfp__value__c' : row['Phones\\Number'],
            #'vnfp__Do_not_call__c' : row['Phones\\Do not call'],
            'vnfp__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
            'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'phone' + '-' + row['QUERYRECID']),
            #'Implementation_External_ID__c' : str(str(counter)+ '-' + 'phone' + '-' + row['QUERYRECID'])
        }
        self.contacts_phones_list.append(phone_info)

    #parameters: row with emails information of contacts
    #description: sent contacts info to salesforce
    #return: add information in a list for sent
    def handle_contacts_emails_report(self, row, counter):
        lookup_id = row['Lookup ID']
        email_info = {
            'vnfp__Type__c' : 'Email',
            'vnfp__value__c' : row['Email Addresses\\Email address'],
            #'vnfp__Do_not_call__c' : row['Phones\\Do not call'],
            'vnfp__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
            'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'contacts-email' + '-' + row['QUERYRECID'])
            #'Implementation_External_ID__c' : str(str(counter)+ '-' + 'contacts-email' + '-' + row['QUERYRECID'])

        }
        self.contacts_emails_list.append(email_info)

    def handle_contacts_addresses_report(self, row, dic, counter):
        lookup_id = row['Lookup ID']
        # print('dic en address', dic)
        addresses_info = {
            'npsp__MailingStreet__c': row['Addresses\\Address'],
            'npsp__MailingCity__c': row['Addresses\\City'],
            'npsp__MailingState__c': row['Addresses\\State'],
            'npsp__MailingPostalCode__c': row['Addresses\\ZIP'],
            'npsp__MailingCountry__c': row['Addresses\\Country'],
            'npsp__Household_Account__c': dic[lookup_id],
            'npsp__Default_Address__c' : False if row['Addresses\\Primary address'] == '' or row['Addresses\\Primary address'] == False else True,
            'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'contacts-address' + '-' + 'contacts' +row['QUERYRECID'])
            #'Implementation_External_ID__c' : str(str(counter)+ '-' + 'contacts-address' + '-' + 'contacts' +row['QUERYRECID'])
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
        if valid and self.valid_check.get(row['Lookup ID'], None) == None:
            self.contacts_act_email.append(new_info)       
            self.valid_check[row['Lookup ID']] = True
            print(self.valid_check)

    def process_organizations(self):
        counter = 0
        with open(f'{self.report_name}_output.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                counter += 1
                if 'Veevart Organizations Report test' == self.report_name: 
                    self.handle_organizations_report(row)
                elif 'Veevart Organization Phones Report test' == self.report_name: 
                    self.handle_phone_report(row, counter)
                    self.handler_update_phone_organization(row)
                elif 'Veevart Organization Addresses Report test' == self.report_name:
                    self.handle_addresses_report(row, counter)
                    self.handler_update_address_organization(row)

            if self.account_list:
                self.sf.bulk.Account.upsert(self.account_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True)  # update info in account object
            
            #print('phone organizations:', self.phone_act_list)
            if self.phone_list:
                #self.sf.bulk.vnfp__Legacy_Data__c.upsert(self.phone_list, 'Auctifera__Implementation_External_ID__c', batch_size = 'auto', use_serial = True) #sent information in address object
                self.sf.bulk.vnfp__Legacy_Data__c.upsert(self.phone_list, 'vnfp__Implementation_External_ID__c', batch_size='auto',use_serial=True) #sent information in address object            
            
            #print('address organizations:', self.address_list)
            if self.address_list:
                self.sf.bulk.npsp__Address__c.upsert(self.address_list, 'vnfp__Implementation_External_ID__c', batch_size='auto',use_serial=True) #sent information in address object

            if self.phone_act_list:
                self.sf.bulk.Account.upsert(self.phone_act_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update information in account object
            
            if self.address_act_list:
                self.sf.bulk.Account.upsert(self.address_act_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update informacion in address object
    

    def process_households(self):
        counter = 0
        with open(f'{self.report_name}_output.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                counter += 1
                if 'Veevart HouseHolds Report test' == self.report_name:
                    self.handler_households(row, counter)
                
            if self.houseHolds_list:
 #               self.sf.bulk.account.insert(self.houseHolds_list, batch_size='auto',use_serial=True) #sent information in account(household) object            
                  self.sf.bulk.Account.upsert(self.houseHolds_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update informacion in address object
        
        return self.houseHolds_external_ids_list
    
    def process_households_ids(self):
        self.households_ids = self.find_households_id(self.houseHolds_external_ids_list)
        return self.households_ids
    
    def process_contacts(self):
        counter = 0
        with open(f'{self.report_name}_output.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                counter += 1
                if 'Veevart Contacts Report test' == self.report_name:
                    self.handler_contacts(row, self.households_ids)
                elif 'Veevart Contacts Report Phones test' == self.report_name:
                    self.handle_contacts_phone_report(row, counter)
                    self.handle_contacts_update_phone(row)
                elif 'Veevart Contacts Report Email test' == self.report_name:
                    self.handle_contacts_emails_report(row, counter)
                    self.handle_contacts_update_email(row)
                   
             
            if self.contacts_list:
                results = self.sf.bulk.Contact.upsert(self.contacts_list, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update information in contact object
                for result in results:
                    if result['success']:
                        self.contacts_id_list.append(result['id'])
                
                self.contacts_accounts_id = self.get_account_id()

            if self.contacts_phones_list:
                self.sf.bulk.vnfp__Legacy_Data__c.upsert(self.contacts_phones_list, 'vnfp__Implementation_External_ID__c', batch_size='auto',use_serial=True) 
            
            if self.contacts_emails_list:
                self.sf.bulk.vnfp__Legacy_Data__c.upsert(self.contacts_emails_list, 'vnfp__Implementation_External_ID__c', batch_size='auto',use_serial=True) 
            
            if self.contacts_act_phone:
                self.sf.bulk.Contact.upsert(self.contacts_act_phone, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update information in account object
            
            #print('update emails contacts', self.contacts_act_email)
            if self.contacts_act_email:
                self.sf.bulk.Contact.upsert(self.contacts_act_email, 'Auctifera__Implementation_External_ID__c', batch_size='auto',use_serial=True) #update information in account object

        return self.contacts_accounts_id
    
    def process_contact_address(self):
        with open(f'{self.report_name}_output.csv', 'r') as f:
            counter = 0
            reader = csv.DictReader(f)
            for row in reader:
                counter += 1
                if 'Veevart Contacts Report Address test' == self.report_name:
                    self.handle_contacts_addresses_report(row, self.contacts_accounts_id, counter)

            # print('update address contacts', self.contacts_address_list)
            if self.contacts_address_list:
                self.sf.bulk.npsp__Address__c.upsert(self.contacts_address_list, 'vnfp__Implementation_External_ID__c', batch_size='auto',use_serial=True)  #sent information in address object


# report_names = ["Veevart Organizations Report test","Veevart Organization Addresses Report test", "Veevart Organization Phones Report test", "Veevart HouseHolds Report test", "Veevart Contacts Report test", "Veevart Contacts Report Address test", "Veevart Contacts Report Email test", "Veevart Contacts Report Email test", "Veevart Contacts Report Phones test"]
# dic_accounts = {}
# dic_households_ids = {}
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
#     #processor.process_organizations()
#     processor.process_households()
#     dic_households_ids = {**dic_households_ids, **processor.process_households_ids()}
#     processor.households_ids = dic_households_ids
#     dic = processor.process_contacts()
#     dic_accounts = {**dic_accounts, **dic}
#    # processor.process_contact_address()

# Uso de la clase
#class DataProcessor
# processor = DataProcessor()
# processor.process_data()


# Crear una instancia de la clase DataProcessor
processor = DataProcessor('veevartpdf')

# Llamar al método process_data para cada reporte
reports = ["Veevart Organizations Report test", "Veevart Organization Addresses Report test", "Veevart Organization Phones Report test"]
for report in reports:
    processor.process_data(report)
###########################################################################