'''
Matplotlib Basic_Lv2: 4. "imshow" for 2D array
: Display 2d array with imshow()

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html
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

data= [Z,Z2]

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(5,8.5)    # Physical page size in inches, (lx,ly)
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.94,wspace=0.2,hspace=0.4)

##-- Title for the page --##
suptit="Imshow Example"
fig.suptitle(suptit,fontsize=15,y=1.0)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

panel_names= ['Default','origin="lower"', 'interpolation="bilinear"',
                'extent=[2,5,-1,1]','aspect="auto"']
prop_settings= [dict(), dict(origin='lower'), dict(interpolation='bilinear'),
                dict(extent=[2,5,-1,1]),dict(aspect="auto")]

nrow, ncol= 5,2
for j,Z in enumerate(data):
    for i,(tit,props) in enumerate(zip(panel_names,prop_settings)):

        ax1= fig.add_subplot(nrow,ncol,i*2+j+1)
        pic1= ax1.imshow(Z,**props)
        if j==0:
            subtit='({}) {}'.format(abc[i],panel_names[i])
            ax1.set_title(subtit,fontsize=12)

plt.colorbar(pic1)
##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N04_2D_imshow_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
