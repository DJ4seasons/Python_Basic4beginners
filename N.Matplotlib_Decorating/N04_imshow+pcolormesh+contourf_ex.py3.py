import numpy as np
import sys

import matplotlib   ### Discover Only
matplotlib.use('TkAgg')   ### Discover Only

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

def plot_common(ax,subtit,xlin,ylin):
    ax.set_title(subtit,fontsize=12,x=0.,ha='left') #,y=0.9

    ax.set_xticks(np.linspace(0,len(xlin)-1,4))
    ax.set_xticklabels([-2,0,2,4])
    ax.set_yticks(np.linspace(0,len(ylin)-1,5))
    ax.set_yticklabels([-3,-1,1,3,5])
    
    #ax.yaxis.set_ticks_position('both')        
    ax.tick_params(axis='both',labelsize=10)

def plot_common2(ax,subtit=''):
    ax.set_title(subtit,fontsize=12,x=0.,ha='left',stretch='condensed') #,y=0.9

    ax.set_xlim(-2,4)
    ax.xaxis.set_major_locator(MultipleLocator(2))   # For Major Ticks
    #ax.xaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks
    #xt_form=FuncFormatter(lambda x, pos: "{:0.1f}".format(x))
    #ax.xaxis.set_major_formatter(xt_form)
   
    ax.set_ylim(-3,5)
    ax.set_yticks(range(-3,6,2))
    #ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    #ax.yaxis.set_ticks_position('both')        
    ax.tick_params(axis='both',labelsize=10)



###---

abc='abcdefghijklmn'
###--- Plotting Start ---###  

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(8,7.5)    # Physical page size in inches, (lx,ly)
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.925,wspace=0.2,hspace=0.3)

##-- Title for the page --##
suptit="imshow vs. pcolormesh vs. contourf"
fig.suptitle(suptit,fontsize=15,y=1.0)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

nrow, ncol= 3,4

for i in range(2):

    ###--- Synthesizing data to be plotted ---###
    xlin = np.linspace(-2,4,6*10**i+1)
    ylin = np.linspace(-3,5,8*10**i+1)
    X,Y = np.meshgrid(xlin,ylin)
    Z = 1./(np.exp((X/3.)**2+(Y/5.)**2))
    res = 1./(10.**i)

    ##-- imshow with nearest
    ax1= fig.add_subplot(nrow,ncol,i+1)
    pic1= ax1.imshow(Z,origin='lower',cmap='jet',interpolation='nearest')
    subtit='({}) imshow nearest'.format(abc[i])
    plot_common(ax1,subtit,xlin,ylin)

    ax2= fig.add_subplot(nrow,ncol,i+3)
    pic2= ax2.imshow(Z,origin='lower',cmap='jet',interpolation='bilinear') ### 10 more intepolation method available
    subtit='({}) imshow bilinear'.format(abc[i+2])
    plot_common(ax2,subtit,xlin,ylin)
    ax2.set_aspect('auto')

    ax3= fig.add_subplot(nrow,ncol,i+5)
    pic3= ax3.pcolormesh(X,Y,Z,cmap='jet',shading='flat')
    subtit='({}) pcolormesh flat'.format(abc[i+4])
    plot_common2(ax3,subtit)

    ax4= fig.add_subplot(nrow,ncol,i+7)
    pic4= ax4.pcolormesh(X,Y,Z,cmap='jet',shading='gouraud')
    subtit='({}) pcolormesh gouraud'.format(abc[i+6])
    plot_common2(ax4,subtit)

    ax5= fig.add_subplot(nrow,ncol,i+9)
    pic5= ax5.contourf(X,Y,Z,10,cmap='jet')
    subtit='({}) contourf clev=10'.format(abc[i+8])
    plot_common2(ax5,subtit)

    ax6= fig.add_subplot(nrow,ncol,i+11)
    pic6= ax6.contourf(X,Y,Z,100,cmap='jet')  ### [clevel]: it's ok with 'array-like' instead of number 100
    subtit='({}) contourf clev=100'.format(abc[i+10])
    plot_common2(ax6,subtit)

        


##-- Seeing or Saving Pic --##

#- If want to see on screen -#
plt.show()

#- If want to save to file
outdir = "/home/djin1/Zbegins_Python/Py3_lecture_2019/data/Pics/"
outfnm = outdir+"imshow+pcolormesh+contourf.png"
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
sys.exit()


### Legend Guide
### https://matplotlib.org/3.1.0/tutorials/intermediate/legend_guide.html
