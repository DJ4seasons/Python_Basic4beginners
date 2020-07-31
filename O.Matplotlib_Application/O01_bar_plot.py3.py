'''
Matplotlib Application(1)
: Display Bar plot and Stacked Bar plot

Data
: HadISST1 sample binary file (obtained from D04)
: Make a histogram and display via bar plot

by Daeho Jin
'''

import sys
import os.path
import numpy as np

def bin_file_read2mtx(fname, dtype=np.float32):
    """ Open a binary file, and read data
        fname : file name with directory path
        dtype   : data type; np.float32 or np.float64, etc. """

    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    with open(fname,'rb') as fd:
        bin_mat = np.fromfile(file=fd, dtype=dtype)

    return bin_mat


def main():
    ###--- Prepare Data ---###

    ###--- Parameters
    indir= '../Data/'
    #HadISST1.sample.2017-2019.36x180x360.f32dat
    yrs= [2017,2019]  # Starting year and ending year
    nyears= yrs[1]-yrs[0]+1
    mon_per_yr= 12
    nt= nyears*mon_per_yr
    nlat, nlon= 180, 360

    infn= indir+"HadISST1.sample.{}-{}.{}x{}x{}.f32dat".format(*yrs,nt,nlat,nlon)
    sst= bin_file_read2mtx(infn)  # 'dtype' option is omitted because 'f32' is basic dtype
    sst= sst.reshape([nyears,mon_per_yr*nlat*nlon])
    print(sst.shape)

    ### We already know that missings are -999.9, and ice-cover value is -10.00.
    bin_bounds=[-15,-2]+list(range(2,33,6))  # Ice, then every 6 degC
    bin_bounds[-1]= 40  # End includes extreme values

    #hist,b= np.histogram(sst,bins=bin_bounds, axis=1)  # This is not working since no option 'axis'
    hist_data=[]
    for k in range(sst.shape[0]):
        hist,b= np.histogram(sst[k,:], bins=bin_bounds)
        hist= hist/hist.sum()*100.
        hist_data.append(hist)

    ### Call a function to draw the bar chart
    data_labels= [2017, 2018, 2019]
    outdir= '../Pics/'
    fig_filename= outdir+'O01_HadISST1_histogram_bar.png'

    plot_data= dict(fig_data=hist_data, bin_bounds=bin_bounds,
                data_labels=data_labels, outfn=fig_filename)
    plot_main(plot_data)
    return

###---------
### Bar plot
###---------
### Plan to draw two axes
### 1. Usual(vertical) Bar plot
### 2. Stacked Bar plot
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FormatStrFormatter

def plot_main(plot_data):

    fig= plt.figure()
    fig.set_size_inches(6,8.5)  ## (xsize,ysize)

    ### Page Title
    suptit= "Monthly HadISST1 Histogram"
    fig.suptitle(suptit,fontsize=17,y=0.97,va='bottom') #stretch='semi-condensed'

    ### Parameters for subplot area
    left,right,top,bottom= 0.05, 0.95, 0.925, 0.05
    npnx,gapx,npny,gapy= 1, 0.03, 2.3, 0.09
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny; ly2=ly*1.3
    ix,iy= left, top

    nvars= len(plot_data['fig_data'])
    nbins= len(plot_data['fig_data'][0])

    ###-- Top Panel
    ### Compare strength distribution of phase 3 and 6
    ax1=fig.add_axes([ix,iy-ly,lx,ly])
    wd=0.8/nvars  # Width of bar
    xlocs= bar_x_locator(wd, data_dim=[nvars,nbins])
    cc=['deeppink','skyblue','gold','0.7']  # Preset colors for each bars

    ### Draw Bar Plot
    for i,(data,d_label) in enumerate(zip(plot_data['fig_data'],plot_data['data_labels'])):
        pbar= ax1.bar(xlocs[i], data, width=wd, color=cc[i],
                alpha=0.8, label=d_label)

    ### Fine tuning and decorating
    y_range=[0,25]
    subtit='(a) SST Histogram by Year'
    bar_common(ax1,subtit,x_dim=nbins,xt_labs=plot_data['bin_bounds'],y_range=y_range)
    ax1.set_xlabel('SST (degC)', fontsize=12) #,labelpad=0)
    ax1.set_ylabel('Percent(%)', fontsize=12)
    ax1.legend(loc='upper center',ncol=3,fontsize=11,framealpha=0.6)

    iy=iy-ly-gapy
    ###-- Bottom Panel
    ### Stacked bar for all years
    ax2=fig.add_axes([ix,iy-ly2,lx,ly2])
    wd=0.8  # Width of bar
    xlocs= bar_x_locator(wd, data_dim=[1, nbins])

    ### Draw stacked bar
    ### - Need information of bar base
    base=np.zeros([nbins,])
    for i,(data,d_label) in enumerate(zip(plot_data['fig_data'],plot_data['data_labels'])):
        pbar2=ax2.bar(xlocs[0], data, width=wd, bottom=base, color=cc[i],
                alpha=0.9, label=d_label)
        write_val(ax2, data, xlocs[0], base+data/2., crt=10)
        base+=data ### Update base of bar

    ### Fine tuning and decorating
    y_range=[0,80]
    subtit='(b) SST Histogram for all years'
    bar_common(ax2,subtit, x_dim=nbins, xt_labs=plot_data['bin_bounds'], y_range=y_range)
    ax2.set_xlabel('SST (degC)', fontsize=12) #,labelpad=0)
    ax2.set_ylabel('Percent(%)', fontsize=12)
    ax2.legend(loc='upper left',bbox_to_anchor=(1.01,1.),borderaxespad=0,fontsize=10)

    ##-- Seeing or Saving Pic --##

    #- If want to see on screen -#
    #plt.show()

    #- If want to save to file
    outfnm= plot_data['outfn']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

    # Defalut: facecolor='w', edgecolor='w', transparent=False
    return

def bar_x_locator(width,data_dim=[1,10]):
    """
    Depending on width and number of bars,
    return bar location on x axis
    Input width: (0,1) range
    Input data_dim: [# of vars, # of bins]
    Output locs: list of 1-D array(s)
    """
    xx=np.arange(data_dim[1])
    shifter= -width/2*(data_dim[0]-1)
    locs=[]
    for x1 in range(data_dim[0]):
        locs.append(xx+(shifter+width*x1))
    return locs

def bar_common(ax,subtit,x_dim=10,xt_labs=[],y_range=[]):
    """
    Decorating Bar plot
    """
    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)

    ### Axis Control
    xx=np.arange(x_dim+1)
    ax.set_xlim(xx[0]-0.6,xx[-2]+0.6)
    ax.set_xticks(xx-0.5)
    ax.set_xticklabels(xt_labs) #,rotation=35,ha='right')
    if len(y_range)==2:
        ax.set_ylim(y_range[0],y_range[1])

    ### Ticks and Grid
    ax.tick_params(axis='both',which='major',labelsize=10)
    ax.yaxis.set_major_formatter(FormatStrFormatter("%d%%"))
    if y_range[1]-y_range[0]<=5:
        ax.yaxis.set_major_locator(MultipleLocator(1))
    elif y_range[1]-y_range[0]<=10:
        ax.yaxis.set_major_locator(MultipleLocator(2))
    elif y_range[1]-y_range[0]<=30:
        ax.yaxis.set_major_locator(MultipleLocator(5))
    elif y_range[1]-y_range[0]<=50:
        ax.yaxis.set_major_locator(MultipleLocator(10))
    else:
        ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(axis='y',color='0.7', linestyle=':', linewidth=1)
    return

def write_val(ax,values,xloc,yloc,crt=0,ha='center',va='center'):
    """
    Show values on designated location if val>crt.
    Input values, xloc, and yloc should be of same dimension
    """
    ### Show data values
    for val,xl,yl in zip(values,xloc,yloc):
        if val>crt: # Write large enough numbers only
            pctxt='{:.0f}%'.format(val)
            ax.text(xl,yl,pctxt,ha=ha,va=va,stretch='semi-condensed',fontsize=10)
    return

if __name__ == "__main__":
    main()
