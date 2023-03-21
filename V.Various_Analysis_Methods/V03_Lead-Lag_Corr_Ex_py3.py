"""
Calculate lead-lag correlation of Nino3.4 and SST indices (area mean)

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

    maxlag=7  # in months

    ax1= fig.add_subplot(211)
    sub_tit= '(a) Ni{}o3.4 vs. TIO'.format('\u00F1')
    data=[nn34,tio]
    vnames=['Ni{}o3.4'.format('\u00F1'),'TIO']
    llcorr_plot(ax1,data,vnames,sub_tit,maxlag=maxlag)

    ax1= fig.add_subplot(212)
    sub_tit= '(b) Ni{}o3.4 vs. SPO'.format('\u00F1')
    data=[nn34,spo]
    vnames=['Ni{}o3.4'.format('\u00F1'),'SPO']
    llcorr_plot(ax1,data,vnames,sub_tit,maxlag=maxlag)

    ### Show or save
    outdir= '../Pics/'
    out_fig_nm= outdir+'V03.llcorr_example.SST_AM+Nino34.png'
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(out_fig_nm,dpi=150,bbox_inches='tight')   # dpi: pixels per inch
    print(out_fig_nm)
    plt.show()
    return

def llcorr_plot(ax,data,vnames,subtit,maxlag=5):

    if not isinstance(data,list) or len(data)!=2:
        sys.exit("'data' should have two 1-d time series")

    tlag= np.arange(-maxlag,maxlag+1,1)
    ccoef,pvals= llcorr(*data,tlag)
    print(ccoef)
    ### Lead-Lag Corr plot
    llc= ax.plot(tlag,ccoef,color='k',lw='1.5')
    ##-- Mark significant values
    ccoef[pvals>0.05]=np.nan  # Masking if p value is too large (now 95% level)
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

def llcorr(ts1,ts2,tlag):
    import scipy.stats as st
    def get_cdf_of_beta_distribution(nn,val):
        '''
        Beta distribution is used to calculate p-value of correlation coefficient
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html

        This is actually same to this way:
        t= r*np.sqrt(Neff-2)/np.sqrt(1-r**2)  where r= corr. coef.
        p= scipy.stats.t.sf(np.abs(t),Neff-2)
        '''
        dist = st.beta(nn/2 - 1, nn/2 - 1, loc=-1, scale=2)
        return dist.cdf(-abs(val))

    ###---
    N= len(ts1)
    Neff= vf.get_Eff_DOF(ts1,ts2)

    coef,pp = [], []
    for it in tlag:
        if it<0:
            cc=np.corrcoef(ts1[:it],ts2[-it:])[0,1]
        elif it>0:
            cc=np.corrcoef(ts1[it:],ts2[:-it])[0,1]
        else:
            cc=np.corrcoef(ts1,ts2)[0,1]

        coef.append(cc)
        new_dof= Neff-2-abs(it)
        pp.append(get_cdf_of_beta_distribution(new_dof,cc)*2)  # two-tailed
    return np.asarray(coef), np.asarray(pp)

if __name__ == "__main__":
    main()
