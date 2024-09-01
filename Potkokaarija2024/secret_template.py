# ssid = 'nimi'
# password = 'ssid:n salasana'

# Define a simple class to hold the ssid and password
class WiFiSecret:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

# List of WiFiSecret objects
secrets = [
    WiFiSecret('Network1', 'Password1'),
    WiFiSecret('Network2', 'Password2'),
    WiFiSecret('Network3', 'Password3')
]