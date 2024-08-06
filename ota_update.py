import requests
import time
import pywifi
from pywifi import const

URL = 'http://192.168.4.1/upload' #your ESP32 server URL for OTA bin upload
BIN_FILE_PATH = r"full_path_to_your_bin_file.bin" #full path to your bin file , not relative path
OTA_AP_SSID = "ESP_OTA" #ESP32 AP SSID
OTA_AP_PASSWORD = None #ESP32 AP password

def connect_to_open_wifi(ssid, password=None):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    original_profile = None
    if iface.status() == const.IFACE_CONNECTED:
        original_profile = iface.network_profiles()

    # Disconnect from any connected network
    iface.disconnect()
    time.sleep(1)
    assert iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN

    if password:
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  
        profile.cipher = const.CIPHER_TYPE_CCMP  # Encryption Algorithm
        profile.key = password
    else:
        profile.akm.append(const.AKM_TYPE_NONE)  
        profile.cipher = const.CIPHER_TYPE_NONE 

    
    # Add the new profile without removing existing ones
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)

    status_update_count = 0
    while (iface.status() != const.IFACE_CONNECTED):
        print(f"connecting to to {ssid}")
        time.sleep(1)
        status_update_count +=1
        if(status_update_count % 5 == 0):
            iface.connect(tmp_profile)
    print(f"Connected to {ssid}")
    return [iface, original_profile]

def connect_to_previous_wifi(wifi_profile):
    iface = wifi_profile[0]
    original_profile = wifi_profile[1]
    if original_profile:
        iface.disconnect()
        time.sleep(1)
        iface.connect(original_profile[0])
        while iface.status() != const.IFACE_CONNECTED:
            print("Reconnecting to the original network")
            time.sleep(1)
        print("Reconnected to the original network")
    else:
        print("No previous network to reconnect to")

        
if __name__ == "__main__":
    wifi_profile = connect_to_open_wifi(OTA_AP_SSID, OTA_AP_PASSWORD)
    files = {'file': open(BIN_FILE_PATH, 'rb')}
    headers = {'Content-Type': 'application/octet-stream'}
    timeout = (10, 15)  # (connect timeout, response timeout) Increase if needed
    try:
        requests.post(URL, files=files, headers=headers, timeout=timeout)
        print('Response Status Code:', response.status_code)
        print('Response Content:', response.content)
    except:
        print("OTA Succeeded") #while using async ESP32 server sometimes the ESP32 get restarted before receiving a response
    connect_to_previous_wifi(wifi_profile)
    
