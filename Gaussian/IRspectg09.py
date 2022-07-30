#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 15:14:43 2022

@author: yavar
"""

import numpy as np


import matplotlib.pyplot as plt

import cclib


pallete1=["#264653ff", "#2a9d8fff", "#e9c46aff", "#f4a261ff", "#e76f51ff"]
pallete2=["#8ecae6", "#219ebc", "#023047", "#ffb703", "#fb8500"]






def plotfreqgaussian(logfile, sigma=30.0):
    """
    

    Parameters
    ----------
    logfile : string
        gaussian log file.
    sigma : float, optional
        gaussian broadening sigma. The default is 30.

    Returns
    -------
    None.

    """
    
    filename = logfile
    dataname = filename[:-3]+"data"

    data = cclib.io.ccread(filename)
    
    
    
    
    irint = data.vibirs
    
    freqs = data.vibfreqs
    
    
    freqmax=max(freqs)
    
    
    
    freqrange = np.linspace(10, 1.1*freqmax, 1001)
    freqspect =np.zeros_like(freqrange)
    
    
    # gaussian convolution
    
    for i in range(len(irint)):
        freqspect=freqspect+irint[i]*np.exp(-((freqrange-freqs[i])/sigma)**2)
        
        
    freqspect=2*np.sqrt(np.pi/sigma)*freqspect
        
    
    
    freqconvol = np.stack((freqrange, freqspect))

    

### Save convoluted data in a file
    np.savetxt(filename[:4]+"_freq.txt", freqconvol.T, fmt="%10.4f")
    
    plt.figure(figsize=(6,3))
    plt.xlabel("Frequency ($cm^{-1}$)")
    plt.ylabel("IR intensity (arb. unit)")
    
    plt.xlim(0, 3500)
        
    plt.plot(freqrange, freqspect, color=pallete1[0])
    plt.bar(freqs, height=irint, width=10, color=pallete1[1])
    
        
    
    
    plt.savefig(filename[:4]+"_freq.png", dpi=300, bbox_inches='tight')
    
      
    return



def orbitenergy(logfile, wind=2.0):
       
    
    filename = logfile
    data = cclib.io.ccread(filename)
    
    ### !!!  there are diff between nelectron and alpha beta electron2
    nelect = []
    with open(logfile, 'r') as f:
        for line in f.readlines():
            if 'alpha electrons' in line:
                nelect.append(int(line.split()[0]))



    moenergies=data.moenergies[0]
    
    
    homo=data.moenergies[0][133]
    lumo=data.moenergies[0][134]
    
    gap=lumo-homo
    
    ocuppied = moenergies[moenergies < lumo]
    unocuppied = moenergies[moenergies > homo]

    plt.figure(figsize=(1,2.5))
    plt.xticks([])
    
    plt.ylabel("Energy (eV)")
    plt.ylim(np.floor(homo-wind), np.ceil(lumo+wind))
    
    plt.barh(ocuppied, height=0.05, width=1, color=pallete1[0])
    plt.barh(unocuppied, height=0.05, width=1, color=pallete1[4])
    
    
    return 
    
    
    
    
    







