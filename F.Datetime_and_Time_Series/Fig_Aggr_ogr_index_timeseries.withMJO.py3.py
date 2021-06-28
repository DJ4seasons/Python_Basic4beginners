"""
# 
# Draw timeseries of aggregation organization idnexes
# : COP, SCAI, MCAI, Iorg  ==> COP, Iorg, COPv2, COPv3, COPv4 in version 3
# 
# Daeho Jin, 2020.11.16
#
"""

import numpy as np
import sys
import os.path
from datetime import timedelta, date
from itertools import repeat

def bin_file_read2mtx(fname,dtp=np.float32):
    """ Open a binary file, and read data 
        fname : file name
        dtp   : data type; np.float32 or np.float64, etc. """

    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    with open(fname,'rb') as fd:
        bin_mat = np.fromfile(file=fd,dtype=dtp)

    return bin_mat

def yield_date_range(start_date, end_date, tdelta=1):
    ### Including end date
    for n in range(0,int((end_date - start_date).days)+1,tdelta):
        yield start_date + timedelta(n)

def running_mean(x, N):
    """
    Calculate running mean with "Cumulative Sum" function, asuming no missings
    Ref: https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    Input x: 1-d numpy array of time series
    Input N: Running Mean period
    Return: Same dimension with x; end points are averaged for less than N values
    """
    cumsum= np.cumsum(np.insert(x, 0, 0))
    new_x= (cumsum[N:] - cumsum[:-N]) / float(N)  ### Now it's running mean of [dim(x)-N] size
    pd0= N//2; pd1= N-1-pd0  ### Padding before and after. If N=5: pd0=2, pd1=2
    head=[]; tail=[]
    for i in range(pd0):
        head.append(x[:i+N-pd0].mean())
        tail.append(x[-i-1-pd1:].mean())
    new_x= np.concatenate((np.asarray(head),new_x,np.asarray(tail)[::-1][:pd1]))
    return new_x

def read_mjoidx_text(fname,date_range=[]):
    """
    Read RMM or OMI Index Text file
    fname: include directory
    date_range: start and end dates, including both end dates, optional
    """
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

    print("Total RMM data record=",len(strs))
    return np.asarray(time_info),np.asarray(pcs),np.asarray(strs) ### Return as Numpy array

def get_filtered_strs(pc1,pc2):
    """
    Based on RMM index, 
    if pc1>=0: np.sqrt(pc1**2+pc2**2)
    if pc1<0: max(abs(pc2)+pc1,0)
    """
    strs= np.sqrt(pc1**2+pc2**2)
    idx= pc1<0
    strs[idx]= np.maximum(np.absolute(pc2[idx])+pc1[idx],0)
    return strs

def read_data(infnm_header,tgt_rg_name,var_name,nv_select=[]):
    nvars= len(var_name)  # Number of indices
    ww= infnm_header.split('_')[-1]
    ndy= int(ww.split('d')[0])
    nt_per_day= int(ww.split('x')[1])
    
    infnm= infnm_header+'.in{}.float32dat'.format(tgt_rg_name)
    data= bin_file_read2mtx(infnm).reshape([ndy,nt_per_day,nvars])
    if len(nv_select)>0:
        data= data[:,:,nv_select]
        var_name= [var_name[i] for i in nv_select]
                
    return data, var_name

def main():
    ###--- Parameters

    #nelemc=42; nelem=nelemc+nelemp
    #indir='/discover/nobackup/djin1/Precip-Cloud/PMM2020/Core_CR_vs_CPR/Data/'
    indir='/Users/djin1/Documents/CLD_Work/Data_Aggr/'

    nvars=5
    nprd= 5; nprd2=21
    mjo_idx=1  ## 0:RMM, 1:OMI

    mjo_idx_nm= ['RMM','OMI']
    mjo_idx_fn= ['rmm.74toRealtime.txt','omi.79toRealtime.txt']

    ###--- Parameters
    rg,nelemp,prwt,km= 15, 6, 7, 19 #map(int,sys.argv[1:5])
    tgtcr= '12' #sys.argv[5]
    #print("IC: ",rg,nelemp,km,prwt,tgtcr)
    set_nm = 'TCPR{}_pr{}x{}_prd'.format(tgtcr,nelemp,prwt)
    print(set_nm)

    ### Target environment
    nt_per_day=48

    date_range=[date(2014,1,1),date(2020,6,30)] 
    date_name=[d.strftime('%Y%m%d') for d in date_range]
    ndy=(date_range[1]-date_range[0]).days+1
    tgt_dates= (date_range[0],date(2020,2,7)) #Due to limit of OMI
    ndays=(tgt_dates[1]-tgt_dates[0]).days+1
    itidx= (tgt_dates[0]-date_range[0]).days

    #var_name= ['COP','SCAI','MCAI','I_org']
    var_name= ['COP','I_org','MCOP1','MCOP2','MCOP3','MCOP4']
    #nv_select= [0,1,2,3]
    nv_select= [2,3,4,5]
    nvars= len(var_name)
    nv_fn= ''.join(list(map(str,nv_select)))
    
    indir = '/Users/djin1/Documents/CLD_Work/Data_Aggr/Org_Indices/'
    infnm_header= indir+'Aggr_org_indices_v6.{}.{}-{}_{}dx{}x{}'.\
        format(set_nm,date_name[0],date_name[1],ndy,nt_per_day,nvars)

    tgt_rg= [((50,90,-20,20),'TIO'),
             ((95,145,-15,15),'MC'),
             ((150,190, -20,20),'WTP'),
             ((-80,-40,-25,15),'AMZ')]

    tgt_rg_idx= 0
    tgt_rg_bound, tgt_rg_name1 = tgt_rg[tgt_rg_idx]
    lst_factor1= (tgt_rg_bound[0]+tgt_rg_bound[1])/2/15
    print(tgt_rg_name1, tgt_rg_bound)
    data1, var_name1= read_data(infnm_header,tgt_rg_name1,var_name,nv_select)
    nvars= len(var_name1)
    
    tgt_rg_idx= 1
    tgt_rg_bound, tgt_rg_name2 = tgt_rg[tgt_rg_idx]
    lst_factor2= (tgt_rg_bound[0]+tgt_rg_bound[1])/2/15
    print(tgt_rg_name2, tgt_rg_bound)
    data2, _= read_data(infnm_header,tgt_rg_name2,var_name,nv_select)
    print(data1.shape)

    ###---
    #nyr= (ndy-itidx)//365
    #ndy2= 365*nyr//5
    ndy2= ndays//5
    data=[]
    for oidata in [data1,data2]:
        oidata= oidata[itidx:itidx+ndy2*5,:,:].reshape([ndy2,5*nt_per_day,nvars]).mean(axis=1)

        ### Change to filtered anomaly
        data.append([])
        for i in range(nvars):
            data[-1].append(running_mean(oidata[:,i],nprd)-running_mean(oidata[:,i],nprd2))
    
    times=[]
    for onedate in yield_date_range(tgt_dates[0]+timedelta(days=2),tgt_dates[1]-+timedelta(days=2),tdelta=5):
        times.append(onedate)
    nt=len(times)
    print(ndays,ndy2,oidata.shape,nt,data[-1][-1].shape)
    #sys.exit()

    ###---
    ### Read RMM data
    mjo_idx_dir='/Users/djin1/Documents/CLD_Work/Data_Obs/'
    mjo_fname= mjo_idx_dir+mjo_idx_fn[mjo_idx]
    _,pcs,_=read_mjoidx_text(mjo_fname,date_range=tgt_dates)
    print(pcs.shape) ### Check the dimension
    #if mjo_idx==0:
    pc1,pc2= pcs[:,0],pcs[:,1]
    #else:
    #    pc1,pc2= pcs[:,1],-pcs[:,0]

    pc1= pc1[:ndy2*5].reshape([ndy2,5]).mean(axis=1)
    pc2= pc2[:ndy2*5].reshape([ndy2,5]).mean(axis=1)

    ### Info needed for figure
    suptit="Aggr. Org. Indices({} to {}-Pentad Band-pass) vs. {} PCs".format(nprd,nprd2,mjo_idx_nm[mjo_idx])
    outdir = "../../Writing_OrgIdx/Pics/"
    fnout = outdir+"Aggr_org_indexes_ts_v6.{}.withMJO_in{}+{}.{}.png".format(set_nm,tgt_rg_name1,tgt_rg_name2,nv_fn)
    
    prset= dict(data=data, tgt_rg_name=(tgt_rg_name1,tgt_rg_name2), suptit=suptit, fnout=fnout, pcs=(pc1,pc2), var_names=var_name1, times=times)

    
    plot_main(prset)
    return

###---------
### Plot
###---------
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FuncFormatter
from matplotlib.dates import DateFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def plot_common(ax,subtit,yrange=[]):
    """
    Decorating time-series plot
    """
    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)

    ### Ticks and Grid
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ymin,ymax= ax.get_ylim()
    if ymin*ymax<0:  ### if y_range include 0, draw a horizontal line
        ym=max(-ymin,ymax)
        ax.set_ylim(-ym,ym)
        ax.axhline(y=0.,ls='--',c='0.3',lw=1)

    #ax.axvline(x=date(2014,6,1),ls='--',c='0.3',lw=1)
    #ax.axvline(x=date(2019,5,31),ls='--',c='0.3',lw=1)

    #else:
    #if ymax>5:
    #    ax.set_ylim(8,0)
    #elif len(yrange)==2:
    #    ax.set_ylim(*yrange)
    #else:
    #    space= (ymax-ymin)*0.15
    #    ax.set_ylim(ymin-space,ymax+space)
        
    ax.grid(axis='y',color='0.7', linestyle=':', linewidth=1)
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(axis='both',which='major',labelsize=10)
    ax.xaxis.set_major_formatter(DateFormatter("%b\n%Y"))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    return (ymin,ymax)

def plot_common2(ax,subtit):
    """
    Decorating time-series plot
    """
    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)

    ### Ticks and Grid
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.3))
    ymin,ymax= ax.get_ylim()
    if abs(ymin)>abs(ymax):
        ax.set_ylim(0.2,-0.5)
    else:
        ax.set_ylim(-0.2,0.5)
    ax.set_ylim(-0.76,0.76)
    xmin,xmax= ax.get_xlim()
    if xmax-xmin<=17:
        ax.xaxis.set_major_locator(MultipleLocator(2))
    else:
        ax.xaxis.set_major_locator(MultipleLocator(3))
        
    ax.grid(axis='both',color='0.7', linestyle=':', linewidth=1)
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(axis='both',which='major',labelsize=10)
    ax.axhline(y=0.,lw=0.7,c='k',ls='--')
    ax.axvline(x=0.,lw=0.7,c='k',ls='--')
    ww=subtit.split()
    ax.set_xlabel(' {} Leads (pentad)  <--->  {} Leads (pentad)'.format(ww[4],ww[2]),labelpad=2)
    return

import scipy.stats as st
from statsmodels.tsa.stattools import acf
def get_new_dof(ts1,ts2):
    N= len(ts1)
    for i,(val1,val2) in enumerate(zip(acf(ts1,nlags=len(ts1)-1),acf(ts2,nlags=len(ts2)-1))):
        if i==0:
            vsum= val1*val2
        else:
            vsum+= 2*(1-i/N)*val1*val2

    return N/vsum

def llcorr(ts1,ts2,npd2,index_range=[]):
    if len(index_range)==2:
        k0,k1= index_range
        if k1<0: k1=k1+len(ts1)
    else:
        k0,k1= 0,len(ts1)
        
    sample_rate=1
    tt= np.arange(-npd2,npd2+1,1)    
    coef,pp = [], []
    for it in tt:
        ishift= -(k0+it) if k0+it<0 else 0
        new_ts1= ts1[k0+ishift:k1+ishift:sample_rate]
        new_ts2= ts2[k0+it+ishift:k1+it+ishift:sample_rate]
        if len(new_ts1) != len(new_ts2):
            nt= min(len(new_ts1),len(new_ts2))
            new_ts1, new_ts2= new_ts1[:nt], new_ts2[:nt]
        coef.append(st.pearsonr(new_ts1,new_ts2)[0])
        nn= get_new_dof(new_ts1,new_ts2)
        dist = st.beta(nn/2 - 1, nn/2 - 1, loc=-1, scale=2)
        pp.append(2*dist.cdf(-abs(coef[-1])))
    return np.asarray(tt),np.asarray(coef),np.asarray(pp)

def plot_main(prset):
    data= prset['data']
    pc1,pc2 = prset['pcs']
    tgt_rg_names= prset['tgt_rg_name']
    times= prset['times']
    var_name= prset['var_names']

    ### Define Figure
    fig=plt.figure()
    fig.set_size_inches(9,10)  ## (xsize,ysize)

    ### Page Title
    suptit= prset['suptit']
    fig.suptitle(suptit,fontsize=16,y=0.97,va='bottom',stretch='semi-condensed')

    ### Parameters for subplot area
    left,right,top,bottom= 0.05, 0.95, 0.925, 0.05
    npnx,gapx,npny,gapy= 2, 0.03, 5, 0.075
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    abc='abcdefghij'
    cc=['#3454B4','#CC7000']

    props = dict(linestyle='-',linewidth=0.7,alpha=0.7)
    props2 = dict(linestyle='-',linewidth=1.5,alpha=0.9)

    ### Each panel for one variable and PC1/PC2
    id_range=[55,-2]
    times= times[id_range[0]:id_range[1]]
    for j,data1 in enumerate(data):
        for k,data0 in enumerate(data1):
            t0,r0,p0= llcorr(data0,pc1,11,index_range=id_range)
            t1,r1,p1= llcorr(data0,pc2,11,index_range=id_range)
    
            ax1=fig.add_axes([ix,iy-ly,lx,ly])
            ax1.plot(t0,r0,c=cc[0],label='PC1',**props2)  ### pc1 time-series
            ax1.plot(t1,r1,c=cc[1],label='PC2',**props2)  ### pc2 time-series
            subtit='({}) LLCorr {} vs. MJO PCs in {}'.format(abc[2*k+j],var_name[k],tgt_rg_names[j])

            r0[p0>0.1],r1[p1>0.1] = np.nan,np.nan
            ax1.plot(t0,r0,c=cc[0],marker='o',ls=None,fillstyle='none') #,label='90% Sig. Level')
            ax1.plot(t1,r1,c=cc[1],marker='o',ls=None,fillstyle='none') #,label='90% Sig. Level')

            r0[p0>0.05]=np.nan
            r1[p1>0.05]=np.nan
            ax1.plot(t0,r0,c=cc[0],marker='o')
            ax1.plot(t1,r1,c=cc[1],marker='o')
            plot_common2(ax1,subtit)
            
            if k==0:
                #ax1.legend(loc='upper left',bbox_to_anchor=(1.04,1.),borderaxespad=0.,fontsize=11)
                ax1.legend(loc='best',ncol=2,fontsize=10)
            if j==1:
                ax1.yaxis.tick_right()
                ax1.yaxis.set_label_position("right")
                ax1.yaxis.set_ticks_position('both')
    
            iy=iy-ly-gapy
        ix=ix+lx+gapx
        iy=top

    ###--- Save or Show
    #plt.show()
    fnout = prset['fnout']
    plt.savefig(fnout,bbox_inches='tight',dpi=150) ### Increase dpi for printing quality
    print(fnout)
    plt.show()
    return

if __name__=='__main__':
    main()


