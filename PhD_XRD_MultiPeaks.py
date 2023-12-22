import math,scipy,pylab
import glob,os
import matplotlib.pyplot as plt
import re , operator
import time
from lmfit.models import LorentzianModel, Model, ExponentialModel
from numpy import loadtxt
from tqdm import tqdm
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from scipy import signal


## Material variables

G= 3E6
Ms= 800
Ha= 0
dH0 = 0  #dH[0]
alpha=0.007
erro=1



## Program variables 

peakmag=[]
fwhmmag=[]
dH=[]
dHa=[]
field=[]
fieldsmag=[]
name1=[]
modsup = LorentzianModel()
zeta=[]
paramos=[]


## Opening files and getting field values from filenames

names=glob.glob("*.dat")

arr = [re.split(r'(\d+)', s) for s in names]
arr.sort(key = lambda x: int(x[1]))

for x in arr:
    field.append(int(x[-2]))
    
## Fitting each graphic to a lorentzian

def Lorexponential(x, simetricL, asymetricL, center, sigma, C):
    return simetricL*(sigma**2/((x-center)**2+sigma**2))+asymetricL*((sigma*(x-center))/((x-center)**2+sigma**2))+C
    



def make_model(num):
    pref = "f{0}_".format(num)
    
    model = Model(Lorexponential, prefix = pref)
    
    model.set_param_hint(pref+'simetricL', value = 0.01 ) 
    model.set_param_hint(pref+'asymetricL', value = 0.01 ) 
    model.set_param_hint(pref+'center', value = paramos[num]['center'] )
    model.set_param_hint(pref+'sigma', value = paramos[num]['sigma']) 
    model.set_param_hint(pref+'C', value = 0.001 ) 
    
    return model

nn=0

for files in names:
    #print(files)
    
    paramos=[]
    data = loadtxt(files)
    x = data[:, 0]
    y = data[:, 1]
    #y = -y
    #y[scipy.where(y<0)]=0
    
    
    
    
    
    ## find peaks and determine number of peaks
    peakind = signal.find_peaks(y , width=3, height=200, prominence=150)
    print(peakind[0])
    wps = x[peakind[0]]


##____   Code to review peaks finder___    

    '''
    plt.figure()
    plt.plot(y)
    plt.plot(peakind[0],y[peakind[0]], 'ro')
    plt.show()
    '''

    
    for pp in range(len(peakind[0])):
        
        larguraajuste = 2
        
        ypeak = y[peakind[0][pp]-larguraajuste:peakind[0][pp]+larguraajuste]
        xpeak = x[peakind[0][pp]-larguraajuste:peakind[0][pp]+larguraajuste]
        
        paramos.append(modsup.guess(ypeak,x=xpeak))
    
    mod = None
    for i in range(len(peakind[0])):
        this_mod = make_model(i)
        if mod is None:
            mod = this_mod
        else:
            mod = mod + this_mod    
        
    outy=mod.fit(y , x=x)
    #print(outy.fit_report())    
    
    for ind in range(len(peakind[0])):
        try:
            peakmag[ind].append(outy.best_values['f'+str(ind)+'_center'])
            fwhmmag[ind].append(outy.best_values['f'+str(ind)+'_sigma'])
            fieldsmag[ind].append(field[nn])
        except:
            peakmag.append([])
            fwhmmag.append([])
            fieldsmag.append([])
            peakmag[ind].append(outy.best_values['f'+str(ind)+'_center'])
            fwhmmag[ind].append(2*outy.best_values['f'+str(ind)+'_sigma'])
            fieldsmag[ind].append(field[nn])
    
    nn+=1
    


## Code to see quality of fits

    #plt.figure()
    plt.plot(x,y)  
    yy=outy.best_fit
    plt.plot(x,yy)
    plt.show()
