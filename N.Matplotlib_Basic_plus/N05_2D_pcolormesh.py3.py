'''
Matplotlib Basic_Lv2: 5. "pcolormesh" for 2D array
: Display 2d array with pcolormesh()

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pcolormesh.html
'''
import numpy as np
import matplotlib.pyplot as plt

###--- Synthesizing data to be plotted ---###
x = y = np.linspace(0,1,6)  # For 5x5 array
X,Y = np.meshgrid(x,y)
Z = np.cos(np.pi/2*X)-np.sin(np.pi/2*Y)
resol= x[1]-x[0]
xp = yp = np.concatenate((x-resol/2,[x[-1]+resol/2,]))
Xp1,Yp1 = np.meshgrid(xp,yp)  # Grid wrapping data points; needed for pcolormesh

x2 = y2 = np.linspace(0,1,11)  # For 10x10 array
X2,Y2 = np.meshgrid(x2,y2)
Z2 = np.cos(np.pi/2*X2)-np.sin(np.pi/2*Y2)
resol= x2[1]-x2[0]
xp2 = yp2 = np.concatenate((x2-resol/2,[x2[-1]+resol/2,]))
Xp2,Yp2 = np.meshgrid(xp2,yp2)  # Grid wrapping data points; needed for pcolormesh

data= [(Xp1,Yp1,Z), (X,Y,Z), (Xp2,Yp2,Z2), (X2,Y2,Z2),]
##<---- Different grid information is needed by shading method!

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(6,6)    # Physical page size in inches, (lx,ly)
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.925,wspace=0.2,hspace=0.3)

##-- Title for the page --##
suptit="Imshow Example"
fig.suptitle(suptit,fontsize=15,y=0.98,va='bottom')  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

panel_names= ['Default',"shading='gouraud'",'Default',"shading='gouraud'",]
prop_settings= [dict(), dict(shading='gouraud'), dict(), dict(shading='gouraud')]


nrow, ncol= 2,2
for i,(XYZ,tit,props) in enumerate(zip(data,panel_names,prop_settings)):
    X,Y,Z= XYZ
    ax1= fig.add_subplot(nrow,ncol,i+1)
    pic1= ax1.pcolormesh(X,Y,Z,**props)
    subtit='({}) {}'.format(abc[i],panel_names[i])
    ax1.set_title(subtit,fontsize=12,x=0.,ha='left')

plt.colorbar(pic1)
##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N05_2D_pcolormesh_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
