import sys
import os.path
import numpy as np
from datetime import date
import common_functions as fns
import matplotlib.pyplot as plt

def main():
    ### Parameters
    tgt_dates= (date(2002,12,1),date(2021,2,28))
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

    ###--- Read MJO data
    mjo_time_range= tgt_dates #(date_range[0],date(2020,2,7))  ## Time limit of OMI
    mjo_id=1  ## 0:RMM, 1:OMI
    mjo_nm= ['RMM','OMI']
    time_info,pcs,strs= fns.read_mjoidx_text(mjo_id,date_range=mjo_time_range,omi_flip=True)
    #mons= np.asarray([dd.month for dd in time_info])
    #mjo_indices= [pcs[:,0]-pcs[:,1], pcs[:,0], pcs[:,0]+pcs[:,1], pcs[:,1]] ## Corresponding to Phase 3/4, 4/5, 5/6, 6/7
    #phs= fns.get_phs(pcs)
    print(type(strs), strs.shape) #; sys.exit()

    ### Build Seasonal Mean
    nn34_sn, iod_sn, qbo_sn= [],[],[]
    mjo_sn=[]
    t1=[]
    iyr, eyr= tgt_dates[0].year+1, tgt_dates[1].year
    for it in range(1,nmons0,3):
        nn34_sn.append(nn34ano[it-1:it+2].mean())
        #iod_sn.append(iodano[it-1:it+2].mean())
        qbo_sn.append(u50[it-1:it+2].mean())
        t1.append(t0[it])
        ## For MJO index
        tidx= (t0[it]-tgt_dates[0]).days
        mjo_sn.append([strs[tidx-31:tidx+60].mean(),strs[tidx-31:tidx+60].std()])
        #if mjo_sn[-1]>2:
        #    print(strs[tidx-31:tidx+60])

    #nyr= len(t1)//4
    #nn34_sn, iod_sn= np.asarray(nn34_sn).reshape([nyr,4]), np.asarray(iod_sn).reshape([nyr,4])
    #qbo_sn, t1= np.asarray(qbo_sn).reshape([nyr,4]), np.asarray(t1).reshape([nyr,4])
    nn34_sn, mjo_sn= np.asarray(nn34_sn), np.asarray(mjo_sn)
    qbo_sn, t1= np.asarray(qbo_sn), np.asarray(t1)
    print(nn34_sn.shape, mjo_sn.shape)
    print( mjo_sn[::4,0].min(),  mjo_sn[::4,0].max())
    print( mjo_sn[::4,1].min(),  mjo_sn[::4,1].max())
    #sys.exit()
    ### Build seasonal std of MJO strength



    outdir= '../Pics_QBO/'
    fnout= outdir+'Fig_timeseries_ref_sn_scatter.qbo_CDAS_byMJO_{}_DJF.png'.format(mjo_nm[mjo_id])
    pdata=dict(snx=t1, sny=[qbo_sn,nn34_sn,mjo_sn],
               data_labels=['U50 (mm/s)','Ni\u00F1o3.4 Anomaly (\u00B0C)',('MJO Mean Amplitude','MJO Amplitude STD')],
               fnout=fnout, suptit='MJO Index= {} in DJF'.format(mjo_nm[mjo_id]))
    plot_main(pdata)
    return

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FuncFormatter
from matplotlib.dates import DateFormatter
def plot_main(pdata):
    snx= pdata['snx']
    sny= pdata['sny']
    data_labels= pdata['data_labels']
    clabels= data_labels[-1]

    fig= plt.figure()
    fig.set_size_inches(9,4)  ## (xsize,ysize)

    ### Page Title
    suptit= pdata['suptit']
    fig.suptitle(suptit,fontsize=16,y=0.97,va='bottom',stretch='semi-condensed')

    ### Parameters for subplot area
    left,right,top,bottom= 0.05, 0.95, 0.93, 0.07
    npnx,gapx,npny,gapy= 2, 0.16, 1, 0.09
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    abc='abcdefgh'
    #sn_name= ['DJF','MAM','JJA','SON']
    cm0= plt.cm.get_cmap('magma_r')
    cm1= plt.cm.get_cmap('magma_r')
    if suptit.split()[2]=='RMM':
        vmins,vmaxes=[1,0.5],[2,0.85]
    elif suptit.split()[2]=='OMI':
        vmins,vmaxes=[0.8,0.3],[2,0.75]

    #props= dict(cmap=cm,vmin=-0.6,vmax=0.6)
    props= (dict(cmap=cm0,vmin=vmins[0],vmax=vmaxes[0],s=60,alpha=0.9),dict(cmap=cm1,vmin=vmins[1],vmax=vmaxes[1],s=60,alpha=0.9))
    lb_delta=0.045

    for i,clab in enumerate(clabels):
        ax1= fig.add_axes([ix,iy-ly,lx,ly])
        pic1=ax1.scatter(sny[0][::4],sny[1][::4],c=sny[2][::4,i],**props[i])
        ax1.set_xlim(-20,15)
        ax1.set_ylim(-2.5,2.5)
        #ax1.set_title('DJF',fontsize=13,ha='left',x=0)
        ax1.grid()
        ax1.set_facecolor('0.9')
        ax1.set_xlabel(data_labels[0],fontsize=11)
        ax1.set_ylabel(data_labels[1],fontsize=11,labelpad=0)
        #ax1.grid(which='minor',axis='x',linestyle=':')
        #ax1.axhline(y=0,c='k',lw=0.8)
        #ax1.xaxis.set_major_formatter(DateFormatter("%Y\n%b"))
        #ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
        for xloc,yloc,cloc,tinfo in zip(sny[0][::4],sny[1][::4],sny[2][::4,i],snx[::4]):
            #print(tinfo,xloc,yloc,cloc)
            ax1.annotate('{:02d}'.format(tinfo.year%100),(xloc+lb_delta/5,yloc-lb_delta),color='0.1',fontsize=10,ha='left',va='top',stretch='condensed')
        #

        cb1=fns.draw_colorbar(fig,ax1,pic1,type='vertical',size='panel',extend='both',gap=0.02,width=0.02)
        #cb1.set_ticks(range(0,21,5))
        cb1.set_label(clab,fontsize=11,labelpad=2,rotation=-90, va='bottom')
        ix=ix+lx+gapx
        if ix>right:
            iy= iy-ly-gapy
            ix=left


    ###---
    fnout= pdata['fnout']
    plt.savefig(fnout,bbox_inches='tight',dpi=150) ### Increase dpi for printing quality
    print(fnout)
    #plt.show()
    return

def get_months(time0,time1,include_end=False):
    iyr, imo= time0.year, time0.month
    eyr, emo= time1.year, time1.month
    if iyr==eyr:
        if imo<=emo:
            return emo-imo+int(include_end)
    elif iyr<eyr:
        return (12-imo)+(eyr-iyr-1)*12+emo+int(include_end)
    sys.exit('time1, {} should be later than time0, {}'.format(time1,time0))
    return

def read_qbo_text(infn,tgt_dates):
    tgt_iyr, tgt_eyr= tgt_dates[0].year, tgt_dates[1].year

    with open(infn,'r') as f:
        lines, years=[],[]
        for line in f:
            line= line.strip()
            if len(line)>2 and (line[0:2]=='19' or line[0:2]=='20'):
                years.append(int(line[0:4]))
                ww=[]
                for idx in range(4,len(line),7):
                    ww.append(float(line[idx:idx+7]))
                lines.append(ww)

    iyr,eyr= years[0], years[-1]
    outdata=[]
    undef= lines[-1][-1]
    if iyr>tgt_iyr:
        for yy in range(tgt_iyr,iyr):
            outdata.append([undef,]*12)
    for i,wws in enumerate(lines):
        lyy= years[i]
        if lyy>=tgt_iyr and lyy<=tgt_eyr:
            outdata.append(wws)
    if tgt_eyr>eyr:
        for yy in range(eyr+1,tgt_eyr+1,1):
            outdata.append([undef,]*12)

    outdata= np.asarray(outdata).reshape(-1)
    if tgt_dates[0].month!=1 or tgt_dates[1].month!=12:
        imon= tgt_dates[0].month-1
        emon= tgt_dates[1].month-12
        outdata= outdata[imon:emon] if emon<0 else outdata[imon:]

    return outdata

def read_mjoidx_text(mjo_id,date_range=[],omi_flip=False):
    """
    Read RMM or OMI Index Text file
    fname: include directory
    date_range: start and end dates, including both end dates, optional
    """
    mjo_idx_nm= ['RMM','OMI']
    mjo_idx_fn= ['rmm.74toRealtime.txt','omi.79toRealtime.txt']
    mjo_idx_dir='/Users/djin1/Documents/CLD_Work/Data_Obs/'
    fname= mjo_idx_dir+mjo_idx_fn[mjo_id]

    if not os.path.isfile(fname):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist: "+fname)

    if len(date_range)!=0 and len(date_range)!=2:
        print("date_range should be [] or [ini_date,end_date]")
        sys.exit()

    mjo_kind= fname.strip().split('/')[-1].split('.')[0]
    if mjo_kind=='rmm':
        nheader=2
        pc_idx= [3,4]
        strs_idx= 6
    elif mjo_kind=='omi':
        nheader=0
        pc_idx= [4,5]
        strs_idx= 6
    else:
        sys.exit("Now only rmm and omi are supported")

    time_info, pcs, strs = [], [], []
    with open(fname,'r') as f:
        for i,line in enumerate(f):
            if i>=nheader:  ### Skip header (2 lines)
                ww=line.strip().split() #
                onedate=date(*map(int,ww[0:3])) ### "map()": Apply "int()" function to each members of ww[0:3]
                if len(date_range)==0 or (len(date_range)==2 and onedate>=date_range[0] and onedate<=date_range[1]):
                    pcs.append([float(ww[k]) for k in pc_idx]) ### PC1 and PC2
                    strs.append(float(ww[strs_idx]))  ### MJO strength
                    #months.append(onedate.month)
                    time_info.append(onedate)  ### Save date-info for displaying time-series

    print("Total {} data record=".format(mjo_idx_nm[mjo_id]),len(strs))
    time_info= np.asarray(time_info)
    pcs= np.asarray(pcs)
    if mjo_id==1 and omi_flip:
        pcs[:,0]*=-1
        pcs= pcs[:,::-1]
    strs= np.asarray(strs)
    return time_info,pcs,strs ### Return as Numpy array
    
def read_nn34_text(infn,tgt_dates):
    tgt_iyr, tgt_eyr= tgt_dates[0].year, tgt_dates[1].year

    with open(infn,'r') as f:
        lines=[]
        for line in f:
            ww= line.strip().split()
            if len(ww)>0:
                if ww[0][:3]=='-99':
                    undef= float(ww[0])
                    break
                else:
                    lines.append(ww)

    iyr,eyr= map(int,lines[0])
    outdata=[]
    if iyr>tgt_iyr:
        for yy in range(tgt_iyr,iyr):
            outdata.append([undef,]*12)
    for wws in lines[1:]:
        lyy= int(wws[0])
        if lyy>=tgt_iyr and lyy<=tgt_eyr:
            outdata.append([float(val) for val in wws[1:13]])
    if tgt_eyr>eyr:
        for yy in range(eyr+1,tgt_eyr+1,1):
            outdata.append([undef,]*12)

    outdata= np.asarray(outdata).reshape(-1)
    if tgt_dates[0].month!=1 or tgt_dates[1].month!=12:
        imon= tgt_dates[0].month-1
        emon= tgt_dates[1].month-12
        outdata= outdata[imon:emon] if emon<0 else outdata[imon:]

    return outdata

if __name__ == "__main__":
    main()
