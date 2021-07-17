"""
Monthly to daily downscaling interpolation example

By Daeho Jin

----
Reference:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html
"""

import sys
import os.path
import numpy as np
from datetime import date, datetime, timedelta
import F00_common_functions as fns

'''
def get_nn34_daily(infn, t_list):
    tdd0= t_list[0]-timedelta(days=16)
    tdd1= t_list[-1]+timedelta(days=16)
    nn34ano= fns.read_nn34_text(infn,(tdd0,tdd1))  # Need buffers before and after the period
    print(nn34ano.shape, nn34ano.mean())

    ms_idx= nn34ano<-99
    if ms_idx.sum()>0:
        sys.exit('Missing data is found!')
        ### Or some treatment needed (removing, duplication, etc.)

    nn34ano_dy= Interp_mon2day(nn34ano,t_list,(tdd0,tdd1))
    return nn34ano_dy

from scipy.interpolate import interp1d
def Interp_mon2day(vals,t_list,val_dates):
    ### Interpolate Monthly data to Daily data
    ### vals: 1-D, wrapping t_list period

    ## First, we need to decide exact time where the monthly data is located
    xx=[]
    iyr,imon= val_dates[0].year, val_dates[0].month
    mdays=0
    for yy in range(iyr,val_dates[1].year+1,1):
        imm=imon if yy==iyr else 1
        for mm in range(imm,13,1):
            mm2, yy2 = mm+1, yy  # Idenfity next month to identify dy_per_mon
            if mm2>12:
                mm2-=12; yy2=yy+1
            dy_per_mon=(date(yy2,mm2,1)-date(yy,mm,1)).days
            xx.append(dy_per_mon/2+0.5+mdays)  # Center of a month's days
            mdays+=dy_per_mon
            if mm==val_dates[1].month and yy==val_dates[1].year: break
    xx=np.asarray(xx)
    print(vals.shape,xx.shape)

    f= interp1d(xx,vals,kind='cubic')  # Set up the interpolation coefficients

    xnew= [(dd-date(iyr,imon,1)).days for dd in t_list]  # Date points to be interpolated
    xnew= np.asarray(xnew)
    f2= f(xnew)
    print(f2.shape)
    return f2
'''

def main():
    ### Parameters
    tgt_dates= (date(2020,1,1),date(2020,12,31))
    tgt_dates_str= [dd.strftime('%Y.%m%d') for dd in tgt_dates]  # See Reference above
    ndays= (tgt_dates[1]-tgt_dates[0]).days+1
    indir = '../Data/'

    ### Read Nino3.4 values (Reference)
    infn_nn34= indir+'nino3.4_anom.1870-2020.txt'
    nn34ano= fns.read_nn34_text(infn_nn34,tgt_dates)
    mm_times= fns.get_months(*tgt_dates,include_end=True)
    print(nn34ano.shape, nn34ano.mean())

    ### Get interpolated time series of Nino3.4
    ### First, build a list of times where data is interpolated
    dd_times= []
    for t in range(1,ndays,3):  # For example, every 3 days
        dd_times.append(tgt_dates[0]+timedelta(days=t))
    nn34ano_dy= fns.get_nn34_daily(infn_nn34,dd_times)
    print(nn34ano_dy.shape, nn34ano_dy.mean())

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
from matplotlib.dates import DateFormatter, MonthLocator
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

    ax1.xaxis.set_major_formatter(DateFormatter("%Y.%m"))
    ax1.xaxis.set_major_locator(MonthLocator(interval=2))
    ax1.xaxis.set_minor_locator(MonthLocator())

    ax1.set_ylim(-1.5,1.5)
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.set_ylabel('(degC)',fontsize=11)

    ax1.grid()
    ax1.axhline(y=0,c='k',lw=0.8)
    ax1.legend(loc='upper right',fontsize=11)

    ###---
    fnout= pdata['fnout']; print(fnout)
    fig.savefig(fnout,bbox_inches='tight',dpi=150)
    plt.show()
    return

if __name__ == "__main__":
    main()
