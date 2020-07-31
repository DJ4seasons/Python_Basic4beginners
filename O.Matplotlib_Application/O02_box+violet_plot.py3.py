'''
Matplotlib Application(2)
: Display Box plot and Violin plot to show distribution

Data
: CCMP_Wind_Analysis_20190101_V02.0_L3.0_RSS.daily.nc (obtained from E02)


by Daeho Jin
'''

import sys
import os.path
import numpy as np

from datetime import timedelta, date
from netCDF4 import Dataset

def open_netcdf(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    fid=Dataset(fname,'r')
    print("Open:",fname)
    return fid


def read_nc_variable(fid,var_name):
    vdata=fid.variables[var_name][:]
    if vdata.shape[0]==1:
        vdata=vdata.reshape(vdata.shape[1:])
    return vdata


def main():
    ###--- Read CCMP wind data
    tgt_date= date(2019,1,1)
    date_txt= tgt_date.strftime('%Y%m%d')

    indir= '../Data/'
    infn= indir+'CCMP_Wind_Analysis_{}_V02.0_L3.0_RSS.daily.nc'.format(date_txt)

    fid= open_netcdf(infn)

    var_names= ['uwnd', 'vwnd']
    wnd_data=[]
    for vn in var_names:
        data1= read_nc_variable(fid,vn).reshape(-1)
        data1= data1.compressed()  # Transform Masked_array into numpy array by removing missings
        wnd_data.append(data1)

    outdir= '../Pics/'
    outfn= outdir+'O02_CCMP_Wind_daily_distribution.{}.box+violin.png'

    plot_data= dict(data=wnd_data,var_names=var_names,outfn=outfn)
    plot_main(plot_data)


###---
### Box and Viloin Plot
###---
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
import matplotlib.patches as mpatches

def plot_main(plot_data):
    ###--- Plotting Start ---###
    abc='abcdefghijklmn'
    ##-- Page Setup --##
    fig = plt.figure()
    fig.set_size_inches(6,8.5)    # Physical page size in inches, (lx,ly)
    fig.subplots_adjust(left=0.06,right=0.94,top=0.92,bottom=0.05,hspace=0.25) #,wspace=0.15)  ### Margins, etc.

    ##-- Title for the page --##
    suptit="CCMP Surface Wind distribution on 2019.01.01"
    fig.suptitle(suptit,fontsize=17,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

    nbins=len(plot_data['data'])
    xind=np.arange(nbins)
    cc=['steelblue','#f07575']

    ##-- Set up an axis --##
    ax1 = fig.add_subplot(2,1,1)   # (# of rows, # of columns, indicater from 1)

    flierprops = dict(marker='.',markerfacecolor='gray',markeredgecolor='none',markersize=3,linestyle='none')
    medianprops = dict(color='k',linewidth=1.5)
    meanprops = dict(marker='x',markeredgecolor='k',markerfacecolor='k',markersize=10,markeredgewidth=2)
    capprops = dict(linewidth=1.5,color='k')
    whiskerprops= dict(linewidth=1.5,linestyle='-')


    boxes=[]
    for i in range(nbins):
        boxprops= dict(facecolor=cc[i],linewidth=1.5)
        box1=ax1.boxplot(plot_data['data'][i],positions=[xind[i],],
                    whis=[5,95],widths=0.6,patch_artist=True,showmeans=True,
                    boxprops=boxprops,flierprops=flierprops,
                    medianprops=medianprops,meanprops=meanprops,
                    capprops=capprops,whiskerprops=whiskerprops)
        boxes.append(box1)

    ax1.legend([box["boxes"][0] for box in boxes], plot_data['var_names'],
                loc='upper right', bbox_to_anchor=[0.99,0.98],
                fontsize=12,framealpha=0.6,borderaxespad=0.)

    subtit='(a) Filled Box Plot'
    data_range= [[wnd.min(),wnd.max()] for wnd in plot_data['data']]
    data_max= np.absolute(np.asarray(data_range)).max()+1
    y_range=[-data_max, data_max]
    plot_common(ax1,subtit,xind,plot_data['var_names'],y_range)

    ##-- Set another axis --##
    ax2 = fig.add_subplot(2,1,2)   # (# of rows, # of columns, indicater from 1)

    violins=[]
    for i in range(nbins):
        vio1=ax2.violinplot(plot_data['data'][i],positions=[xind[i],],
                        points=100, widths=0.6,
                        vert=True, showextrema=True)
        violins.append(vio1)

    markerprops= dict(marker='x',c='k',s=100,linewidth=2,zorder=3)  # 'linewidth', not 'linewidths'
    ax2.scatter(xind,[data.mean() for data in plot_data['data']], **markerprops)

    for b1,b2 in zip(*[vio1['bodies'] for vio1 in violins]):
        b1.set_color(cc[0]); b1.set_alpha(0.9)
        b2.set_color(cc[1]); b2.set_alpha(0.9)

    patches= [mpatches.Patch(color=col) for col in cc]
    ax2.legend(patches, plot_data['var_names'],
                loc='upper right', bbox_to_anchor=[0.99,0.98],
                fontsize=12,framealpha=0.6,borderaxespad=0.)

    subtit='(b) Violin Plot'
    plot_common(ax2,subtit,xind,plot_data['var_names'],y_range)

    ##-- Seeing or Saving Pic --##
    #- If want to see on screen -#
    #plt.show()

    #- If want to save to file
    outfnm= plot_data['outfn']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
    return

def plot_common(ax,subtit,xind,x_ticklabels,y_range):
    ax.set_title(subtit,fontsize=14,x=0.,ha='left')
    ax.set_xticks(xind)
    ax.set_xticklabels(x_ticklabels)
    ax.set_xlim(xind[0]-0.6,xind[-1]+1.)

    ax.set_ylim(y_range)
    ax.set_ylabel('Unit= m/s',fontsize=12,labelpad=0)

    ax.tick_params(axis='both',which='major',labelsize=11)
    return

if __name__ == "__main__":
    main()
