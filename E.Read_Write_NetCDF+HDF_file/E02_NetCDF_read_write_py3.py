"""
Read CCMP 6-hrly netCDF file and write daily mean

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

"""


import sys
import os.path
import numpy as np
from datetime import datetime
from netCDF4 import Dataset, date2num
import E01_NetCDF_file_header_info_py3 as nc_check

def main():
    ###--- Parameters
    tgt_date= datetime(2019,1,1)
    date_str= tgt_date.strftime('%Y%m%d')
    #date_str= '{}{:02d}{:02d}'.format(2019,1,1)

    indir = '../Data/'
    #CCMP_Wind_Analysis_20190101_V02.0_L3.0_RSS.nc
    infn= indir+'CCMP_Wind_Analysis_{}_V02.0_L3.0_RSS.nc'.format(date_str)

    vars = ['longitude','latitude','uwnd', 'vwnd']

    f_id= nc_check.open_netcdf(infn)

    lons = f_id.variables[vars[0]]     # No slicing
    lats = f_id.variables[vars[1]][:]  # Slicing
    print(type(lons), lons.shape, type(lats), lats.shape)
    ### By slicing, netCDF_variable object changes to numpy.MaskedArray
    lons = lons[:]
    print(type(lons))

    ### It's also possible to pull out data by one line
    data= [f_id.variables[vv][:] for vv in vars]

    ### Check dimension of uwnd and vwnd
    print(data[vars.index('uwnd')].shape, data[vars.index('vwnd')].shape)

    ### Calculate daily mean
    for i, vn in enumerate(['uwnd','vwnd']):
        idx= vars.index(vn)
        data[idx]= data[idx].mean(axis=0)

    ### Create a netcdf file
    outdir= indir
    outfn= outdir+'CCMP_Wind_Analysis_{}_V02.0_L3.0_RSS.daily.nc'.format(date_str)
    ncfw= Dataset(outfn, "w", format="NETCDF4")

    ## Dimensions
    ln= ncfw.createDimension(vars[0],data[0].shape[0])  # Define a dim of container
    lt= ncfw.createDimension(vars[1],data[1].shape[0])
    times= [tgt_date,]
    tm= ncfw.createDimension('time',len(times))

    lonnc= ncfw.createVariable(vars[0],'f4',(vars[0],))  # Create a container
    latnc= ncfw.createVariable(vars[1],'f4',(vars[1],))
    timenc= ncfw.createVariable('time','f8',('time',))

    lonnc[:], latnc[:]= data[0].astype(np.float32), data[1].astype(np.float32)  # Assign values to container
    lonnc.units, latnc.units= 'degrees_east', 'degrees_north'
    timenc.units = 'hours since 0001-01-01 00:00:00.0'
    timenc.calendar = 'gregorian'
    timenc[:] = date2num(times, timenc.units, calendar=timenc.calendar)

    ## Data variables
    undef= -999.9
    uwndnc= ncfw.createVariable(vars[2],'f4',('time',vars[1],vars[0]))
    # Useful options of createVariable()
    # zlib=True, complevel=N  # N= 1 being fastest, 9 being best compression ratio
    # fill_value= val or False # val for overriding default _FillValue, and False for disabling
    # https://unidata.github.io/netcdf4-python/#Dataset.createVariable
    uwndnc[:]= data[2] ## It can accept masked array

    vwndnc= ncfw.createVariable(vars[3],'f4',('time',vars[1],vars[0]),fill_value= undef)
    vwndnc[:]= data[3].filled(fill_value=undef)  ## Change masked array to ndarray with fill_value
    # <-- Identify missing cells of ndarray by given "fill_value" option

    uwndnc.units, vwndnc.units= [f_id.variables[vv].units for vv in vars[2:]]

    ## Attributions
    ncfw.description = 'Daily mean of CCMP winds'

    ## Close file
    print("{} is written.\n".format(outfn))
    ncfw.close()

    ## Test the written netcdf file
    test= True
    if test:
        nc_f= nc_check.open_netcdf(outfn)
        nc_check.print_netcdf_details(nc_f)

        uwnd= nc_f.variables['uwnd'][:].squeeze()
        vwnd= nc_f.variables['vwnd'][:].squeeze()
        nc_f.close()

        check_data_imshow(np.sqrt(uwnd**2+vwnd**2))

    return

def check_data_imshow(arr2d, origin='lower'):
    import matplotlib.pyplot as plt
    plt.imshow(arr2d, origin=origin)
    plt.colorbar()
    plt.show()
    return

if __name__ == "__main__":
    main()
