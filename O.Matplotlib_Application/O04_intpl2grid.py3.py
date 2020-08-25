'''
Matplotlib Application(4)
: Interpolation from non-grid to grid
: Display scatter(original) and pcolormesh(gridded)

Data
: RMM Index data

By Daeho Jin
'''

import numpy as np
import sys
import os.path
from datetime import date

import O00_Functions as fns
import matplotlib.pyplot as plt
#from matplotlib.ticker import AutoMinorLocator, FixedLocator, MultipleLocator

def main():
    ### Get RMM index
    tgt_dates=(date(2015,1,1),date(2019,12,31))  # Recent 5 years
    time_info, pcs, phs, strs, miss_idx= fns.read_rmm_text(tgt_dates)

    ### Check missing
    if miss_idx.sum()>0:
        print("There are missings:", miss_idx.sum())
        sys.exit()
    else:
        print("No missings")

    ### Check data range
    from math import floor, ceil
    x_range=[floor(pcs[:,0].min()),ceil(pcs[:,0].max())]
    y_range=[floor(pcs[:,1].min()),ceil(pcs[:,1].max())]
    print(x_range,y_range)

    ##-- Interpolate to 2D grid --##
    from scipy.interpolate import griddata
    grid_x= np.arange(x_range[0],x_range[1]+0.01,0.1) # x_res=0.1
    grid_y= np.arange(y_range[0],y_range[1]+0.01,0.1) # y_res=0.1
    grid_x,grid_y= np.meshgrid(grid_x,grid_y)
    grid_z= griddata((pcs[:,0],pcs[:,1]),strs,(grid_x,grid_y),method='cubic',fill_value=np.nan)
    print(grid_x.shape,grid_y.shape,grid_z.shape) #;sys.exit()

    ###--- Plotting Start ---###
    ##-- Page Setup --##
    fig = plt.figure()
    fig.set_size_inches(7.2,5)    # Physical page size in inches, (lx,ly)
    fig.subplots_adjust(left=0.06,right=0.94,top=0.92,bottom=0.1,wspace=0.1) #,hspace=0.3 ### Margins, etc.

    ##-- Title for the page --##
    suptit="Example of Grid Interpolation using griddata"
    fig.suptitle(suptit,fontsize=15,y=0.98,va='bottom')  #,ha='left',x=0.,stretch='semi-condensed')

    abc='abcdefghijklmn'
    cm = plt.cm.get_cmap('CMRmap_r')

    ##-- Set up an axis1 --##
    ax1 = fig.add_subplot(1,2,1)   # (# of rows, # of columns, indicater from 1)
    pic1 = ax1.scatter(pcs[:,0],pcs[:,1],c=strs,s=3,marker='o',alpha=0.9,cmap=cm)

    subtit='(a) Scatter(original)'
    ax1.set_title(subtit,fontsize=12,x=0.,ha='left')
    ax1.set_xlim(x_range)
    ax1.set_ylim(y_range)
    ax1.set_xlabel('PC1',fontsize=11)
    ax1.set_ylabel('PC2',fontsize=11)
    ax1.yaxis.set_ticks_position('both')

    ##-- Set up an axis2 --##
    ax2= fig.add_subplot(1,2,2)   # (# of rows, # of columns, indicater from 1)
    X,Y= np.meshgrid(np.arange(x_range[0]-0.05,x_range[1]+0.06,0.1),np.arange(y_range[0]-0.05,y_range[1]+0.06,0.1)) # Boundary of data
    props = dict(edgecolor='none',alpha=0.8,cmap=cm,vmin=0.)
    pic2 = ax2.pcolormesh(X,Y,grid_z,**props)

    subtit='(b) Pcolormesh(gridded)'
    ax2.set_title(subtit,fontsize=12,x=0.,ha='left')
    ax2.set_xlabel('PC1',fontsize=11)
    ax2.set_ylabel('PC2',fontsize=11,rotation=-90)
    ax2.set_xlim(x_range)
    ax2.set_ylim(y_range)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_ticks_position('both')
    ax2.yaxis.set_label_position("right")

    cb= fns.draw_colorbar(fig,ax2,pic2,type='horizontal',gap=0.11,extend='max')
    ##-- Seeing or Saving Pic --##

    #- If want to see on screen -#
    #plt.show()

    #- If want to save to file
    outdir= '../Pics/'
    outfnm= outdir+'O04_griddata_example_withRMM.png'
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(outfnm,dpi=150,bbox_inches='tight')   # dpi: pixels per inch
    return

if __name__ == "__main__":
    main()
