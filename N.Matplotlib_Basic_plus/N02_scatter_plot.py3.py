'''
atplotlib Basic_Lv2: 2. Scatter Plot
: Check settings of scatter plots

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

###--- Synthesizing data to be plotted ---###
xx = np.arange(5)+0.5
yy = [1.5,0.5,3,1.25,4.3]
sz = np.arange(5)*30+10
cc = yy

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(7,6)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.05,
                    hspace=0.3,wspace=0.2)  ### Margins, etc.

##-- Title for the page --##
suptit = "Scatter Plot Examples"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')


### Pick colors from pre-defined colormap; https://matplotlib.org/stable/tutorials/colors/colormaps.html
#cmap= mpl.colormaps['magma']

panel_names= ['(X, Y) only','(X, Y) + Marker Size', '(X, Y) + Markersize + Colors']
prop_settings= [dict(), dict(s=sz,marker='^'), dict(s=sz,marker='^',c=yy,vmin=0,vmax=5,cmap='magma')]
nrow, ncol= 2,2
for i,(tit,props) in enumerate(zip(panel_names,prop_settings)):
    ##-- Set up an axes --##
    ax1 = fig.add_subplot(nrow,ncol,i+1)   # (# of rows, # of columns, indicater from 1)

    ##-- Plot on an axes --##
    pic1= ax1.scatter(xx,yy,**props)

    ax1.set_title('({}) {}'.format(abc[i],tit),ha='left',x=0.,fontsize=12)
    ax1.set_xlim([0,5])
    ax1.set_ylim([0,5])

    if 'cmap' in props.keys():
        plt.colorbar(pic1)

##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N02_scatter_plot_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
