'''
Matplotlib Basic_Lv2: 1. Line Plot
: Change properties of line graph

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

def plot_common2(ax,subtit='',ytlab=True,ytright=False):
    ax.set_title(subtit,fontsize=12,x=0.,ha='left') #,y=0.9

    ax.set_xlim(-0.5,4.5)
    ax.xaxis.set_major_locator(MultipleLocator(1))   # For Major Ticks
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks
    #xt_form=FuncFormatter(lambda x, pos: "{:0.1f}".format(x))
    #ax.xaxis.set_major_formatter(xt_form)
    ax.xaxis.set_major_formatter("{x:0.1f}")  # Working on ver 3.3+


    ax.set_ylim(-1,17)
    ax.set_yticks(range(0,17,4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    if not ytlab:
        ax.set_yticklabels('')

    if ytright:
        ax.yaxis.tick_right()

    ax.yaxis.set_ticks_position('both')

    ax.tick_params(axis='both',labelsize=10)
    ax.axhline(y=0.,color='k',linestyle=':',lw=0.6)
    ax.axvline(x=0.,color='k',ls=':',lw=0.6)


###--- Synthesizing data to be plotted ---###
x = np.arange(5)
y = x**2

#for x1,y1 in zip(x,y):
#    print(x1,y1)
###---

abc='abcdefghijklmnopqr'

##-- Line setting for plot --##
color_names = ['b','g','r','c','m','y','k','0.7'];lcn=len(color_names)
markers = ['o','^','d','s','D','*','+','x',''];lmk=len(markers)
line_styles = ['-','--',':','-.',''];lls=len(line_styles)

###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(8.5,8.5)    # Physical page size in inches, (lx,ly)

##-- Title for the page --##
suptit="Various Line Properties"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

nrow, ncol= 4,4

left,right,top,bottom = 0.05,0.95,0.925,0.07
npnx=ncol; gapx=0.03
npny=nrow; gapy=0.07
lpnx= (right-left-(npnx-1)*gapx)/npnx
lpny= (top-bottom-(npny-1)*gapy)/npny

ix=left; iy=top
for i in range(nrow*ncol):
    ##-- Set up an axes --##
    ax1 = fig.add_axes([ix,iy-lpny,lpnx,lpny])  # [left,bottom,width,height]

    ##-- Plot on an axes --##
    props=dict(color=color_names[i%lcn],marker=markers[i%lmk],
            linestyle=line_styles[i%lls],markersize=2+i,linewidth=0.5+i*0.3)
    ax1.plot(x,y,**props)
    ### No Marker: just remove "marker=something"
    ### No Line: add "linestyle='None'"


    ##-- Title for each panel --##
    subtit='({}) Msize={}, lw={:.1f}'.format(abc[i],2+i,0.5+i*0.2)
    #plot_common2(ax,subtit='',ytlab=True,ytright=False)

    if i==ncol*(nrow-1):
        ax1.set_xlabel('X-axis Label',fontsize=12)
        ax1.set_ylabel('Y-axis Label',fontsize=12,rotation=90,labelpad=0)

    if i%ncol==ncol-1:
        plot_common2(ax1,subtit,ytlab=True,ytright=True)
    elif i%ncol!=0:
        plot_common2(ax1,subtit,False)
    else:
        plot_common2(ax1,subtit)

    ix=ix+lpnx+gapx
    if ix+lpnx > 1.0:
       ix=left
       iy=iy-lpny-gapy


##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N01_line_plot_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
