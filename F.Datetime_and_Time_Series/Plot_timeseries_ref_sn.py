import sys
import os.path
import numpy as np
from datetime import date
import common_functions as fns
import matplotlib.pyplot as plt

def main():
    ### Parameters
    tgt_dates= (date(2002,12,1),date(2021,3,1))
    tgt_dates_str= ['{}{:02d}'.format(tgt.year, tgt.month) for tgt in tgt_dates]
    nyr, mon_per_yr= tgt_dates[1].year-tgt_dates[0].year, 12
    nmons0, nmons= fns.get_months(*tgt_dates,include_end=True), nyr*mon_per_yr
    indir = '/Users/djin1/Documents/CLD_Work/Data_Obs/'
    print(nmons0, nmons)
    
    ### Read QBO
    '''
    infn_qbo= indir+'QBO_index/data_qbo_u50.nc'
    vars = ['qbo_djf','time','u50','year']
    qbo_data= fns.read_nc_data(infn_qbo,vars)
    ## Check temporal dimension
    t0= qbo_data['time'][:]
    #t1= qbo_data['year'][:]
    print(t0[0]) #, t1[-1], t1.dtype)
    imon= fns.get_months(t0[0],tgt_dates[0])
    if t0[-1]>=tgt_dates[0]:
        u50= qbo_data['u50'][imon:imon+nmons0]
        t0= t0[imon:imon+nmons0]
    else:
        print("Target dates are out of data period", tgt_dates, t0[[0,-1]])
    #yr_idx= np.logical_and(t1>tgt_dates[0].year, t1<=tgt_dates[1].year)
    #qbo_djf= qbo_data['qbo_djf'][yr_idx]
    #t1= t1[yr_idx]
    '''
    infn_qbo= indir+'QBO_index/data_qbo_u50.txt'
    u50= fns.read_qbo_text(infn_qbo,tgt_dates)
    print(u50.shape, u50.mean()) #, qbo_djf.shape) #; sys.exit()
    iyr,imo= tgt_dates[0].year,tgt_dates[0].month
    t0=[]
    for t in range(len(u50)):
        t0.append(date(iyr,imo,1))
        imo+=1
        if imo>12: imo-=12; iyr+=1


    ### Read Nino3.4 values
    infn_nn34= indir+'SST_index/nino3.4_anom.1870-2020.txt'
    nn34ano= fns.read_nn34_text(infn_nn34,tgt_dates)
    print(nn34ano.shape, nn34ano.mean())

    ### Read IOD index values
    infn_iod= indir+'SST_index/IOD_anom.1870-2020.txt'
    iodano= fns.read_nn34_text(infn_iod,tgt_dates)
    print(iodano.shape, iodano.mean())

    ### Build Seasonal Mean
    nn34_sn, iod_sn, qbo_sn= [],[],[]
    t1=[]
    for it in range(1,nmons0,3):
        nn34_sn.append(nn34ano[it-1:it+2].mean())
        iod_sn.append(iodano[it-1:it+2].mean())
        qbo_sn.append(u50[it-1:it+2].mean())
        t1.append(t0[it])
    #nyr= len(t1)//4
    #nn34_sn, iod_sn= np.asarray(nn34_sn).reshape([nyr,4]), np.asarray(iod_sn).reshape([nyr,4])
    #qbo_sn, t1= np.asarray(qbo_sn).reshape([nyr,4]), np.asarray(t1).reshape([nyr,4])
    nn34_sn, iod_sn= np.asarray(nn34_sn), np.asarray(iod_sn)
    qbo_sn, t1= np.asarray(qbo_sn), np.asarray(t1)
    print(nn34_sn.shape, iod_sn.shape)

    outdir= '../Pics_QBO/'
    fnout= outdir+'Fig_timeseries_ref_sn.qbo_CDAS.png'
    pdata=dict(snx=t1, sny=[qbo_sn,nn34_sn,iod_sn], data_labels=['U50','Ni\u00F1o3.4','IOD'],
               fnout=fnout)
    plot_main(pdata)
    return

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FuncFormatter
from matplotlib.dates import DateFormatter
def plot_main(pdata):
    snx= pdata['snx']
    sny= pdata['sny']
    data_labels= pdata['data_labels']
    
    fig= plt.figure()
    fig.set_size_inches(7,5)  ## (xsize,ysize)

    ### Page Title
    suptit="Reference Time Series [{}-{}]".format(snx[0].year,snx[-1].year)
    fig.suptitle(suptit,fontsize=16,y=0.97,va='bottom',stretch='semi-condensed')

    ### Parameters for subplot area
    left,right,top,bottom= 0.07, 0.93, 0.92, 0.07
    npnx,gapx,npny,gapy= 1, 0.11, 1, 0.06
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    abc='abcdefgh'
    sn_name= ['DJF','MAM','JJA','SON']

    ax1= fig.add_axes([ix,iy-ly,lx,ly])
    ax1b= ax1.twinx()
    ax1.bar(snx,sny[0],width=90,color='C0',label=data_labels[0],alpha=0.7)
    ax1b.plot(snx,sny[1],c='C1',label=data_labels[1])
    ax1b.plot(snx,sny[2]*2,c='C5',label=data_labels[2]+'x2')
    ax1.set_ylim(-20,20)
    ax1.set_ylabel('U50 (mm/s)')
    ax1b.set_ylim(-2.5,2.5)
    ax1b.set_ylabel('\u0394SST (degC)',rotation=-90,va='bottom')
    #ax1.set_title('({}) {}'.format(abc[i],sn_name[i]),fontsize=13,ha='left',x=0)
    ax1.grid()
    ax1.grid(which='minor',axis='x',linestyle=':')
    ax1.axhline(y=0,c='k',lw=0.8)
    ax1.xaxis.set_major_formatter(DateFormatter("%Y\n%b"))
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
        #
    #if i==0:
    fig.legend(bbox_to_anchor=(ix+0.03, iy),loc='upper left',fontsize=11, ncol=3)
    iy= iy-ly-gapy

    
    ###---
    fnout= pdata['fnout']
    plt.savefig(fnout,bbox_inches='tight',dpi=150) ### Increase dpi for printing quality
    print(fnout)
    #plt.show()
    return

if __name__ == "__main__":
    main()
