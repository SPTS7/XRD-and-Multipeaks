import math,scipy,pylab
from scipy.optimize import curve_fit
import numpy as np
import glob,os
import matplotlib.pyplot as plt
import re , operator
import time
from lmfit.models import Model
from numpy import loadtxt
from tqdm import tqdm



n=1
x1=[]
y1=[]
ind=0
theta_0=0.0020
A=0.0065
B=0.0012
t0=145
fmr=2.4995
phi=1
tau=225

pontosatirar=15


## Opening files

names=glob.glob("*.dat")

## Getting data

for files in names:
    if n==1:
        data = loadtxt(files)
        x1  = data[:, 0]
        y1  = data[:, 4]
        n+=1
    else:
        data = loadtxt(files)
        x2  = data[:, 0]
        y2  = data[:, 4]

## calculo para picosegundos e subtração das curvas

time=x1*10**-3

curve=(y1-y2)/2*-1

## tirar os primeiros pontos, antes do salto e os primeiros 10 ps


curve1=curve[pontosatirar:]
time1=time[pontosatirar:]


## fit para a curva 

def demag(t, theta_0 , A, B, t0, fmr, phi, tau):
    return theta_0 + A*np.exp(-t*t0) + B*np.sin(2*math.pi*fmr*t+phi)*np.exp(-t/tau)

DM = Model(demag)

param = DM.make_params() 


param.add('theta_0' , value= theta_0 , min=0.0015, max=0.0025)
param.add('A' , value= A , min=0.0015, max=0.0085)
param.add('B' , value= B , min=0.0008, max=0.0019)
param.add('t0' , value= t0 , min=140, max=160)
param.add('fmr'  , value= fmr )#, min=2.4, max=2.6)
param.add('phi'  , value= phi )#, min=0.5, max=0.7)
param.add('tau'  , value= tau , min=200, max=250)


c=curve1
ti=time1

DMfit = DM.fit(c, params=param , t = ti)
print(DMfit.fit_report())


#popt, pcov = curve_fit(demag, ti, c, bounds=(0,[0.1,0.01,0.01,160,5,1,300]))

## Making a csv to save the results

'''
le=len(ti)
file = open("Results_"+str(names[0])+".csv","w") 

file.write("Time,Curve,Fit"+"\n")

for z in range(pontosatirar):
    line1=str(time[z])+","+str(curve[z])
    file.write(line1 +"\n")


for i in range(le):
    line=str(ti[i])+","+str(c[i])+","+str(DMfit.best_fit[i])
    file.write(line +"\n")
file.close()

file = open("Fit_Values_"+str(names[0])+".csv","w") 
file.write(DMfit.fit_report())
file.close()
'''
## plot
'''
plt.plot(ti,c,'ro')

plt.plot(ti, demag(ti, *popt), 'r-', label='fit: theta_0=%5.3f, A=%5.3f, B=%5.3f , t0=%5.3f, fmr=%5.3f , phi=%5.3f, tau=%5.3f' % tuple(popt))
plt.legend()
'''

DMfit.plot_fit()
plt.xlabel('Time (Ps)')
plt.ylabel('Voltage (mV)')
#plt.savefig('Fit_'+str(names[0])+".png")

plt.show()