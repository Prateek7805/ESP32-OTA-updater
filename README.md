# ESP32-OTA-updater
### Light weight OTA updater for updating ESP32 bin files 
### Assumptions
* ESP32 is in AP mode with fixed ssid name
* ESP32 OTA is configured/programmed as an HTTP updater  

### Dependencies
* requests
* pywifi  
* time
  
ESP32 OTA (Over the Air) updates in ESP_AP mode require connecting wifi to ESP32 AP, opening the browser, accessing the OTA url and then updating the file. While this can be very useful and simple for infrequent updates, testing and frequent code changes may require reconnecting between home and ESP AP connection repeatedly.  

ESP32-OTA-updater performs the sequence of steps in the same sequence:
1) Connects to the ESP-AP (waits for connection establishment and attempts to connect every 5 seconds)
2) Sends the OTA request with the bin file as application/octet-stream
3) Connects to the previous wifi network (if any).
