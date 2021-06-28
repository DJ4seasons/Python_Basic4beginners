'''
Matplotlib Basic(6)
: Apply various decorating skills of M03 to multi-panels
: Tune some decoratoins adjusting to multi-panel environment

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_subplot
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html
https://matplotlib.org/stable/gallery/ticks_and_spines/tick-locators.html
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

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

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.05,
                    #hspace=0.6,wspace=0.5)
                    hspace=0.3,wspace=0.2)  ### Margins, etc.
'''
wspace: float, optional
    The width of the padding between subplots, as a fraction of the average Axes width.
hspace: float, optional
    The height of the padding between subplots, as a fraction of the average Axes height.
'''

##-- Title for the page --##
suptit="Multi-Panel Setting with Deco1"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

nrow, ncol= 3,4
for i in range(nrow*ncol):
    ##-- Set up an axes --##
    ax1 = fig.add_subplot(nrow,ncol,i+1)   # (# of rows, # of columns, indicater from 1)

    ##-- Plot on an axes --##
    ax1.plot(x,y)

    ##-- Title for each panel --##
    subtit='({}) Panel#{}'.format(abc[i],i+1)
    plot_common(ax1,subtit)


##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"M06_multi_panel_wDeco1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
