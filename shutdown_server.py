import requests
# Send a request to the Flask server to shut down
response = requests.post('http://localhost:3000/shutdown')
