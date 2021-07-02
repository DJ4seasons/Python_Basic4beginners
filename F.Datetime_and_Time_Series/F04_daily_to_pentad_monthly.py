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
    data1= df1.to_numpy()  # Convert to numpy array
    xt= df1.index #.values
    return np.squeeze(data1), xt

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
    print(ts_ptd.shape, len(xt_ptd), xt_ptd[0])

    ### Daily to monthly
    ts_mon,xt_mon= daily_to_monthly1(ts0,tgt_dates)
    print(ts_mon.shape, len(xt_mon), xt_mon[0])

    ### Daily to monthly using Pandas
    ts_mon_p,xt_mon_p= daily_to_monthly_wPandas(ts0,tgt_dates)
    print(ts_mon_p.shape, len(xt_mon_p), xt_mon_p[0])

    ### For plotting
    outdir= '../Pics/'
    fnout= outdir+'F04_daily_to_pentad_and_monthly_ex1.png'
    suptit= "Daily to Pentad/Monthly Timeseries [{}-{}]".format(*tgt_dates_str)
    pdata=dict(d_data=(xt0,ts0),
                ts_data=[(xt_ptd,ts_ptd),(xt_mon,ts_mon),(xt_mon_p,ts_mon_p)],
                titles=['Pentad','Monthly','Monthly with Pandas',],
                suptit=suptit,fnout=fnout)
    plot_main(pdata)
    return

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FuncFormatter
from matplotlib.dates import DateFormatter
def plot_common(ax1,subtit):
    ax1.set_title(subtit,fontsize=12,x=0,ha='left')
    ax1.set_ylim(-2.5,3.5)
    ax1.grid()
    ax1.axhline(y=0,c='k',lw=0.8)
    ax1.xaxis.set_major_formatter(DateFormatter("%Y\n%b"))
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.set_ylabel('RMM PC1',fontsize=11)

def plot_main(pdata):
    dx,dy= pdata['d_data']
    titles= pdata['titles']
    ts_data= pdata['ts_data']

    fig= plt.figure()
    fig.set_size_inches(6,8.5)  ## (xsize,ysize)

    ### Page Title
    suptit= pdata['suptit']
    fig.suptitle(suptit,fontsize=15,y=0.975,va='bottom',stretch='condensed')

    ### Parameters for subplot area
    abc='abcdefgh'

    lf,rf,tf,bf = 0.04, 0.94, 0.94, 0.07
    gapx,gapy = 0.05, 0.08
    nrow,ncol = 3, 1
    lpnx=(rf-lf-gapx*(ncol-1))/ncol
    lpny=(tf-bf-gapy*(nrow-1))/nrow

    ### Plot time series
    ix,iy= lf,tf
    for i,(tit,(xt,ydata)) in enumerate(zip(titles,ts_data)):
        ax1= fig.add_axes([ix,iy-lpny,lpnx,lpny])  # [left,bottom,width,height]
        ## Line plots
        ax1.plot(dx,dy,c='C1',lw=1,alpha=0.9)
        ax1.plot(xt,ydata,c='C0',lw=3,alpha=0.6)

        subtit= '({}) {}'.format(abc[i],tit)
        plot_common(ax1,subtit)

        ix=ix+lpnx+gapx
        if ix>rf: ix=lf; iy=iy-lpny-gapy

        ###---
    fnout= pdata['fnout']
    fig.savefig(fnout,bbox_inches='tight',dpi=150)
    print(fnout)
    plt.show()
    return

if __name__ == "__main__":
    main()
