"""
t-test example

Note: Welch's t-test
Welch's t-test is to test if two populations have equal means.
Welch's t-test is more reliable when the two samples have unequal variance and/or unequal sample size.
https://en.wikipedia.org/wiki/Welch%27s_t-test

---
Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Binary data file(HadISST) was produced by D04 code
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

Daeho Jin

---
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind_from_stats.html
"""

import sys
import os.path
import numpy as np

from scipy import stats

import V00_Functions as vf

def main():
    ### Get Nino3.4 Index
    yrs= [2014,2021]  # Starting year and ending year
    #Nino4 (5N-5S, 160E-150W) [160,210,-5,5]
    #Nino3.4 (5N-5S, 170W-120W) [-170,-120,-5,5]
    nn34= vf.get_sst_areamean_from_HadISST([-170,-120,-5,5],yrs,remove_AC=True)
    ### And other region
    tio= vf.get_sst_areamean_from_HadISST([240,280,-10,0],yrs,remove_AC=True)
    spo= vf.get_sst_areamean_from_HadISST([-170,-120,-40,-30],yrs,remove_AC=True)

    data= [nn34, tio, spo]
    var_names= ['Ni{}o3.4'.format('\u00F1'), 'Trop_IO', 'S_Pacific']

    dof1= [vf.get_Eff_DOF(ts,is_ts1_AR1=True,adjust_AR1=True) for ts in data]
    dof2= [vf.get_Eff_DOF(ts,is_ts1_AR1=False) for ts in data]

    get_stat= lambda ts, dof: [ts.mean(), ts.std(ddof=1), dof]

    print("\n{} vs. {}".format(var_names[0], var_names[1]))
    t1,p1= stats.ttest_ind_from_stats(*get_stat(data[0],dof1[0]), *get_stat(data[1],dof1[1]), equal_var=False)
    t2,p2= stats.ttest_ind_from_stats(*get_stat(data[0],dof2[0]), *get_stat(data[1],dof2[1]), equal_var=False)
    print("DoF1= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(dof1[0], dof1[1], t1, p1))
    print("DoF2= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(dof2[0], dof2[1], t2, p2))

    print("\n{} vs. {}".format(var_names[0], var_names[2]))
    t1,p1= stats.ttest_ind_from_stats(*get_stat(data[0],dof1[0]), *get_stat(data[2],dof1[2]), equal_var=False)
    t2,p2= stats.ttest_ind_from_stats(*get_stat(data[0],dof2[0]), *get_stat(data[2],dof2[2]), equal_var=False)
    print("DoF1= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(dof1[0], dof1[2], t1, p1))
    print("DoF2= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(dof2[0], dof2[2], t2, p2))

    return

if __name__ == "__main__":
    main()
