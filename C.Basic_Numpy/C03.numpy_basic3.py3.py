'''
Numpy Basic(3)
2. characteristics of numpy array
2-4. Concatenated application of numpy functions
2-5. In-place operation

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
print("\n2. characteristics of numpy array")
print("\n2-4. Concatenated application of numpy functions")

print('\nFirst define sample array')
print('''arr1= np.arange(24)
arr1= np.reshape(arr1, [4,6]''')
arr1= np.arange(24)
arr1= np.reshape(arr1, [4,6])
show_array_info(arr1)

print("\n# We already saw that below two lines produce the same result.")
print("# arr1= np.reshape(arr1, [4,6])")
print("# arr1= arr1.reshape([4,6])")
print('''
# This is because 'reshape' is a numpy function as well as a method of numpy array class
# In the case of method of array, multiple methods can be concatenated.''')

print("\nExample: arr2= np.arange(24).reshape([4,6])")
arr2= np.arange(24).reshape([4,6])
print("Test if arr1 equals arr2 using 'np.array_equal()'")
print("Result of 'np.array_equal(arr1,arr2)' = {}".format(np.array_equal(arr1,arr2)))

print("\nExample of grid-degrading")
print("c= arr1.reshape([2,2,3,2]).swapaxes(1,2).reshape([2,3,4]).mean(axis=2)")
c= arr1.reshape([2,2,3,2]).swapaxes(1,2).reshape([2,3,4]).mean(axis=2)
show_array_info(c)

print("\nExample of calculating monthly anomaly")
print("Define new array: d= np.arange(120)")
d= np.arange(120)
print("ano= (d.reshape([-1,12]) - d.reshape([-1,12]).mean(axis=0).reshape([1,12])).reshape(-1)")
ano= (d.reshape([-1,12]) - d.reshape([-1,12]).mean(axis=0).reshape([1,12])).reshape(-1)
print("ano[:12] = {}".format(ano[:12]))
print("ano[-12:] = {}".format(ano[-12:]))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n2-5. In-place operation")

print("\nDefine new array: e= np.zeros([2,2])")
e= np.zeros([2,2])
show_array_info(e)

### Copy or not
print("""
Test1:
e2= e
e2[0,0]= 1
print(e)""")
e2= e
e2[0,0]= 1
print(e)

print("""
Test2:
e3= np.copy(e)
e3[0,1]= 2
print(e)""")
e3=np.copy(e)
e3[0,1]=2
print(e)

print("""
Test3:
e4= e[:]
e4[1,0]= 3
print(e)""")
e4= e[:]
e4[1,0]= 3
print(e)

print("""
Test4:
e4= e[1,:]
e4[1]=4
print(e)""")
e4= e[1,:]
e4[1]=4
print(e)

print("""
Test5: Define a function
def function1(arr):
    arr[0]=-1
    return
function1(e)
print(e)""")
def function1(arr):
    arr[0]=-1
    return
function1(e)
print(e)

print("""
# Remember: The assignment in python is just creating a pointer to the memory location.
# In numpy, please make sure that it is copied when necessary.
# Particularly be cautious when passing array to function(s).
#
# It is also interesting that, in the case of 'List,' '[:]' plays a role of copy, but not in numpy.
""")

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n2-6. Array transformation") # hsatck, vstack, ...



input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n . Random module examples")



input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n NaN and Masked Array")









'''
### Logical operation
np.logical_and()
np.logical_or()
np.logical_not()

### Expanding Array
np.repeat()
np.tile()
np.concatenate()
np.hstack()
np.vstack()
np.dstack()

### Simple statistical methods
np.dot()
np.max()
np.mean(); np.average()
np.min()
np.sum()
np.std()
np.var()
np.median()
np.cumsum()
np.corrcoef()
np.histogram()
np.digitize()
np.percentile()
np.sort()
np.partition()
...

### Argument methods
np.argmax() # Return index of maximum value
np.argmin()
np.argsort()
np.argpartition()

### Mathematical functions
np.sin()
np.cos()
np.around()
np.floor()
np.ceil()
np.power()
np.log()
np.exp()

### Checking data
np.isnan()
np.isinf()
np.isfinite()

### Treat NaN values
np.nan_to_num()
np.nansum()
np.nanmin()
np.nanargmin()
np.nanpercentile()
...

### https://docs.scipy.org/doc/numpy/reference/



'''
