# Python_Basic4beginners
Educational Code Examples for Getting Used to Python3   
: Numpy, Matplotlib, Cartopy, etc. for Earth Science Students and Researchers

## Python Installation
For most systems of Windows, Mac OSX, Linux, "Conda" is recommended.

Full version: [ANACONDA](https://www.anaconda.com/products/individual)  
Custom version: [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

(Most Linux systems may have python pre-installed; then "pip" command can manage package installation/update)  
(Test: type "python" or "python3" in the command window)  

## Python (and packages) Version Info (July 2021)
Current version for code testing (recommended minimum version)  
python:     3.8.10  (3.5+)  
matplotlib: 3.4.2   (3.2+)  
cartopy:    0.19    (0.18+)  
numpy:      1.20    (1.17+)  
scipy:      1.6.3   (1.4+)  

To check the version, type the command "conda list" (for conda system) or "pip list"  

## Python package/module installation
For conda system, search keywords, "cond install cartopy" (or any other package name). Then, it leads to https://anaconda.org/conda-forge/cartopy where the command is shown as "conda install -c conda-forge cartopy"  

For custom installation, use command "pip" (or pip3); e.g., "pip install cartopy"  

## Python package/module update
For conda system, type "conda update <package_name>"  
  - For Anaconda system, type "conda update all" for update all available packages/modules  

For systems working with pip, type "pip install <package_name> --upgrade"  

If your computer already had Anaconda, and it is not going to update cartopy to 0.18+, the conda needs to be removed and re-installed with newest download.

All packages/modules used in the codes
---
   
```
import sys
import numpy as np
import os
import glob

from subprocess import run
from pyhdf.SD import SD, SDC
import h5py
from netCDF4 import Dataset

import matplotlib
import cartopy

import scipy
from sklearn import linear_model

### Optionally,
import xarray
```

## Recommended syllabus 
1. Level 0
   - A. Basic_Python
2. Level 1
   - C. Basic_Numpy
   - M. Matplotlib_Basic_Setup
   - N. Matplotlib_Basic_Plus 
   - Optionally, B. Python_replacing_shell_script
3. Level 2
   - D. Read_Write_Text+Binary_file
   - E. Read_Write_NetCDF+HDF_file
   - F. Datetime_and_Time_Series
   - O. Matplotlib_Application+Cartopy
4. Level 3
   - V. Various_Analysis_Methods

##

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

<p align="center">
  <img src="https://github.com/DJ4seasons/Python_Basic4beginners/blob/master/Book_Cover.jpg" width="640" title="Book Covers">
</p>

