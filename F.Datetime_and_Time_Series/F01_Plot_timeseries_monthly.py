"""
Draw monthly timeseries of U50, NINO3.4, and IOD indices

By Daeho Jin

----
Reference:
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
"""

import sys
import os.path
import numpy as np
from datetime import datetime
import F00_common_functions as fns
import matplotlib.pyplot as plt

def main():
    ### Parameters
    tgt_dates= (datetime(2010,11,1),datetime(2021,3,1))
    tgt_dates_str= [dd.strftime('%Y/%m') for dd in tgt_dates]  # See Reference above
    
    times= fns.get_months(*tgt_dates,include_end=True)
    nmons= len(times); print(nmons)
    indir = '../Data/'

    ### Read QBO
    infn_qbo= indir+'data_qbo_u50.txt'
    u50= fns.read_qbo_text(infn_qbo,tgt_dates)
    print(u50.shape, u50.mean())

    ### Read Nino3.4 values
    infn_nn34= indir+'nino3.4_anom.1870-2020.txt'
    nn34ano= fns.read_nn34_text(infn_nn34,tgt_dates)
    print(nn34ano.shape, nn34ano.mean())

    ### Read IOD index values
    infn_iod= indir+'IOD_anom.1870-2020.txt'
    iodano= fns.read_nn34_text(infn_iod,tgt_dates)
    print(iodano.shape, iodano.mean())

    outdir= '../Pics/'
    fnout= outdir+'F01_timeseries_monthly.png'
    suptit= "Monthly Time Series [{}-{}]".format(*tgt_dates_str)
    pdata=dict(xt=times, yy=[u50,nn34ano,iodano], data_labels=['U50','Ni\u00F1o3.4','IOD'],
                suptit=suptit,fnout=fnout)
    plot_main(pdata)
    return

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FuncFormatter
from matplotlib.dates import DateFormatter
def plot_main(pdata):
    xt,yy= pdata['xt'],pdata['yy']
    data_labels= pdata['data_labels']

    fig= plt.figure()
    fig.set_size_inches(6,4.5)  ## (xsize,ysize)

    ### Page Title
    suptit= pdata['suptit']
    fig.suptitle(suptit,fontsize=15,y=0.97,va='bottom',stretch='semi-condensed')

    ### Parameters for subplot area
    abc='abcdefgh'
    fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.07)

    ### Plot time series
    ax1= fig.add_subplot(111)
    ax1b= ax1.twinx()
    ax1.plot(xt,yy[0],c='C0',lw=4,alpha=0.7,label=data_labels[0])  # Use left y-axis
    ax1b.plot(xt,yy[1],c='C1',lw=1.5,alpha=0.9,label=data_labels[1])  # Use right y-axis
    ax1b.plot(xt,yy[2]*2,c='C5',lw=1.5,alpha=0.9,label=data_labels[2]+'x2') # Use right y-axis

    ax1.set_ylim(-25,25)
    ax1b.set_ylim(-2.5,2.75)
    #ax1.set_title('(a) Monthly',fontsize=13,ha='left',x=0)
    ax1.grid()
    ax1.axhline(y=0,c='k',lw=0.8)
    ax1.xaxis.set_major_formatter(DateFormatter("%Y\n%b"))
    # <--- For more information of Date Format, see Reference above
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1b.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.set_ylabel('(m/s)',fontsize=11)
    ax1b.set_ylabel('(degC)',fontsize=11,rotation=-90,va='bottom')

    fig.legend(bbox_to_anchor=(0.06, 0.075), loc='lower left',fontsize=11,
               ncol=3, borderaxespad=0.)

    ###---
    fnout= pdata['fnout']
    fig.savefig(fnout,bbox_inches='tight',dpi=150)
    print(fnout)
    #plt.show()
    return

if __name__ == "__main__":
    main()
