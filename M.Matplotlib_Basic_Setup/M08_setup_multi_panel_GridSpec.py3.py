'''
Matplotlib Basic(8)
: Apply GridSpec for advanced sub-plotting
: Mimic layout of M04

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/tutorials/intermediate/gridspec.html
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
import matplotlib.gridspec as gridspec
"""
Note: From Matplotlib ver 3.3, figure object also has 'add_gridspec' mtehod, which
doesn't require the import of gridspec
"""

def plot_common(ax, subtit=''):
    ax.set_title(subtit,fontsize=12,x=0.,ha='left') #,y=0.9

    ax.set_xlim(-0.5,4.5)
    ax.xaxis.set_major_locator(MultipleLocator(1))   # For Major Ticks
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks
    #xt_form=FuncFormatter(lambda x, pos: "{:0.1f}".format(x))
    #ax.xaxis.set_major_formatter(xt_form)
    ax.xaxis.set_major_formatter("{x:0.1f}")  # Working on ver 3.3+
    ax.set_xlabel('X-axis Label',fontsize=10)

    ax.set_ylim(-1,17)
    ax.set_ylabel('Y-axis Label',fontsize=10,rotation=90,labelpad=2)
    ax.set_yticks(range(0,17,4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_ticks_position('both')


    ax.tick_params(axis='both',labelsize=9)
    ax.axhline(y=0.,color='k',linestyle=':')
    ax.axvline(x=0.,color='k',ls=':',lw=0.5)
    return

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

gs_spec0= dict(left=0.05,right=0.95,top=0.92,bottom=0.5,hspace=0.75,wspace=0.45)
gs_spec1= dict(left=0.05,right=0.95,top=0.3,bottom=0.05)
gs0= fig.add_gridspec(ncols=4,nrows=2,**gs_spec0)  # Matplotlib ver. 3.3+
gs1= fig.add_gridspec(ncols=1,nrows=1,**gs_spec1)  # Matplotlib ver. 3.3+
#gs0= gridspec.GridSpec(ncols=4,nrows=2,**gs_spec0)
#gs1= gridspec.GridSpec(ncols=1,nrows=1,**gs_spec1)

##-- Title for the page --##
suptit="GridSpec Example"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

axes=[]
axes.append(fig.add_subplot(gs0[:,:2]))
axes.append(fig.add_subplot(gs0[:,2:3]))
axes.append(fig.add_subplot(gs0[0,3]))
axes.append(fig.add_subplot(gs0[1,3]))

axes.append(fig.add_subplot(gs1[0]))

for i,ax1 in enumerate(axes):
    ##-- Plot on an axes --##
    ax1.plot(x,y)

    ##-- Title for each panel --##
    subtit='({}) Panel#{}'.format(abc[i],i+1)
    plot_common(ax1,subtit)


##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"M08_multi_panel_wGridSpec.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
