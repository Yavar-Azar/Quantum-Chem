
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:11:42 2017

@author: yavar-16
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.colors as col




# read the atoms in each group from file or user


# read the atoms in each group from file or user



fig = plt.figure()

#  This function checks existance of input    
def get_fname(prompt):
    while True:
        fn = input(prompt)
        if os.path.exists(fn): return fn
        print("The file you selected does not exist, please try again")
#######################################################
        
        
checkf=get_fname("enter name of gaussian check file:   ")
listfile=get_fname("enter name of group list:   ")


with open(checkf) as fin:
    out=os.path.splitext(checkf)[0]+'.txt'
    head=[next(fin) for x in range(15)]
fin.close()

 
    
    
#extract number of atoms from FChk file
a=filter(lambda x:'Number of atoms' in x, head)
a=list(map(lambda x:x.strip(),a))
nat=str(a).split()[4]
natom=int(nat.replace("']",""))
    
#extract number of electrons
    
a=filter(lambda x:'Number of electrons' in x, head)
a=list(map(lambda x:x.strip(),a))
nelec=str(a).split()[4]
nelec=int(nelec.replace("']",""))
    
if (nelec % 2 == 0):
    print("This is Closed shell system, anything  is ok")#even 
else:
    print('''WARNING........................
    I am Sorry, this is open shell system, 
    RUNNNN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ''')
    
HOMO=nelec/2

#HOMO=int(raw_input("enter HOMO level number:   "))
delta=int(input("enter delta number:   "))
#natom=int(raw_input("enter atom number:   "))




with open(listfile, "r") as f:
    gname = []
    gnumbs=[]
    for line in f:
        gname.append(line.split()[0])
        tmpn=line.split(' ', 1)[1]
        tmpn=tmpn.split()
        gnumbs.append(tmpn)        
f.close()   
ngroups=len(gname) 



a=int(HOMO-delta)
b=int(HOMO+delta+1)
contrib=np.zeros((ngroups,b-a+1))
i=0
#level=167
tmp01=np.zeros((natom,1))
for level in range(a,b+1):
    tmp= open('temp','w')
    tmp.write(checkf+'\n')
    tmp.write('8\n')
    tmp.write('3\n')
    tmp.write(str(level))
    tmp.close()
    cmd=str("Multiwfn < temp  > temp.out")
    os.system(cmd)
    open('compos.txt','w').writelines([ line for line in open('temp.out') if 'Atom' in line and ' : ' in line])
    with open('compos.txt', 'r') as infile:
        with open("compos0.txt", 'w') as outfile:
            data = infile.read()
            data = data.replace(")", " ")
            data = data.replace("(", " ")
            data = data.replace("%", " ")
            data = data.replace(":", " ")
            data = data.replace("Atom", "")
            outfile.write(data)   
#   cmd1=str("cat compos.txt | sed 's/)/  /g'  | sed 's/(/  /g' | sed 's/%/ /g' | sed 's/:/  /g' | sed 's/Atom/ /g' > compos0.txt" )
    #os.system(cmd1)
    composit=[x.split()[2] for x in open("compos0.txt").readlines()]
    temp000=np.array(composit,dtype=float).reshape((natom,1))
    tmp01 = np.hstack((tmp01,temp000))
    for k in range(ngroups):
        sum0=0.0
        numbk=np.array(gnumbs[k],dtype=int)
        for l in numbk:
            sum0=sum0+temp000[l-1,0]
        contrib[k,i]=sum0
    i=i+1
    print("calculations for  ", level, "-th orbital finished")
    
# Change th list style!!!!!!!!!!!!!!!!!!!!1
sum1=np.zeros(2*delta+2)
collist=[ "#833177", "#4F758B", "#008C95", "#94B7BB", "#EADA24" , "#5d2e8c", "#3A3939", "#64A70B", "#910048", "#06d6a0", "#505759", "#b7b7b7", "#ff5e5b", "#00b2e2", "#ccff66", "#5d2e8c" ]
rsccolors= ['#4F758B','#EADA24','#94B7BB','#D1CCBD','#833177','#C964CF','#008C95','#A3C7D2','#BE4D00','#F0B323','#64A70B','#CEDC00','#006BA6','#5BC2E7', '#DAAA00', '#910048','#E31C79','#505759']
fig=plt.plot()

xindex=[]
for i in range(delta):
    t=delta-i
    tt='H-'+str(t)
    xindex.append(tt)
xindex.append('H')
xindex.append('L')
for i in range(delta):
    tt='L+'+str(i+1)
    xindex.append(tt)



ind = np.arange(2*delta+2)
for m in range(ngroups):
    y=contrib[m,]
    plt.bar(ind,y,  width=0.5,  bottom= sum1, color=rsccolors[m],  ec="none", align='center',label=gname[m])
    sum1=sum1+y
ymax=1.05*np.amax(sum1)
plt.xticks(ind, xindex, rotation='vertical',fontsize =14)
plt.yticks(fontsize =14)
#ax.tick_params(axis=u'both', which=u'both',length=0)

plt.xlim(-1,2*delta+2)
plt.ylim(0,ymax)
sec_legend = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=6, mode="expand", borderaxespad=0, fontsize =10)
plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig("test.pdf", dpi=300)
plt.savefig("test.png", dpi=300)

plt.show()