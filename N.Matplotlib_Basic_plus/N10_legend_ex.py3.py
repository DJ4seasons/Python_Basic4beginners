'''
Matplotlib Basic_Lv2: 10. Legend examples
: Draw a legend box

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

def plot_common(ax,subtit='',ytlab=True,ytright=False):
    ax.set_title(subtit,fontsize=12,stretch='semi-condensed') #,x=0.,ha='left') #,y=0.9

    ax.set_xlim(-4,4)
    ax.xaxis.set_major_locator(MultipleLocator(2))   # For Major Ticks
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks
    #xt_form=FuncFormatter(lambda x, pos: "{:0.1f}".format(x))
    #ax.xaxis.set_major_formatter(xt_form)

    ax.set_ylim(-1.5,1.5)
    #ax.set_yticks(range(0,17,4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    if not ytlab:
        ax.set_yticklabels('')

    if ytright:
        ax.yaxis.tick_right()

    ax.yaxis.set_ticks_position('both')

    ax.tick_params(axis='both',labelsize=10)
    ax.axhline(y=0.,color='k',linestyle=':',lw=0.7)
    ax.axvline(x=0.,color='k',ls=':',lw=0.7)
    return

###--- Legend options
legend_locs=[
    ['best'     ,0], ['upper right'     ,1], ['upper left'  ,2],
    ['lower left'   ,3], ['lower right'     ,4], ['right'   ,5],
    ['center left'  ,6], ['center right'    ,7], ['lower center'    ,8],
    ['upper center' ,9], ['center'  ,10],
    ]


###--- Synthesizing data to be plotted ---###
x = np.arange(-4,4.1,0.1)
ysin = np.sin(x)
ycos = np.cos(x)

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(10,7.5)    # Physical page size in inches, (lx,ly)

##-- Title for the page --##
suptit="Legend Examples "
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

nrow, ncol= 3,4

left,right,top,bottom = 0.05,0.95,0.925,0.07
gapx,gapy = 0.03,0.09
lpnx= (right-left-(ncol-1)*gapx)/ncol
lpny= (top-bottom-(nrow-1)*gapy)/nrow
ix=left; iy=top
for i in range(nrow*ncol):
    ##-- Set up an axes --##
    ax1 = fig.add_axes([ix,iy-lpny,lpnx,lpny])  # [left,bottom,width,height]

    ##-- Plot on an axes --##
    line1=ax1.plot(x,ysin,label='sin(x)')  # plotting line graph1
    line2=ax1.plot(x,ycos,label='cos(x)')  # plotting line graph2


    ##-- Legend and sub-title --##
    if i<10:
        ax1.legend(loc=legend_locs[i][0],fontsize=9,framealpha=0.7)
        subtit='({}) Loc={}'.format(abc[i],legend_locs[i][0])
    elif i==10:
        subtit='({}) Loc={}, ncol=2'.format(abc[i],legend_locs[9][0])
        ax1.legend(loc=legend_locs[9][0],fontsize=9,framealpha=0.7,ncol=2)
    else:
        subtit='({}) Legend Loc={}'.format(abc[i],legend_locs[2][0])
        ax1.legend(loc=legend_locs[2][0],bbox_to_anchor=(1.05,1.),fontsize=9,borderaxespad=0.) #,framealpha=0.7)


    if i%ncol==0:
        ax1.set_ylabel('Y-axis Label',fontsize=12,rotation=90,labelpad=0)
    elif i%ncol==ncol-1:
        ax1.yaxis.set_label_position('right')
        ax1.set_ylabel('Y-axis Label',fontsize=12,rotation=-90,labelpad=0,va='bottom')
    if i >= ncol*(nrow-1):
        ax1.set_xlabel('X-axis Label',fontsize=12)

    if i%ncol==ncol-1:
        plot_common(ax1,subtit,ytlab=True,ytright=True)
    elif i%ncol!=0:
        plot_common(ax1,subtit,False)
    else:
        plot_common(ax1,subtit)

    ix=ix+lpnx+gapx
    if ix+lpnx > 1.0:
       ix=left
       iy=iy-lpny-gapy

##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N02_legend_ex.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
