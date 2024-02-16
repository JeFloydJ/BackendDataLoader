import csv

def eliminar_columnas(csv_input, headers_eliminar, csv_output):
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

# Uso de la función
headers_eliminar = ["Lookup ID", "QUERYRECID"]
eliminar_columnas('output.csv', headers_eliminar, 'output.csv')