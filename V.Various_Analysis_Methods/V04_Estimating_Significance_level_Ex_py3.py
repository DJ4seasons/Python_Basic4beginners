"""
Estimating significance level of correlation coefficients by bootstrap method

---
Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Binary data file(HadISST) was produced by D04 code
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

Daeho Jin
"""

import sys
import os.path
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from scipy.stats import norm

import V00_Functions as vf

def main():
    ### Get Nino3.4 Index
    yrs= [2015,2020]  # Starting year and ending year
    #Nino3.4 (5N-5S, 170W-120W) [-170,-120,-5,5]
    nn34= vf.get_sst_areamean_from_HadISST([-170,-120,-5,5],yrs,remove_AC=True)
    ### And other region
    tio= vf.get_sst_areamean_from_HadISST([240,280,-10,0],yrs,remove_AC=True)
    spo= vf.get_sst_areamean_from_HadISST([-170,-120,-40,-30],yrs,remove_AC=True)

    ###---
    ### Plotting setup
    ###---
    fig=plt.figure()
    fig.set_size_inches(6,8.5)  ## (xsize,ysize)
    fig.subplots_adjust(hspace=0.3)
    ###--- Suptitle
    suptit="Lead-Lag Correlation Example [HadISST,2015-20]"
    fig.suptitle(suptit,fontsize=15,y=0.95,va='bottom',stretch='semi-condensed')

    maxlag=7

    ax1= fig.add_subplot(211)
    sub_tit= '(a) Ni{}o3.4 vs. TIO'.format('\u00F1')
    data=[nn34,tio]
    vnames=['Ni{}o3.4'.format('\u00F1'),'TIO']
    corr_crt= estimate_significant_corr_coef(nn34,tio)[1]  # Choose 95% level
    llcorr_plot(ax1,data,vnames,sub_tit,maxlag=maxlag,corr_crt=corr_crt)

    ax1= fig.add_subplot(212)
    sub_tit= '(b) Ni{}o3.4 vs. SPO'.format('\u00F1')
    data=[nn34,spo]
    vnames=['Ni{}o3.4'.format('\u00F1'),'SPO']
    corr_crt= estimate_significant_corr_coef(nn34,spo)[1]  # Choose 95% level
    llcorr_plot(ax1,data,vnames,sub_tit,maxlag=maxlag,corr_crt=corr_crt)

    ### Show or save
    outdir= '../Pics/'
    out_fig_nm= outdir+'V04.estimate_corr_sig_level_example.SST_AM+Nino34.png'
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(out_fig_nm,dpi=150,bbox_inches='tight')   # dpi: pixels per inch
    print(out_fig_nm)
    plt.show()
    return

def llcorr_plot(ax,data,vnames,subtit,maxlag=5,corr_crt=-1):

    if not isinstance(data,list) or len(data)!=2:
        sys.exit("'data' should have two 1-d time series")

    tlag= np.arange(-maxlag,maxlag+1,1)
    ccoef= llcorr_simple(*data,tlag)

    ### Lead-Lag Corr plot
    llc= ax.plot(tlag,ccoef,color='k',lw='1.5')
    ##-- Mark significant values
    if corr_crt>0:
        ccoef[np.absolute(ccoef)<corr_crt]=np.nan  # Masking if p value is too large (now 95% level)
        llc2= ax.plot(tlag,ccoef,color='r',ls='',
                    marker='o',markersize=10,alpha=0.6)

    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)

    ### Zero lines
    ylim= ax.get_ylim()
    if ylim[0]*ylim[1]<0:
        ax.axhline(y=0.,ls='--',lw=1,c='k')
    ax.axvline(x=0.,ls='--',lw=1,c='k')

    ### Misc
    #ax.legend(loc='upper right',fontsize=11)
    ax.set_xlabel(' {} Lags   <--->  {} Lags    '.format(*vnames),fontsize=12)
    ax.set_ylabel('Correlation Coeff.',fontsize=12)
    ax.tick_params(axis='both',labelsize=10)
    ax.yaxis.set_major_locator(MultipleLocator(0.2))   # For Major Ticks
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks
    ax.grid(ls='--')
    return

def llcorr_simple(ts1,ts2,tlag):
    coef = []
    for it in tlag:
        if it<0:
            cc=np.corrcoef(ts1[:it],ts2[-it:])[0,1]
        elif it>0:
            cc=np.corrcoef(ts1[it:],ts2[:-it])[0,1]
        else:
            cc=np.corrcoef(ts1,ts2)[0,1]
        coef.append(cc)
    return np.asarray(coef)

def estimate_significant_corr_coef(ts1,ts2):

    N= len(ts1)
    Neff= vf.get_Eff_DOF(ts1,ts2)
    decorr_level= N/Neff
    niter= 2000  # Number of samples used for estimating

    ### Build index array
    len_ts1, count= 0, 0
    ts1_idx, n_samples= [0,], []
    while len_ts1<N-np.ceil(decorr_level):
        #nsample= np.rint(decorr_level*(count+1)-len(new_ts1)).astype(int)
        nsample= round(decorr_level*(count+1)-len_ts1)
        count+=1
        len_ts1+= nsample
        ts1_idx.append(len_ts1)
        n_samples.append(nsample)
    n_samples.append(N-len_ts1)
    #print(ts1_idx, n_samples); sys.exit()
    shuffle_idx= np.array(ts1_idx)

    ### Set-up random module
    rg = np.random.default_rng(123)  # Set seed number in order to repeat
    rg.shuffle(shuffle_idx)

    corrs=[]
    idx_k=0
    for i in range(niter):
        ### Shuffle by chunk
        new_ts1=[]
        for idx in shuffle_idx:
            m= n_samples[ts1_idx.index(idx)]
            new_ts1+=list(ts2[idx:idx+m])

        corrs.append(np.corrcoef(new_ts1,ts1)[0,1])
        rg.shuffle(shuffle_idx)

    corrs= np.asarray(corrs)
    #simple_check_distribution(corrs); sys.exit()

    ### Fisher transform:
    ### Transform pearsonr's beta distribution to normal distribution
    ### z= atanh(r); r= tanh(z)
    z= np.arctanh(corrs)
    print(z.mean(), z.std(ddof=1))
    #simple_check_distribution(z); sys.exit()

    ### For two-tail [0.9,0.95,0.975,0.99],  find [0.05,0.025,0.0125,0.005]
    z_sf= norm.ppf([0.05,0.025,0.0125,0.005],loc=z.mean(),scale=z.std(ddof=1))*-1
    ### Back to corr space to return
    print(z_sf, np.tanh(z_sf))
    return np.tanh(z_sf)

def simple_check_distribution(arr1d):
    fig=plt.figure()
    plt.hist(arr1d,bins=10,density=True)

    x= np.linspace(-1,1,100)
    plt.plot(x,norm.pdf(x,arr1d.mean(),arr1d.std(ddof=1)))
    plt.text(0.1,0.92,'mean= {:.2f}'.format(arr1d.mean()),transform=plt.gca().transAxes)
    plt.text(0.1,0.86,'std = {:.2f}'.format(arr1d.std(ddof=1)),transform=plt.gca().transAxes)
    plt.title('Distribution of Corr. Coef.')
    plt.show()
    return

if __name__ == "__main__":
    main()
