'''
Matplotlib Basic(5)
: Produce multi-panels using fig.add_axes()

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_subplot
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html
'''

import numpy as np
import matplotlib.pyplot as plt

###--- Synthesizing data to be plotted ---###
x = np.arange(5)
y = x**2

#for x1,y1 in zip(x,y):
#    print(x1,y1)
###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(8.5,6)    # Physical page size in inches, (lx,ly)

##-- Title for the page --##
suptit="Multi-Panel Setting with fig.add_axes()"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

##-- Subplot Setting --##
nrow, ncol= 3,4

left,right,top,bottom = 0.05,0.95,0.925,0.05
npnx,gapx= ncol,0.05
npny,gapy= nrow,0.08
lpnx= (right-left-(npnx-1)*gapx)/npnx
lpny= (top-bottom-(npny-1)*gapy)/npny

ix=left; iy=top
for i in range(nrow*ncol):
    ##-- Set up an axis --##
    ax1 = fig.add_axes([ix,iy-lpny,lpnx,lpny])  # [left,bottom,width,height]

    ##-- Plot on an axis --##
    ax1.plot(x,y)
    ax1.set_title('({}) Panel#{:d}'.format(abc[i],i+1))

    ##-- Update panel location
    ix=ix+lpnx+gapx
    if ix > right:
       ix=left
       iy=iy-lpny-gapy


##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"M05_multi_panel2.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
