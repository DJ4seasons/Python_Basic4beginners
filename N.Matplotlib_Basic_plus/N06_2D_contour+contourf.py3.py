'''
Matplotlib Basic_Lv2: 6. "contour" and "contourf" for 2D array
: Display 2d array with contour() and contourf()

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contour.html
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contourf.html
https://matplotlib.org/stable/api/contour_api.html#matplotlib.contour.ContourLabeler.clabel
'''
import numpy as np
import matplotlib.pyplot as plt

###--- Synthesizing data to be plotted ---###
x = y = np.linspace(0,1,6)  # For 5x5 array
X,Y = np.meshgrid(x,y)
Z = np.cos(np.pi/2*X)-np.sin(np.pi/2*Y)

x2 = y2 = np.linspace(0,1,11)  # For 10x10 array
X2,Y2 = np.meshgrid(x2,y2)
Z2 = np.cos(np.pi/2*X2)-np.sin(np.pi/2*Y2)

data= [(X,Y,Z), (x2,y2,Z2),]

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(6,10)    # Physical page size in inches, (lx,ly)
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95,wspace=0.25,hspace=0.45)

##-- Title for the page --##
suptit="Contour/Contourf Example"
fig.suptitle(suptit,fontsize=15,y=0.98,va='bottom')  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

## Settings for contour()
panel_names1= ['Default',"Custom Levs+colors=['b','r']",'clabel() Ex.']
prop_settings1= [dict(),dict(levels=[-0.7,-0.3,-0.1,0.1,0.2,0.5],colors=['b','r']),dict()]

## Settings for contourf()
panel_names2= ["Default","levels=100 + contour()"]
prop_settings2= [dict(),dict(levels=100)]


nrow, ncol= 5,2
for j,XYZ in enumerate(data):
    X,Y,Z= XYZ
    pn= j+1
    for i,(tit,props) in enumerate(zip(panel_names1,prop_settings1)):
        ax1= fig.add_subplot(nrow,ncol,pn)
        pic1= ax1.contour(X,Y,Z,**props)
        subtit='({}) {}'.format(abc[pn-1],tit)
        ax1.set_title(subtit,fontsize=12,x=0.,ha='left')
        pn+=2
        if 'clabel' in tit:
            ax1.clabel(pic1,fmt='%.2f')

    for i,(tit,props) in enumerate(zip(panel_names2,prop_settings2)):
        ax2= fig.add_subplot(nrow,ncol,pn)
        pic2= ax2.contourf(X,Y,Z,**props)
        subtit='({}) {}'.format(abc[pn-1],tit)
        ax2.set_title(subtit,fontsize=12,x=0.,ha='left')
        pn+=2
        if 'contour' in tit:
            pic3=ax2.contour(X,Y,Z,levels=5,colors='k',linewidths=2.5,alpha=0.8)
            ax2.clabel(pic3,fmt='%.2f')
#plt.colorbar(pic1)
##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N06_2D_contour+contourf_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
