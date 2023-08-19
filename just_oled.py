import time
def avg(li):
    eq=0
    if li[-1]>0.4 :
        eq=round(sum(li)/len(li),1)
    return eq

def display(oled,ch1,avg1,ch2,avg2,ch3,avg3):
    oled.fill(0)
    oled.fill_rect(0, 0, 32, 64, 1)
    oled.text("CH1:",0,4,0)
    oled.text(str(ch1)+"mA",36,0)
    oled.line(0,20,32,20,0)
    oled.hline(32,20,128,20)
    oled.text("CH2:",0,25,0)
    oled.text(str(ch2)+"mA",36,22)
    oled.line(0,40,32,40,0)
    oled.hline(32,40,128,40)
    oled.text("CH3:",0,46,0)
    oled.text(str(ch3)+"mA",36,42)
    oled.text("AVG:"+str(avg1)+"mA",36,12)
    oled.text("AVG:"+str(avg2)+"mA",36,32)
    oled.text("AVG:"+str(avg3)+"mA",36,52)
    oled.show()


def display_simple(oled,ch1,ch2,ch3):
    oled.fill(0)
    oled.fill_rect(0, 0, 32, 64, 1)
    oled.text("CH1:",0,4,0)
    oled.text(str(ch1)+"mA",36,4)
    oled.line(0,20,32,20,0)
    oled.hline(32,20,128,20)
    oled.text("CH2:",0,25,0)
    oled.text(str(ch2)+"mA",36,26)
    oled.line(0,40,32,40,0)
    oled.hline(32,40,128,40)
    oled.text("CH3:",0,46,0)
    oled.text(str(ch3)+"mA",36,46)
    oled.show()

def just_oled_run(oled,ina):
    avg_list_0=[]
    avg_list_1=[]
    avg_list_2=[]
    t=time.time()
    while True:
        if len(avg_list_0)>=20:
            avg_list_0.pop(0)
            avg_list_1.pop(0)
            avg_list_2.pop(0)
        avg_list_0.append(ina.getI(0))
        avg_list_1.append(ina.getI(1))
        avg_list_2.append(ina.getI(2))
        a1=avg_list_0[-1]
        a2=avg_list_1[-1]
        a3=avg_list_2[-1]
        v1=avg(avg_list_0)
        v2=avg(avg_list_1)
        v3=avg(avg_list_2)
        display(oled,a1,v1,a2,v2,a3,v3)
        time.sleep(0.1)
