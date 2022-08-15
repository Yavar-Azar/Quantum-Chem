# -*- coding: utf-8 -*-
"""
INSTRUCTION

1-enter list of your gaussian outputs in this way;

>> list1="1.out  D2.out  D3.out  D4.out  ".split()

2-use listspectra function to find excitation energies and broadening


>> listspectra(list1)

3-use plotspectra to plot UV-vis together in given range

>>plotspectra(list1, 200, 500)

4-use cdspectra for CD calculation similar way

5- use firstpeak to calculate firstpeaks in spectra

firstpeak(list1)

"""

import scipy
#import os
#import sys
import numpy as np
#from itertools import islice
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema



def excitedstates(logfile, excitedata):
    """
    This function reads a gaussian output and writes two columns file 
    containing excitation energies (eV) and oscillator strength 
    
    Keyword arguments:
        
        logfile -- name of gaussian output from TDDFT run
        
        excitedata -- two columns file excitation energies (eV) vs oscillator strength

    
    """
    oscill=[]
    ene=[]
    fn=open(logfile)
    for line in fn:
        if 'Excited State' in line:
            en=line.split()[4]
            en=float(en)
            osci=line.split()[8]
            osci=float(osci[2:])
            ene.append(en)
            oscill.append(osci)
    statnum=len(ene)
    ene=np.array(ene)
    oscill=np.array(oscill)
    data = np.vstack((ene, oscill))
    fn.close()
    b=[]
    with open(logfile) as f:
        for line in f:
            if "R(length)" in line:
                for i in range(statnum):
                    a=next(f)
                    aa=a.strip().split()
                    aaa=float(aa[4])
                    b.append(aaa)
                rotat =np.array(b)
    datarot=np.vstack((data, rotat)).T
    np.savetxt(excitedata,datarot, fmt="%8.4f %8.4f %8.4f")
    f.close()
    
        
            
                                
def broadoscill(fname, broadened):
    
    """
    this function reads file containing energy (eV) and oscillator strngth
    and use a special  broadening on it
    
    
    Keyword arguments:
        fname -- name of file containg energies and oscillator strengths
        
        broadened -- array of broadened data
        
    """
    fw=0.15
    eneoscill=np.loadtxt(fname)
    ene=eneoscill[:,0]
#   oscill=eneoscill[:,1]
    nstate=len(ene)
    convdata=np.zeros((1000,2))
    spect=np.zeros((1000,2))
    convdata[:,0]=np.linspace(1,10.99,1000)
    for i in range(nstate):
        for j in range(1000):
            convdata[j,1]=convdata[j,1]+(2.175e8/(fw*8100))*eneoscill[i,1]*np.exp(-2.773*((j*0.01-eneoscill[i,0]+1)/fw)**2)
    spect[:,0]=1240/convdata[:,0]
    spect[:,1]=convdata[:,1]
    np.savetxt(broadened,spect , fmt="%8.2f %8.2f")
    
    
    
def cdspectra(fname, cdspectra):
    
    """
    This function reads file containing energy and R srengths and convolve values
    in a CDSPECREA
    
    Keyword arguments:
        
        fname -- name of file contating energy and R values
        
        cdspect -- name of file cd spectra data
        
    """
    
    fw=0.15
    enerot=np.loadtxt(fname)
    ene=enerot[:,0]
#   oscill=eneoscill[:,1]
    nstate=len(ene)
    convdata=np.zeros((1000,2))
    cdspect=np.zeros((1000,2))
    convdata[:,0]=np.linspace(1,10.99,1000) 
    for i in range(nstate):
        for j in range(1000):
            convdata[j,1]=convdata[j,1]+(enerot[i,0]/((22.97)*1.77245385*fw))*enerot[i,2]*np.exp(-1*(((j*0.01-enerot[i,0]+1)/fw)**2))
    cdspect[:,0]=1240/convdata[:,0]
    cdspect[:,1]=convdata[:,1]
    np.savetxt(cdspectra,cdspect , fmt="%8.2f %8.2f")
       


def listspectra(loglist):
    """ 
    reads list of gaussian files as input and writes  all UVVIS and CDspectra
    with same label in datfiles  
    """
    mainlist=[]
    for log in loglist:
        label=str(log.split(".")[0])
        excitedstates(log, label+".dat")
        broadoscill(label+".dat", label+".UV")
        cdspectra(label+".dat",label+".CD")
        mainlist.append(label)
   
    


def plotspectra(loglist,xmin,xmax):
    fig, ax1 = plt.subplots()
    xmin=int(xmin)
    xmax=int(xmax)
#    output=raw_input("please enter output name  :  ")

    colorlist=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']
    ax2 = ax1.twinx()
    ymax=0.0
    j=0
    for log in loglist:
        label=str(log.split(".")[0])
        data=np.loadtxt(label+".UV")
        #    col=raw_input("enter a color     :   "   )
#    alpha=float(input("enter alpha:  "))
#    labe=raw_input("and its label in legend  :   ")
#    data=np.loadtxt(f,usecols=(0,1))
#    shift=float(input("shift in energy  :   "))
        x=data[:,0]
        y=data[:,1]
        oscildata= np.loadtxt(label+".dat")
        x2=1240/oscildata[:,0]
        y2=oscildata[:,1]
        yfilt=y[(x > xmin) & (x > xmin)]
        temp=np.max(yfilt)*1.1
        ymax=max(temp, ymax)
        #    z=data[:,2]
        ax1.plot(x,y,'-' ,  lw=4-j*0.2, color=colorlist[j], label=label)
        ax2.bar(x2, y2, width=0.5)
        j=j+1
        ax1.set_xlim(xmin,xmax)
#        ax1.set_ylim(0,6000)
#    i=0 

        
        
#    z=data[:,2]

    ax1.set_ylim(0,ymax)
    ax1.set_xlabel('$\mathrm{\lambda}$/nm ', fontsize = 20)
    ax1.set_ylabel('$\mathrm{\epsilon /cm^{-1}M^{-1}}$', fontsize = 20)
    ax2.set_ylabel('Oscillator Strength', fontsize = 20)
    ax2.set_ylim(0,0.4)

    #ax1.xticks(fontsize = 20)
    ax1.tick_params(labelsize=16)
    ax2.tick_params(labelsize=16)
    

    ax1.legend(loc='upper right', fontsize =20)
#ax1.tick.label.set_fontsize(24)

    plt.gcf().subplots_adjust(bottom=0.15,left=0.1)
    fig.set_size_inches(12,6)
    fig.savefig(loglist[1][0]+"UV.png", dpi=300)
    plt.show() 
    
    
def plotcd(loglist,xmin,xmax):
    fig,ax = plt.subplots()
    xmin=int(xmin)
    xmax=int(xmax)
#    output=raw_input("please enter output name  :  ")

    colorlist=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']    #ax2 = ax1.twinx()
    j=0
    for log in loglist:
        label=str(log.split(".")[0])
        data=np.loadtxt(label+".CD")
        #    col=raw_input("enter a color     :   "   )
#    alpha=float(input("enter alpha:  "))
#    labe=raw_input("and its label in legend  :   ")
#    data=np.loadtxt(f,usecols=(0,1))
#    shift=float(input("shift in energy  :   "))
        x=data[:,0]
        y=data[:,1]
        #    z=data[:,2]
        ax.plot(x,y,'-' , lw=4-0.3*j,alpha=0.7, color=colorlist[j], label=label)
        j=j+1
        ax.set_xlim(xmin,xmax)
        #ax1.set_ylim(0,6000)
    
    ax.set_xlabel('$\mathrm{\lambda}$/nm ', fontsize = 18)
    ax.set_ylabel('$\mathrm{\Delta \epsilon /cm^{-1}M^{-1}}$', fontsize = 18)
    #ax1.xticks(fontsize = 20)
    ax.tick_params(labelsize=16)
    plt.ylim(-50,50)
    ax.legend(loc='upper right', fontsize =20)
#ax1.tick.label.set_fontsize(24)
    plt.gcf().subplots_adjust(bottom=0.15,left=0.1)
    fig.set_size_inches(12,6)
    fig.savefig(loglist[1][0]+"CD.png", dpi=300)
    plt.show() 
    

        
def secder(UVspect):
    data00=np.loadtxt(UVspect)
    # HERE we consider wavelengths higher than 220, CHANGE IT!!!
    data01=data00[data00[:,0] > 220]
    # Here we filter values smaller than 0.01
    data02=data01[data01[:,1] > 0.01]
    data02=np.flip(data02,0)
    x=data02[:,0]
    y=data02[:,1]
    leng=len(x)
    z=np.zeros((leng))
    for i in range(2,leng-2):
        h=x[i]-x[i-1]
        z[i]=(1/12.0)*(-y[i+2]-y[i-2]+16*y[i-1]+16*y[i+1]-30*y[i])/h**2
    newx=x[2:leng-2]
    zz=z[2:leng-2]
    ## Here we smooth the 2nd derivative with SAVGOL FILTER
    smothed2d=scipy.signal.savgol_filter(zz, 19, 5)
    g=np.vstack((newx,smothed2d)).T
    np.savetxt(str(UVspect)+"_2nder",g, fmt="%8.4f")
    mini = argrelextrema(smothed2d, np.less)
    maxi = argrelextrema(smothed2d, np.greater)
    minizz=newx[mini]
    maxizz=newx[maxi]
    minizz=np.sort(minizz)
    maxizz=np.sort(maxizz)
    exterspect=np.interp(minizz,x,y)
    extdata=np.vstack((minizz, exterspect)).T
    np.savetxt(str(UVspect)+"_exterm",extdata, fmt="%8.4f")
    
    
    

def extract_peaks(loglist, criteria):
    char=loglist[0][0]
    myfile = open(char+"peaks2d.txt", 'w')
    for log in loglist:
        secder(log)
        data=np.loadtxt(log+"_exterm")
        if data.ndim == 1:
            data00=np.reshape(data,(1,2))
        else:
            data00=data[data[:,1] > criteria]
        peak="%8.2f"%data00[-1,0]
        peakval="%8.2f"%data00[-1,1]
        myfile.write(log+peak+ peakval + "\n")
    myfile.close()
        
             
#filelist=input("enter list of g09 log files with space:    ").split()
#lrange=input("enter a range for wavelengths in nm for example 300 800 :").split()
#lmin=float(lrange[0])
#lmax=float(lrange[1])
#listspectra(filelist)
#plotspectra(filelist, lmin, lmax)
