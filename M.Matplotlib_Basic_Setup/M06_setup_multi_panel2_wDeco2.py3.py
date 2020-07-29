'''
Matplotlib Basic(6)
: Apply various decorating skills of M02 to multi-panels
: Tune some decoratoins adjusting to multi-panel environment

by Daeho Jin

---
Reference:
https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.add_axes
https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html
https://matplotlib.org/examples/ticks_and_spines/tick-locators.html
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

def plot_common2(ax,subtit='',ytlab=True,ytright=False):
    ax.set_title(subtit,fontsize=12,x=0.,ha='left') #,y=0.9

    ax.set_xlim(-0.5,4.5)
    ax.xaxis.set_major_locator(MultipleLocator(1))   # For Major Ticks
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks
    xt_form=FuncFormatter(lambda x, pos: "{:0.1f}".format(x))
    ax.xaxis.set_major_formatter(xt_form)

    ax.set_ylim(-1,17)
    ax.set_yticks(range(0,17,4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    if not ytlab:
        ax.set_yticklabels('')

    if ytright:
        ax.yaxis.tick_right()

    ax.yaxis.set_ticks_position('both')

    ax.tick_params(axis='both',labelsize=10)
    ax.axhline(y=0.,color='k',linestyle=':')
    ax.axvline(x=0.,color='k',ls=':',lw=0.5)


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
suptit="Multi-Panel Setting"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

nrow, ncol= 3,4

left,right,top,bottom = 0.05,0.95,0.925,0.07
npnx=ncol; gapx=0.03
npny=nrow; gapy=0.09
lpnx= (right-left-(npnx-1)*gapx)/npnx
lpny= (top-bottom-(npny-1)*gapy)/npny

ix=left; iy=top
for i in range(nrow*ncol):
    ##-- Set up an axis --##
    ax1 = fig.add_axes([ix,iy-lpny,lpnx,lpny])  # [left,bottom,width,height]

    ##-- Plot on an axis --##
    ax1.plot(x,y,color='{:.1f}'.format(i/(nrow*ncol)))

    ##-- Title for each panel --##
    subtit='({}) Panel#{}'.format(abc[i],i+1)
    #plot_common2(ax,subtit='',ytlab=True,ytright=False)

    if i==ncol*(nrow-1):  # For the only panel on bottom left corner
        ax1.set_xlabel('X-axis Label',fontsize=12)
        ax1.set_ylabel('Y-axis Label',fontsize=12,rotation=90,labelpad=0)

    if i%ncol==ncol-1:  # Right-most column
        plot_common2(ax1,subtit,ytlab=True,ytright=True)
    elif i%ncol!=0:  # Center columns
        plot_common2(ax1,subtit,False)
    else:  # Left-most column
        plot_common2(ax1,subtit)

    ix=ix+lpnx+gapx
    if ix+lpnx > 1.:
       ix=left
       iy=iy-lpny-gapy


##-- Seeing or Saving Pic --##

#- If want to see on screen -#
#plt.show()

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"M06_multi_panel4.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
