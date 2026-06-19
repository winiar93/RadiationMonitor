import network
import time

WIFI_SSID = "xxxx"
WIFI_PASSWORD = "xxx"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connected with WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        start = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), start) > 15000:
                return None
            time.sleep_ms(500)

    print("Connected. IP:", wlan.ifconfig()[0])
    return wlan
