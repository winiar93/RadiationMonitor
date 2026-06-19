from machine import Pin
from time import sleep_ms
from machine import disable_irq, enable_irq
import json
import urequests as requests
from wifi_connection import connect_wifi

GPIO_PIN = 26
CONVERSION_FACTOR = 151
count = 0
API_URL = "http://[IP]:5000/api/readings"

def isr(pin):
    global count
    count += 1
    
def send_measurement(cpm, usvh):
    payload = json.dumps({
        "cpm": cpm,
        "usvh": usvh,
    })
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, headers=headers, data=payload)
        print("API response:", response.status_code)
        response.close()
    except Exception as e:
        print("Error while sending data to API:", e)

pin = Pin(GPIO_PIN, Pin.IN)
pin.irq(trigger=Pin.IRQ_RISING, handler=isr)

connect_wifi()
print("Detecting signals on GPIO", GPIO_PIN, "...")

while True:
    state = disable_irq()
    count = 0
    enable_irq(state)
    sleep_ms(60000)
    cpm = count 
    usvh = round(cpm / CONVERSION_FACTOR, 3)
    print(f"Radiation measurement: {cpm} CPM | {usvh} µSv/h")
    send_measurement(cpm, usvh)

    
