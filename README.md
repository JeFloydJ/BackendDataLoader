# BackendDataLoader

Este proyecto utiliza un servidor local y un script de autenticación para obtener tokens de acceso tanto en altru como en salesforce. Se debe tener en cuenta que:
- hay dos carpetas que tienen el nombre para cada uno, tanto como para salesforce tanto como para altru. Esto quiere decir que si yo quiero autorizar y obtener tokens de acceso para altru, debo ejecutar los proximos pasos en la carpetas authAltru y serverAltru y si se quiere hacer en salesforce se debe hacer lo mismo pero en las carpetas authSalesforce y serverSalesforce

## Requisitos

- Python 3
- Bibliotecas: `requests`

## Instalación

Para instalar las dependencias necesarias, puedes usar pip:

```bash
pip install requests
```

-Biblioteca: `simple-salesforce`
```bash
pip install simple-salesforce
```
## Pasos para ejecutar el proyecto
Ejecutar el servidor: Primero, debes ejecutar el servidor local. Puedes hacer esto ejecutando el siguiente comando en tu terminal:

```bash
python3 server.py
```
Esto iniciará el servidor en el puerto 8000.

## Ejecutar el script de autenticación: 
A continuación, debes ejecutar el script de autenticación. Puedes hacer esto ejecutando el siguiente comando en una nueva terminal:
```bash
python3 auth.py
```
Esto generará un enlace.

## Autorizar la aplicación: 
se abrirán el enlace en tu navegador automaticamente, debes dar autorizar en el link que se abrió.
## Obtener informacion de endpoints: 
Después de autorizar la aplicación, se debe ejecutar el siguiente comando:
```bash
python3 eventGetSearchConstituent.py
```
y este traerá la información del endpoint
