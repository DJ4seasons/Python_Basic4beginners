'''
Dealing with missing data in Numpy

1. Using arbitrary number
2. Using NaN
3. Using Masked Array

By Daeho Jin
'''

import numpy as np

def show_array_info(a,show_contents=True):
   """
   Print information of numpy array
   """
   result="N_Dims={}, Shape={}, Data_Type={}".format(a.ndim, a.shape, a.dtype)
   print(result)
   if show_contents:
      print(a)
   return

###--- Start
print('\nBefore start, define a sample array first')
print('''arr0= np.arange(12)
arr0= np.reshape(arr0, [3,4]''')
arr0= np.arange(12, dtype=float)
arr0= np.reshape(arr0, [3,4])
show_array_info(arr0)

print("\n1. Using an arbitrary number to represent missings")
print("\n1-1. Set an array with missings")
print("""undef= -999.9
arr1= np.copy(arr0)
missing_loc= ([0,2],[1,2])  # (axis0_indices, axis1_indices)
arr1[missing_loc]= undef
""")
undef= -999.9
arr1= np.copy(arr0)
missing_loc= ([0,2],[1,2])
arr1[missing_loc]= undef
show_array_info(arr1)

print("""
### Check number of missings
ms_idx= arr1==undef
print(ms_idx.sum())""")
ms_idx= arr1==undef
print(ms_idx.sum())

print("\n1-2. Calculate mean for axis1")
print("""no_ms_idx= np.logical_not(ms_idx)
mean1= np.average(arr1, weights=no_ms_idx, axis=1)
""")
no_ms_idx= np.logical_not(ms_idx)
mean1= np.average(arr1, weights=no_ms_idx, axis=1)
show_array_info(mean1)

print("\n1-3. Normalize by total sum")
print("""norm1= np.copy(arr1)
norm1[no_ms_idx]= norm1[no_ms_idx]/norm1[no_ms_idx].sum()
""")
norm1= np.copy(arr1)
norm1[no_ms_idx]= norm1[no_ms_idx]/norm1[no_ms_idx].sum()
show_array_info(norm1)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2. Using NaN (Not a Number) to represent missings")
print("\n2-1. Set an array with missings")
print("""undef= np.nan
arr1= np.copy(arr0)
missing_loc= ([0,2],[1,2])  # (axis0_indices, axis1_indices)
arr1[missing_loc]= undef
""")
undef= np.nan
arr2= np.copy(arr0)
missing_loc= ([0,2],[1,2])
arr2[missing_loc]= undef
show_array_info(arr2)

print("""
### Check number of missings
ms_idx= np.isnan(arr2)
print(ms_idx.sum())""")
ms_idx= np.isnan(arr2)
print(ms_idx.sum())

input("\nPress Enter to continue...\n")
print("\n2-2. Calculate mean for axis1")
print("""mean2= np.nanmean(arr2, axis=1)
""")
mean2= np.nanmean(arr2, axis=1)
show_array_info(mean2)

print("""
### For comparison,
mean2b= np.average(arr2, weights=~ms_idx, axis=1)
print(mean2b)""")
mean2b= np.average(arr2, weights=~ms_idx, axis=1)
print(mean2b)

print("\n2-3. Normalize by total sum")
print("""norm2= np.copy(arr2)/np.nansum(arr2)
show_array_info(norm2)
""")
norm2= np.copy(arr2)/np.nansum(arr2)
show_array_info(norm2)

print("""
### Other NaN related functions
np.nan_to_num()
np.nanargmax(), np.nanargmin()
np.nancumsum(), np.nancumprod()
np.nanmin(), np.nanmax(), np.nanmedian()
np.nanpercentile(), np.nanquantile()
np.nansum(), np.nanprod()
np.nanstd(), np.nanvar()

### Also check other extreme values
np.isinf()
np.isfinite()
...
""")

input("\nPress Enter to continue...\n")
print("""### One advantage of using nan
import matplotlib.pyplot as plt
plt.imshow(norm2)
plt.colorbar() # colorbar 그리기
plt.show()
""")
import matplotlib.pyplot as plt
plt.imshow(norm2)
plt.colorbar() # Draw colorbar
plt.show()

print('"Matplotlib" automatically identify NaN as an missing data!!!')

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n3. Using Masked Array module")
print("\n3-1. Create a masked array")
print("""arr3= np.ma.masked_where(ms_idx,arr0)
show_array_info(arr3)
""")
arr3= np.ma.masked_where(ms_idx,arr0)
show_array_info(arr3)

print("""
### This is also same:
arr3= np.ma.array(arr0, mask=ms_idx)
""")
arr3= np.ma.array(arr0, mask=ms_idx)
show_array_info(arr3)

print("""
### Show mask
print(arr3.mask)""")
print(arr3.mask)

print("""
### Also available various functions to make masked array
np.ma.masked_greater(x, value[, copy])
np.ma.masked_less_equal(x, value[, copy])
np.ma.masked_outside(x, v1, v2[, copy])
...
""")

input("\nPress Enter to continue...\n")
print("\n3-2. Calculate mean for axis1")
print("""mean3= np.ma.mean(arr3, axis=1)
### 'arr3.mean(axis=1)' also produce the same result
""")
mean3= np.ma.mean(arr3, axis=1)
show_array_info(mean3)

print("\n3-3. Normalize by total sum")
print("""norm3= np.ma.copy(arr3)/arr3.sum()
show_array_info(norm3)
""")
norm3= np.ma.copy(arr3)/arr3.sum()
show_array_info(norm3)

print('''
### Be Caution: "np.copy" makes different result!
norm3b= np.copy(arr3)/arr3.sum()
show_array_info(norm3b)''')
norm3b= np.copy(arr3)/arr3.sum()
show_array_info(norm3b)

input("\nPress Enter to continue...\n")

print("\n3-4. Back to numpy array")
print("""
### If want to keep dimension:
show_array_info(arr3.filled(fill_value=np.nan))""")
show_array_info(arr3.filled(fill_value=np.nan))

print("""
### If want to remove missings:
show_array_info(arr3.compressed())""")
show_array_info(arr3.compressed())


print("""
3-5. Other functions for masked array

### There are quite various functions available for masked array
### Check https://numpy.org/doc/stable/reference/routines.ma.html
""")

input("\nPress Enter to continue...\n")
print("""### One advantage of using masked array
#import matplotlib.pyplot as plt
plt.clf()  # Delete previuos figure drawn above
plt.imshow(norm3)
plt.colorbar() # colorbar 그리기
plt.show()
""")
#import matplotlib.pyplot as plt
plt.clf()
plt.imshow(norm3)
plt.colorbar() # Draw colorbar
plt.show()

print('"Matplotlib" naturally works with masked array!!!')

print("\nTHE END: Dealing with missings with Numpy\n")
