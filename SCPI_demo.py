import pyvisa   #官方文档 https://pyvisa.readthedocs.io/
#N6700C电源的编程文档 https://www.keysight.com/us/en/assets/9018-03617/programming-guides/9018-03617.pdf

rm = pyvisa.ResourceManager()
rm.list_resources() #此处应列出已连接的设备，后面需要根据此处列出的设备端口写具体代码
inst = rm.open_resource('USB0::0x2A8D::0x0002::MY56013232::0::INSTR')
inst.write(':Voltage 9,(@1);:Current 1,(@1);:output:state on,(@1)') #SCPI语句，设置Channel1电压为9v，状态为开启
out = inst.query(':Measure:Voltage? (@1);:Measure:Current? (@1); :Output:State? (@1)')#读取Ch1的电压电流值和工作状态
print(out)  #输出形式为一串字符串，转换为数据处理需要用python进行字符串处理

volt = float(inst.query(':Measure:Voltage? (@1);'))
curr = float(inst.query(':Measure:Current? (@1);'))
print('volt='+str(volt)+'\n'+'current='+str(curr))
print('power='+str(volt*curr))
