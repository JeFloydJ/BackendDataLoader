import csv

def count_records(file_path):
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            return sum(1 for row in reader)
    except FileNotFoundError as e:
        return str(e)

# Uso del método
file_path = 'Veevart Contacts Report test_output.csv'
print(f'El número de registros en el archivo es: {count_records(file_path)}')
