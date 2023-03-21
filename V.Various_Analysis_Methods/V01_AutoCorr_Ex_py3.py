"""
Calculate auto-correlation of Nino3.4 and SST indices (area mean)

Simple method using auto-covariance is implmented in V00_Functions.
If want to use FFT method, try statsmodels.tsa.stattools.acf()

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

import V00_Functions as vf


def main():
    ### Get Nino3.4 Index
    yrs= [2015,2020]  # Starting year and ending year
    #Nino3.4 (5N-5S, 170W-120W) [-170,-120,-5,5]
    nn34= vf.get_sst_areamean_from_HadISST([-170,-120,-5,5],yrs,remove_AC=True)
    ### And other region
    tio= vf.get_sst_areamean_from_HadISST([240,280,-10,0],yrs,remove_AC=True)
    spo= vf.get_sst_areamean_from_HadISST([-170,-120,-40,-30],yrs,remove_AC=True)

    ### Calculate AC
    nlags= min(len(nn34)-1,100)  ## Prevent too long record
    ac_nn34,xx= vf.acf(nn34,nlags=nlags)
    data=[ac_nn34,]+[vf.acf(ts1)[0] for ts1 in [tio,spo]]
    vnames=['Ni\u00F1o3.4','Trop. IO','S. Pacific']

    ## Add AR1 example
    ar1= [ac_nn34[1]**val for val in xx]
    data.append(ar1)
    vnames.append(vnames[0]+'_AR(1)')
    ## Adjusted AR1
    ac1= []
    for k in range(1,25,1):
        if ac_nn34[k]<0.05:
            break
        else:
            ac1.append(ac_nn34[k]**(1/k))
    #print(ac1)
    ac1= np.array(ac1).mean()
    ar2= [ac1**val for val in xx]
    data.append(ar2)
    vnames.append(vnames[0]+'_AR(1)\nAdjusted')

    ###---
    ### Plotting setup
    ###---
    fig=plt.figure()
    fig.set_size_inches(6.4,5)  ## (xsize,ysize)

    ###--- Suptitle
    suptit="Auto-correlation Example [HadISST, 2015-20]"
    fig.suptitle(suptit,fontsize=15,y=0.94,va='bottom',stretch='semi-condensed')

    ax1= fig.add_subplot(111)
    sub_tit= ''
    props= dict(lw=2,alpha=0.8)
    simple_plot(ax1,xx,data,vnames,sub_tit,props)

    ### Show or save
    outdir= '../Pics/'
    out_fig_nm= outdir+'V01.autocorr_example.SST_AM+Nino34.png'
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(out_fig_nm,dpi=150,bbox_inches='tight')   # dpi: pixels per inch
    print(out_fig_nm)
    plt.show()
    return


def simple_plot(ax,xx,data,vnames,subtit,props=dict()):

    if not isinstance(data,list):
        data= [data,]

    ### Plot
    for d,vn in zip(data,vnames):
        ls='--' if 'AR' in vn else '-'
        ac= ax.plot(xx,d,label=vn,ls=ls,**props)

    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)

    ### Zero lines
    ylim= ax.get_ylim()
    if ylim[0]*ylim[1]<0:
        ax.axhline(y=0.,ls='-',lw=0.8,c='k')
    ## Reference for e-folding time
    ax.axhline(y=1/np.exp(1),ls='--',lw=2,c='0.6')

    ### Misc
    ax.legend(loc='upper right',fontsize=11)
    ax.set_xlabel('Lags in months',fontsize=12)
    ax.set_ylabel('Correlation Coeff.',fontsize=12)
    ax.tick_params(axis='both',labelsize=10)
    ax.grid(axis='x',ls='--',lw=0.8,c='0.2')

    return

if __name__ == "__main__":
    main()
