"""
Calculate regression slopes between Nino3.4 and SST indices (area mean)

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
from scipy.stats import linregress

import V00_Functions as vf


def main():
    ### Get Nino3.4 Index
    yrs= [2015,2019]  # Starting year and ending year
    #Nino3.4 (5N-5S, 170W-120W) [-170,-120,-5,5]
    nn34= vf.get_sst_areamean_from_HadISST([-170,-120,-5,5],yrs)
    ### And other regions
    tio= vf.get_sst_areamean_from_HadISST([240,280,-10,0],yrs)
    spo= vf.get_sst_areamean_from_HadISST([-170,-120,-40,-30],yrs)

    ###---
    ### Plotting setup
    ###---
    fig=plt.figure()
    fig.set_size_inches(6,8.5)  ## (xsize,ysize)

    ###--- Suptitle
    suptit="Regr. of SST against Ni{}o3.4 [HadISST,2015-19]".format('\u00F1')
    fig.suptitle(suptit,fontsize=15,y=0.95,va='bottom',stretch='semi-condensed')
    fig.subplots_adjust(hspace=0.3)

    ax1= fig.add_subplot(211)
    sub_tit= '(a) Tropical Indian Ocean'
    scatter_and_regr_plot(ax1,nn34,tio,sub_tit)

    ax2= fig.add_subplot(212)
    sub_tit= '(b) South Pacific'
    scatter_and_regr_plot(ax2,nn34,spo,sub_tit)

    ### Show or save
    plt.show()

    outdir= '../Pics/'
    out_fig_nm= outdir+'V01.regression_example.SST_AMvsNino34.png'
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    #fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
    return

def scatter_and_regr_plot(ax,x,y,subtit):
    ### Scatter plot
    ax.scatter(x,y,c='0.4',s=10,marker='o',alpha=0.9)

    ### Regression
    slope,intercept,rvalue,pvalue,stderr= linregress(x,y)

    ##-- New coordinates for prediction
    new_x= np.linspace(x.min(),x.max(),100)
    prd= new_x*slope+intercept

    ##- Draw regression line
    rline= ax.plot(new_x,prd,c='k',lw=2,alpha=0.8)
    anntxt=r'$R^2={:.3f}$'.format(rvalue**2)
    anntxt2='Coef.={:.2f}'.format(slope)
    anntxt3='p_value={:.3f}'.format(pvalue)
    for i,atxt in enumerate([anntxt,anntxt2,anntxt3]):
        yloc= 0.92-i*0.07
        if slope>0:
            ax.annotate(atxt,xy=(0.02,yloc),xycoords='axes fraction',ha='left',fontsize=11,stretch='semi-condensed')
        else:
            ax.annotate(atxt,xy=(0.98,yloc),xycoords='axes fraction',ha='right',fontsize=11,stretch='semi-condensed')

    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)

    ### Misc
    ax.set_xlabel('Ni{}o3.4 anomaly'.format('\u00F1'),fontsize=12)
    ax.set_ylabel('SST anomaly',fontsize=12)
    ax.tick_params(axis='both',labelsize=10)

    ### Zero lines
    xlim= ax.get_xlim()
    if xlim[0]*xlim[1]<0:
        ax.axvline(x=0.,ls='--',lw=1)
    ylim= ax.get_ylim()
    if ylim[0]*ylim[1]<0:
        ax.axhline(y=0.,ls='--',lw=1)
    return

if __name__ == "__main__":
    main()
