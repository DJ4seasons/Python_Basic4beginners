"""
Daily to Pentad/Monthly example using RMM MJO indices
: Daily to pentad (using Numpy)
: Daily to monthly (using Numpy)
: Daily to monthly (using Pandas)

By Daeho Jin
"""

import sys
import os.path
import numpy as np
from datetime import date, datetime, timedelta
import F00_common_functions as fns
import pandas as pd

def daily_to_pentad1(ts1d,xt,tdelta=5):
    """
    Convert 1-D daily time series (ts1d) to pentad (or any time mean)
    """
    n_ptd= ts1d.shape[0]//tdelta
    ts_ptd= ts1d[:n_ptd*tdelta].reshape([n_ptd,tdelta]).mean(axis=1)
    xt_ptd= xt[int((tdelta-1)/2)::tdelta]
    return ts_ptd,xt_ptd

def daily_to_pentad2(ts1d,xt,tgt_dates,tdelta=5):
    """
    Convert 1-D daily time series (ts1d) to pentad (or any time mean)
    Temporal mean is performed from the same day of every year.
    """

    date1= tgt_dates[0]
    ts_ptd, xt_ptd=[],[]
    while(date1+timedelta(days=365)<=tgt_dates[1]):
        tidx= (date1-tgt_dates[0]).days
        n_ptd= 365//tdelta
        ts_ptd1= ts1d[tidx:tidx+n_ptd*tdelta].reshape([n_ptd,tdelta]).mean(axis=1)
        xt_ptd1= xt[tidx+int((tdelta-1)/2):tidx+365:tdelta]
        ts_ptd.append(ts_ptd1)
        xt_ptd.append(xt_ptd1)
        date1= date1+timedelta(days=365)

    return np.concatenate(ts_ptd),np.concatenate(xt_ptd)

def daily_to_monthly1(ts1d,tgt_dates):
    """
    Convert 1-D daily time series (ts1d) to monthly
    Temporal mean is performed based on calendar month.
    """
    date1= tgt_dates[0]

    ts_mm, xt_mm=[],[]
    while(True):
        yr1,mm1= date1.year, date1.month
        yr2,mm2= yr1,mm1+1
        if mm2>12:
            yr2+=1; mm2-=12
        date2= date(yr2,mm2,1)
        if date2<=tgt_dates[1]:
            ndy= (date2-date1).days
        else:
            ndy= (tgt_dates[1]-date1).days+1

        if ndy>20:  # minimum days to represent a month
            tidx= (date1-tgt_dates[0]).days
            ts_mm.append(ts1d[tidx:tidx+ndy].mean())
            xt_mm.append(date(yr1,mm1,15))
            date1= date2
        else:
            break
    return np.asarray(ts_mm),xt_mm

def daily_to_monthly_wPandas(ts1d,tgt_dates):
    """
    Convert 1-D daily time series (ts1d) to monthly using Pandas function
    Temporal mean is performed based on calendar month.
    """
    if ts1d.ndim==1:
        data1= np.copy(ts1d).reshape([-1,1])
    elif ts1d.ndim==2:
        data1= ts1d
    else:
        sys.exit("Too many dims of ts1d", ts1d.ndim)

    df1= pd.DataFrame(data1,index=pd.date_range(*tgt_dates,freq='D'))
    df1= df1.resample('M').mean()
    data1= df1.to_numpy()
    return np.squeeze(data1),df1.index.values

def main():
    ### Parameters
    tgt_dates= (date(2018,6,1),date(2020,5,31))
    tgt_dates_str= [dd.strftime('%Y.%m%d') for dd in tgt_dates]  # See Reference above
    ndays= (tgt_dates[1]-tgt_dates[0]).days+1
    #indir = '../Data/'

    ### Get RMM index
    time_info, pcs, phs, strs, miss_idx= fns.read_rmm_text(tgt_dates)

    ### Check missing
    if miss_idx.sum()>0:
        print("There are missings:", miss_idx.sum())
        sys.exit()
    else:
        print("No missings")

    ### Reference daily time series
    ts0= pcs[:,0]  # PC1
    xt0=[dd for dd in fns.yield_date_range(*tgt_dates,tdelta=1)]

    ### Daily to pentad
    ## Method1
    #ts_ptd,xt_ptd= daily_to_pentad1(ts0,xt0); print(ts_ptd.shape, len(xt_ptd))
    ## Method2
    ts_ptd,xt_ptd= daily_to_pentad2(ts0,xt0,tgt_dates)
    print(ts_ptd.shape, len(xt_ptd))

    ### Daily to monthly
    ts_mon,xt_mon= daily_to_monthly1(ts0,tgt_dates)
    print(ts_mon.shape, len(xt_mon))

    ### Daily to monthly using Pandas
    ts_mon_p,xt_mon_p= daily_to_monthly_wPandas(ts0,tgt_dates)
    print(ts_mon_p.shape, len(xt_mon_p))
    
    sys.exit()


    outdir= '../Pics/'
    fnout= outdir+'F03_monthly_to_daily_ex1.png'
    suptit= "Monthly and Daily NINO34 Time Series [{}-{}]".format(*tgt_dates_str)
    pdata=dict(m_data=(mm_times,nn34ano), d_data=(dd_times,nn34ano_dy),
                data_labels=['Monthly','3-Daily',],
                suptit=suptit,fnout=fnout)
    plot_main(pdata)
    return

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FuncFormatter
from matplotlib.dates import DateFormatter
def plot_main(pdata):
    mx,my= pdata['m_data']
    dx,dy= pdata['d_data']
    data_labels= pdata['data_labels']

    fig= plt.figure()
    fig.set_size_inches(7.5,5)  ## (xsize,ysize)

    ### Page Title
    suptit= pdata['suptit']
    fig.suptitle(suptit,fontsize=15,y=0.97,va='bottom',stretch='semi-condensed')

    ### Parameters for subplot area
    abc='abcdefgh'
    fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.07)

    wd= (dx[1]-dx[0]).days*0.8
    ### Plot time series
    ax1= fig.add_subplot(111)
    ax1.bar(dx,dy,width=wd,color='C0',label=data_labels[1],alpha=0.7)
    ax1.plot(mx,my,c='C1',marker='^',markersize=10,lw=2,alpha=0.9,label=data_labels[0])

    ax1.set_ylim(-2.,2.)
    ax1.grid()
    ax1.axhline(y=0,c='k',lw=0.8)
    ax1.xaxis.set_major_formatter(DateFormatter("%Y.%m"))
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.set_ylabel('(degC)',fontsize=11)

    ax1.legend(loc='upper right',fontsize=11)

    ###---
    fnout= pdata['fnout']
    fig.savefig(fnout,bbox_inches='tight',dpi=150)
    print(fnout)
    #plt.show()
    return

if __name__ == "__main__":
    main()
