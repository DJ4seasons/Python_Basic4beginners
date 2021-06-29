'''
atplotlib Basic_Lv2: 3. Bar Plot
: Check settings of scatter plots

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html
'''

import numpy as np
import matplotlib.pyplot as plt


###--- Synthesizing data to be plotted ---###
yy = np.array([1.5,-0.5,3,-1.25,4.3])

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(7,6)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.05,
                    hspace=0.3,wspace=0.2)  ### Margins, etc.

##-- Title for the page --##
suptit = "Bar Plot Examples"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

panel_names= ['Defalut','width=0.4', 'align="edge"', 'Different Colors']
prop_settings= [dict(), dict(width=0.4), dict(align='edge'),dict()]

xloc= np.arange(len(yy))  # Need to specify bar location on x-axis

nrow, ncol= 2,2
for i,(tit,props) in enumerate(zip(panel_names,prop_settings)):
    ##-- Set up an axes --##
    ax1 = fig.add_subplot(nrow,ncol,i+1)   # (# of rows, # of columns, indicater from 1)

    ##-- Plot on an axes --##
    if i<3:
        pic1= ax1.bar(xloc,yy,**props)
    else:
        pos_idx= yy>=0
        pic1= ax1.bar(xloc[pos_idx],yy[pos_idx],color='r',**props)
        pic2= ax1.bar(xloc[~pos_idx],yy[~pos_idx],color='b',**props)

    ax1.set_title('({}) {}'.format(abc[i],tit),ha='left',x=0.,fontsize=12)
    ax1.axhline(y=0,c='k',lw=0.8)
    ax1.axvline(x=2,c='0.6',lw=1.5,ls='--')

##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N03_bar_plot_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
