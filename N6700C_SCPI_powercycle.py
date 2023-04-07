import pyvisa   #官方文档 https://pyvisa.readthedocs.io/
#N6700C电源的编程文档 https://www.keysight.com/us/en/assets/9018-03617/programming-guides/9018-03617.pdf

import time

loop = 5    #循环次数
on_duration = 1     #上电时长，单位秒
off_duration = 1    #下点时长

rm = pyvisa.ResourceManager()
rm.list_resources() #此处应列出已连接的设备，后面需要根据此处列出的设备端口写具体代码
inst = rm.open_resource('USB0::0x2A8D::0x0002::MY56013232::0::INSTR')
inst.write(':Voltage 9,(@1);:Current 1.5,(@1);') #SCPI语句，设置Channel1电压为9v，状态为开启

for i in range(0,loop):
    inst.write(':output:state on,(@1)')
    time.sleep(on_duration)
    volt = float(inst.query(':Measure:Voltage? (@1);'))
    curr = float(inst.query(':Measure:Current? (@1);'))
    power = volt*curr
    print('power='+str(power))
    inst.write(':output:state off,(@1)')
    time.sleep(off_duration)
else:
    print(str(i+1)+' loops')
