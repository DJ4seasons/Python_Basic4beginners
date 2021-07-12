"""
Read CCMP 6-hrly netCDF file and write daily mean with Xarray

By Daeho djin

---
Input file:
data/CCMP_Wind_Analysis_20190101_V02.0_L3.0_RSS.nc

Referece:
Wentz, F.J., J. Scott, R. Hoffman, M. Leidner, R. Atlas, J. Ardizzone, 2015:  Remote Sensing Systems Cross-Calibrated Multi-Platform (CCMP) 6-hourly ocean vector wind analysis product on 0.25 deg grid, Version 2.0, [indicate date subset, if used]. Remote Sensing Systems, Santa Rosa, CA. Available online at www.remss.com/measurements/ccmp

Acknowledgement:
Ricciardulli, Lucrezia & National Center for Atmospheric Research Staff (Eds). Last modified 27 Feb 2017. "The Climate Data Guide: CCMP: Cross-Calibrated Multi-Platform wind vector analysis." Retrieved from https://climatedataguide.ucar.edu/climate-data/ccmp-cross-calibrated-multi-platform-wind-vector-analysis.

Source:
http://data.remss.com/ccmp/v02.0/Y2019/M01/

---

Xarray can handle netcdf4/hdf5, GRIB, GeoTIFF, and many more.
http://xarray.pydata.org/en/stable/user-guide/io.html

Introduction to Xarray can be found here:
http://xarray.pydata.org/en/stable/user-guide/terminology.html
"""


import sys
import os.path
import numpy as np
from datetime import datetime
#from netCDF4 import Dataset, date2num
import xarray as xr
import E01_NetCDF_file_header_info_py3 as nc_check

def main():
    ###--- Parameters
    tgt_date= datetime(2019,1,1)
    date_str= tgt_date.strftime('%Y%m%d')
    #date_str= '{}{:02d}{:02d}'.format(2019,1,1)

    indir = '../Data/'
    #CCMP_Wind_Analysis_20190101_V02.0_L3.0_RSS.nc
    infn= indir+'CCMP_Wind_Analysis_{}_V02.0_L3.0_RSS.nc'.format(date_str)

    # Open as Xarray Dataset including several DataArrays
    ds = xr.open_dataset(infn,mask_and_scale=True)  # Default engine='netcdf4'
    print(ds)

    ### Method 1: smae procedure to all variables
    ds_day= ds.resample(time="1D").mean()
    fn_out1= infn[:-2]+'daily_xarray_method1.nc'
    ds_day.to_netcdf(fn_out1,format="NETCDF4")
    # For compression,
    # encoding={var_name:{"zlib": True, "complevel": N}}
    '''
    ### Method 2: DataArray of each variable is dealt
    vars = ['uwnd', 'vwnd']
    new_da= []
    for key in vars:
        da= ds[key].mean(axis=0)  # axis0: Time; 6-hrly to daily
        print(type(da), da.coords)
        da= da.expand_dims(dim= dict(time= [np.datetime64(tgt_date)]),axis=0)
        print(da.coords)
        new_da.append(da)
        # FYI, resample() can be applied to DataArray, too.
        # If resample() is used, no need the expand_dims().
    ds_day2= xr.merge(new_da)  #new_da[0].to_dataset()
    print(ds_day2)
    fn_out2= infn[:-2]+'daily_xarray_method2.nc'
    ds_day2.to_netcdf(fn_out2,format='NETCDF4')

    ### Method 3: Building from scratch
    vars = ['uwnd', 'vwnd','latitude','longitude']
    new_arr= []
    for key in vars:
        arr= ds[key].to_masked_array()
        print(type(arr), arr.shape)
        if 'wnd' in key:
            arr= arr.mean(axis=0)  # Convert to daily
            arr= arr.reshape([1,*arr.shape])  # axis0 is necessary for time dimension
        new_arr.append(arr.filled(fill_value=np.nan))  # NaN is default fill value of Xarray

    ds_day3= xr.Dataset(
                {
                vars[0]: (('time',vars[2],vars[3]),new_arr[0]),
                vars[1]: (('time',vars[2],vars[3]),new_arr[1]),
                },
                coords= {
                    'time': [np.datetime64(tgt_date),],
                    vars[2]: new_arr[2],
                    vars[3]: new_arr[3],
                    },
                )
    print(ds_day3)

    fn_out3= infn[:-2]+'daily_xarray_method3.nc'
    ds_day3.to_netcdf(fn_out3,format='NETCDF4')
    '''
    ### Check the output
    outfn= fn_out1
    nc_f= nc_check.open_netcdf(outfn)
    nc_check.print_netcdf_details(nc_f)

    return

if __name__ == "__main__":
    main()
