'''
Numpy Basic Part3
2. characteristics of numpy array
2-4. Concatenated application of numpy functions
2-5. In-place operation
2-6. Tiling/Joining Arrays

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

print('''
First define a sample array
arr1= np.arange(24)
arr1= np.reshape(arr1, [4,6])''')
arr1= np.arange(24)
arr1= np.reshape(arr1, [4,6])
show_array_info(arr1)

print('''
# We already saw that below two lines produce the same result.
# arr1= np.reshape(arr1, [4,6])
# arr1= arr1.reshape([4,6])

# This is because 'reshape' is a numpy function as well as a method of numpy array class
# In the case of method of array, multiple methods can be concatenated.
''')

input("\nPress Enter to continue... (2-4a)\n")

print("Example of grid-degrading (e.g., 0.5x0.5deg --> 1x1deg): \n")
print("c= arr1.reshape([2,2,3,2]).swapaxes(1,2).reshape([2,3,4]).mean(axis=2)")
c= arr1.reshape([2,2,3,2]).swapaxes(1,2).reshape([2,3,4]).mean(axis=2)
show_array_info(c)

print("""
c2= arr1.reshape([2,2,3,2]).mean(axis=(1,3))  # 'mean' over multiple axes
print(np.array_equal(c,c2))""")
c2= arr1.reshape([2,2,3,2]).mean(axis=(1,3))
print(np.array_equal(c,c2))

input("\nPress Enter to continue... (2-4b)\n")

print("""
Example of calculating monthly anomaly:
Define new array: d= np.arange(120)  # Assume monthly 10-years time-series
""")
d= np.arange(120)
print("clim_d= d.reshape([-1,12]).mean(axis=0)")
print("ano= (d.reshape([-1,12]) - clim_d.reshape([1,12])).reshape(-1) \n")
clim_d= d.reshape([-1,12]).mean(axis=0)
ano= (d.reshape([-1,12]) - clim_d.reshape([1,12])).reshape(-1)

print("ano[:12] = {}".format(ano[:12]))
print("ano[::12] = {}".format(ano[::12]))

print("\nPress Enter to continue... (2-4c)\n")
input("----------------------------------------\n")

print("\n2-5. In-place operation")

print("\nDefine new array: e= np.zeros([2,2])")
e= np.zeros([2,2])
show_array_info(e)

print("""
### Copy or not?
Test1:
e1= e
e1[0,0]= 1
print(e)""")
e1= e
e1[0,0]= 1
print(e)

print("""
Test2:
e2= np.copy(e)
e2[0,1]= 2
print(e)""")
e2=np.copy(e)
e2[0,1]=2
print(e)

print("""
Test3:
e3= e[:]
e3[1,0]= 3
print(e)""")
e3= e[:]
e3[1,0]= 3
print(e)

input("\nPress Enter to continue... (2-5a)\n")

print("""
Test4:
e4= e[1,:]
e4[1]=4
print(e)""")
e4= e[1,:]
e4[1]=4
print(e)

print("""
Test5:
e5= e.reshape(-1)  # 'copy' characteristic varies by numpy functions
e5[0]= -9
print(e)""")
e5= e.reshape(-1)
e5[0]= -9
print(e)

print("""
Test6: Define a function
def function1(arr):
    arr[0]=-1
    return
function1(e[:,1])
print(e)""")
def function1(arr):
    arr[0]=-1
    return
function1(e[:,1])
print(e)

print("""
# Remember: The assignment in python is just creating a pointer to the memory location.
# With numpy, please make sure that it is copied when necessary.
# Particularly be cautious when passing array to function(s).
#
# It is also interesting that, in the case of 'List,' '[:]' plays a role of copy,
# but not in numpy.
""")

print("\nPress Enter to continue... (2-5b)\n")
input("----------------------------------------\n")

print("\n2-6. Tiling/Joining Arrays")

print('''
Define a sample array
a= np.arange(4)''')
a= np.arange(4)
print(a)

print('\nb= np.tile(a,3)  # Repeat as a whole')
b= np.tile(a,3)
show_array_info(b)

print('\nb2= np.tile(a,[2,2])  # Repeat as a whole')
b2= np.tile(a,[2,2])
show_array_info(b2)

print('\nc= np.repeat(a,3)  # Repeat by element')
c= np.repeat(a,3)
show_array_info(c)

print('\nIn the case of 2-D array,')
print('a= np.arange(4).reshape([2,2])')
a= np.arange(4).reshape([2,2])
print(a)

print('\nb= np.tile(a,2)  # Repet as a whole')
b= np.tile(a,2)
show_array_info(b)

print('\nc= np.repeat(a,2)  # Repet by element')
c= np.repeat(a,2)
show_array_info(c)

print('\nc2= np.repeat(a,2,axis=1)  # Repet by element')
c2= np.repeat(a,2,axis=1)
show_array_info(c2)

input("\nPress Enter to continue... (2-6a)\n")

print('''
Define two sample arrays
d1= np.arange(6).reshape([2,3])
d2= d1+10''')
d1= np.arange(6).reshape([2,3])
d2= d1+10
show_array_info(d1)
show_array_info(d2)

print("\ne= np.stack((d1,d2))  # 'stack'")
e= np.stack((d1,d2))
show_array_info(e)

print("\nAbove is same to e= np.concatenate((d1.reshape([1,*d1.shape]),d2[None,:,:]),axis=0)")
e= np.concatenate((d1.reshape([1,*d1.shape]),d2[None,:,:]),axis=0)
show_array_info(e)

input("\nPress Enter to continue... (2-6b)\n")

print("\ne= np.hstack((d1,d2))  # 'hstack'")
e= np.hstack((d1,d2))
show_array_info(e)

print("\nAbove is same to e= np.concatenate((d1,d2),axis=1)")
e= np.concatenate((d1,d2),axis=1)
show_array_info(e)

input("\nPress Enter to continue... (2-6c)\n")

print("f= np.vstack((d1,d2))  # 'vstack'")
f= np.vstack((d1,d2))
show_array_info(f)

print("\nAbove is same to f= np.concatenate((d1,d2),axis=0)")
f= np.concatenate((d1,d2),axis=0)
show_array_info(f)

input("\nPress Enter to continue... (2-6d)\n")

print("g= np.dstack((d1,d2))  # 'dstack'")
g= np.dstack((d1,d2))
show_array_info(g)

print("\nAbove is same to g= np.concatenate((d1.reshape([*d1.shape,1]),d2[:,:,None]),axis=2)")
g= np.concatenate((d1.reshape([*d1.shape,1]),d2[:,:,None]),axis=2)
show_array_info(g)

input("\nPress Enter to continue... (2-6e)\n")


print('''Check other numpy functions, too!
### Simple statistical methods
np.dot()
np.max(arr1); np.maximum(arr1,arr2)
np.mean(); np.average()
np.min(arr1); np.minimum(arr1,arr2)
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
np.unique()
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
...

### https://numpy.org/doc/stable/reference/
''')
print("THE END: Basic Numpy\n")
