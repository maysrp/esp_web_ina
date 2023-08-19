import time,gc
import json,os
from machine import Pin,I2C
import ina3221
import ssd1306



ch=Pin(2,Pin.IN,Pin.PULL_UP)
t=1
while True:
    t+=1
    print(ch.value())
    if not ch.value():
        type_run=2
        del ch
        time.sleep(3)
        ac="WEB"
        print("WEB")
        break
    if t>50:
        type_run=1
        del ch
        print("NO WEB")
        ac="NO WEB"
        break
    time.sleep_ms(100)


i2c=I2C(scl=Pin(0),sda=Pin(2), freq=4000000)
oled=ssd1306.SSD1306_I2C(128,64,i2c)
ina=ina3221.INA3221(i2c,addr=0x40)
#ina=ina3221.INA3221(i2c,addr=0x43)
#OLED
oled.text(ac,0,0)
oled.show()
time.sleep_ms(500)

if type_run==1:
    from just_oled import just_oled_run
    just_oled_run(oled,ina)


#web 联网
import network
from uWeb import uWeb, loadJSON
from just_oled import display_simple

try:
    f=open("config.dat","r")
    config=json.loads(f.read())
    f.close()
except Exception as e:
    config={"name":"","password":""}
    f=open("config.dat","w")
    f.write(json.dumps(config))
    f.close()

if config["name"]:
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(config["name"],config["password"])
    for _ in range(100):
        if sta_if.isconnected():
            print('\nConnected! Network information:', sta_if.ifconfig())
            break
        else:
            print('.', end='')
            time.sleep_ms(100)
    if sta_if.isconnected():
        conn=1
        print(sta_if.ifconfig())
        oled.fill(0)
        oled.text("wifi:"+config["name"],0,0)
        oled.text(sta_if.ifconfig()[0],0,8)
        oled.text("ip:8000/",0,16)
        oled.show()
    else:
        sta_if.disconnect()
        conn=0
        wlan_ap = network.WLAN(network.AP_IF)
        wlan_ap.active(True)
        wlan_ap.config(essid="wani",password="12345678",authmode=network.AUTH_WPA_WPA2_PSK)




def ina_dic(): #电流获取
    global ina
    return {'a_1': ina.getI(0),'a_2': ina.getI(1),'a_3': ina.getI(2)}


server = uWeb("0.0.0.0", 8000)  #init uWeb object




def wifi():
    vars=config
    print(config)
    server.render('wifi.html', variables=vars)

def wifipost():
    print('Payload: ', loadJSON(server.request_body))
    c=loadJSON(server.request_body)
    if c:
        f=open("config.dat","w")
        f.write(json.dumps(c))
        f.close()
    server.render('wifi.html', variables=c)
    
    
def home(): #render HTML page
    vars = ina_dic()
    display_simple(oled,vars["a_1"],vars["a_2"],vars["a_3"])
    server.render('content.html', variables=vars)


def get_ina():
    server.sendJSON(ina_dic())

#configure routes
server.routes(({
    (uWeb.GET, "/"): home,
    (uWeb.GET, "/wifi"): wifi,
    (uWeb.POST, "/wifi"): wifipost,
    (uWeb.GET, "/i"): get_ina,
}))

#start server
server.start()



