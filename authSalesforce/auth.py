# Import necessary modules
import requests
import webbrowser

# Your Salesforce credentials
client_id = '3MVG9zeKbAVObYjPODek1PYnJW15VxHyhGPUOe1vzfHcg89tL_3Xyj_DCZQql_RL4Gjdnmk7EpfFk4DGDulnz'
redirect_uri = 'http://localhost:8000'
response_type = 'code'

# Salesforce authentication URL
url = f"https://login.salesforce.com/services/oauth2/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}"

# Define the payload and headers (both are empty in this case)
headers = {}
payload = {}

# Send the GET request and get the response
response = requests.request("GET", url, headers=headers, data=payload)

# Return the URL from the response
link = response.url
webbrowser.open(link)