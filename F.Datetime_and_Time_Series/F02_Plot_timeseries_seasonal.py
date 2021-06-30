"""
Draw seasonal timeseries of U50, NINO3.4, and IOD indices

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

def main():
    ### Parameters
    tgt_dates= (datetime(2010,11,1),datetime(2021,3,1))
    tgt_dates_str= [dd.strftime('%Y/%m') for dd in tgt_dates]  # See Reference above
    mon_per_yr= 12
    times= fns.get_months(*tgt_dates,include_end=True)
    nmons= len(times); print(nmons)
    indir = '../Data/'

    sn_names= ['DJF','MAM','JJA','SON']
    sn_idx= 0
    imon_idx= 13-tgt_dates[0].month + sn_idx*3  # Index for center month of season
    if imon_idx>=12: imon_idx-=12

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

    ### Build Seasonal Mean
    nn34_sn, iod_sn, qbo_sn= [],[],[]
    t1=[]
    for it in range(imon_idx,nmons,12):
        nn34_sn.append(nn34ano[it-1:it+2].mean())
        iod_sn.append(iodano[it-1:it+2].mean())
        qbo_sn.append(u50[it-1:it+2].mean())
        t1.append(times[it])

    ## Usually 'list' also works for plotting, but in case of needing indexing or calculation...
    nn34_sn, iod_sn= np.asarray(nn34_sn), np.asarray(iod_sn)
    qbo_sn, t1= np.asarray(qbo_sn), np.asarray(t1)
    print(nn34_sn.shape, iod_sn.shape)

    outdir= '../Pics/'
    fnout= outdir+'F02_timeseries_seasonal.{}.png'.format(sn_names[sn_idx])
    suptit= "Seasonal Time Series [{}-{} {}]".format(t1[0].year,t1[-1].year,sn_names[sn_idx])
    pdata=dict(xt=t1, yy=[qbo_sn,nn34_sn,iod_sn], data_labels=['U50','Ni\u00F1o3.4','IOD'],
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
    ax1.bar(xt,yy[0],width=90,color='C0',label=data_labels[0],alpha=0.7)  # Use left y-axis
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
