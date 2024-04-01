import json
import csv

def json_to_csv(json_file_path, csv_file_path):
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


json_to_csv('Veevart HouseHolds Report test_response.json', 'output.csv')
