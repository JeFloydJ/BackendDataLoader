import csv
import json


file_path = '/Users/juanestebanfloyd/Documents/AltruFinaltest/logs/organizations_response.txt'
file_path_json = '/Users/juanestebanfloyd/Documents/AltruFinaltest/logs/organizations_response.json'

with open(file_path, 'r') as file, open(file_path_json, 'w') as file_json:
    for line in file:
        new_line = line.replace("'", '"').replace("True", 'true').replace("False", 'false').replace("None", 'null')
        file_json.write(new_line)  


with open(file_path_json) as json_file:
    data = json.load(json_file)
    print(data[0])


def generate_report_send_data(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
        
        # Inicializar contadores y listas
        success_true = 0
        success_false = 0
        created_true = 0
        created_false = 0
        success_ids_true = []
        success_ids_false = []
        created_ids_true = []
        created_ids_false = []
        errors_list = []

        # Analizar los datos
        for item in data:
            if item['success']:
                success_true += 1
                success_ids_true.append(item['id'])
            else:
                success_false += 1
                success_ids_false.append(item['id'])
            
            if item['created']:
                created_true += 1
                created_ids_true.append(item['id'])
            else:
                created_false += 1
                created_ids_false.append(item['id'])
            
            if item['errors']:
                for error in item['errors']:
                    errors_list.append({'id': item['id'], 'error': error})

        # Crear el archivo CSV
        with open('reportOfSentData.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Escribir encabezados
            writer.writerow(['Operation', 'True', 'False', 'Id', 'Error', 'Message Error'])
            
            # Escribir datos de Success
            writer.writerow(['Success', success_true, success_false, '', '', ''])
            for id in success_ids_true:
                writer.writerow(['', '', '', id, '', ''])
            for id in success_ids_false:
                writer.writerow(['', '', '', id, '', ''])
            
            # Escribir datos de Created
            writer.writerow(['Created', created_true, created_false, '', '', ''])
            for id in created_ids_true:
                writer.writerow(['', '', '', id, '', ''])
            for id in created_ids_false:
                writer.writerow(['', '', '', id, '', ''])
            
            # Escribir datos de errores
            writer.writerow(['Error', '', '', '', len(errors_list), ''])
            for error in errors_list:
                writer.writerow(['', '', '', error['id'], 1, json.dumps(error['error'])])

        print("Archivo CSV generado con éxito.")

generate_report_send_data(file_path_json)

