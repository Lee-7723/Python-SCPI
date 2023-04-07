import pyvisa           #官方文档 https://pyvisa.readthedocs.io/
import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg') #设置matplotlib后端，默认使用的agg在plt.show()时不显示图像
import matplotlib.pyplot as plt

visa_address = 'TCPIP0::192.168.1.100::inst0::INSTR'
rm = pyvisa.ResourceManager()
scope = rm.open_resource(visa_address)
print(scope.query('*IDN?'))

scope.write('*RST')             #reset
scope.write('Trigger:A:edge:source ch3')    #设置trigger
scope.write('ch3:termination 50')
scope.write('display:global:ch3:state 1;:display:global:ch1:state 0;:display:global:ch2:state 0;:display:global:ch4:state 0')
scope.write('AUTOSET EXECUTE')  #autoset
scope.write('acquire:state 1')  #设置为运行状态
while not scope.query('trigger:state?') == 'TRIGGER\n': #等待autoset过程
    time.sleep(0.05)
#time.sleep(3)

scope.write('measurement:meas3:type pk2pk') #添加测量项名为MEAS3 峰峰值
scope.write('measurement:meas3:source CH3') #设置信号源 CH3
scope.query('measurement:meas3:value?')     #查询MEAS3的值

scope.write('data:source ch3')  #设置数据来源 ch3

tscale = float(scope.query('wfmoutpre:xincr?'))
tstart = float(scope.query('wfmoutpre:xzero?'))
vscale = float(scope.query('wfmoutpre:ymult?'))
voff = float(scope.query('wfmoutpre:yzero?'))
vpos = float(scope.query('wfmoutpre:yoff?'))

r = int(scope.query('*esr?'))   #don't know if these 3 lines are necessary, put here just in case

bin_wave = scope.query_binary_values('curve?',datatype='h', container=np.array) #获取曲线并存为数组
record = len(bin_wave)
total_time = tscale * record
tstop = tstart +total_time
scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)    #创建时间轴数

unscaled_wave = np.array(bin_wave, dtype='double')
scaled_wave = (unscaled_wave-vpos)*vscale + voff

display = plt.plot(scaled_time, scaled_wave, color='#F00', linewidth=1)#, figure=plt.figure(facecolor='#000'))
display = plt.title('channel 3')
display = plt.xlabel('time(s)')
display = plt.ylabel('voltage(V)')#
display = plt.grid(True, color='#bbb', linestyle='--')
#display = plt.figure(facecolor='#000')
display = plt.minorticks_on()
display = plt.pause(1)
display = plt.show()

scope.close()
rm.close()

