'''
Numpy Basic(2)
: Some characteristics of array and popular functions

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
print("\n2-1. Operation of array(s)")

### Simple operation
print('\nFirst define sample arrays')
print('''arr1= np.arange(6).reshape([2,3])
arr2= (np.arange(6)-1.).reshape([2,3])''')
arr1= np.arange(6).reshape([2,3])
arr2= (np.arange(6)-1.).reshape([2,3])
show_array_info(arr1)
show_array_info(arr2)
print('\nAdd: add1 = arr1+arr1')
add1 = arr1+arr1
show_array_info(add1)

print('\nAdd: i_plus_f = arr1(int)+arr2(float)')
i_plus_f = arr1+arr2
show_array_info(i_plus_f)

print('\nMultiplication: mult1 = arr1*3.')
mult1= arr1*3.
show_array_info(mult1)

print('\nMultiplication: mult2 = arr1*arr2')
mult2 = arr1*arr2
show_array_info(mult2)
print('# Element-wise operation!')
input("\nPress Enter to continue...\n")

print('\nMulitplication: mult3 = arr1(2D)*array_1d')
print('arr_1d = arr2[0,:]')
arr_1d = arr2[0,:]
show_array_info(arr_1d)
print('mult3= arr1*arr_1d')
mult3= arr1*arr_1d
show_array_info(mult3)

print('\narr_1d = arr2[:,0]')
arr_1d = arr2[:,0]
show_array_info(arr_1d)
try:
    print('mult4= arr1*arr_1d')
    mult4= arr1*arr_1d
except Exception as err:
    print("Error message\n:",err)
print("\n# Working only when the size matched to the last axis of 2D array." )
print("# Below shows two methods making it working")
print("\nMethod1: mult4= arr1*arr_1d.reshape([-1,1])")
mult4= arr1*arr_1d.reshape([-1,1])
show_array_info(mult4)

print("\nMethod2: mult4= arr1*arr_1d[:,None]")
mult4= arr1*arr_1d[:,None]
show_array_info(mult4)


input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n2-2. Slicing and Indexing")

print('\nSlicing: Same as shown with "List"')
print('a= np.arange(10) # Define a numpy array')
a= np.arange(10)
show_array_info(a)
print("\na[2:5] = {}  # = a[2:5:1]".format(a[2:5]))
print("a[::2] = {}  # = a[0:len(a):2]".format(a[::2]))
print("a[1::2] = {}".format(a[1::2]))
print("a[::-1] = {}  # Flip the order".format(a[::-1]))
print("a[8:1:-2] = {}  # Reversed slicing is not working".format(a[::-1]))

print('\nIndexing: Pull out data by providing indexes')
print('index_list=[1,3,5]  # List object')
index_list=[1,3,5]
print('a[::-1][index_list] = {}'.format(a[::-1][index_list]))
print('\nindex_list= np.array([1,3,5])  # numpy array')
index_list= np.array([1,3,5])
print('a[::-1][index_list] = {}'.format(a[::-1][index_list]))

input("\nPress Enter to continue...\n")

print('\nIndexing with some conditions')
print('b=np.arange(12).reshape([3,4]) # Define a numpy array')
b=np.arange(12).reshape([3,4])
show_array_info(b)
print('\nOne condition: idx= b>2')
idx= b>2
show_array_info(idx)
print('c1= b[idx]')
c1= b[idx]
show_array_info(c1)
print('# Output of indexing is 1-D array!')

print('\nTwo conditions: idx= np.logical_and(b>2, b<9)')
idx= np.logical_and(b>2,b<9)
show_array_info(idx)
print('c2= b[idx]')
c2= b[idx]
show_array_info(c2)

print('\nThree conditions: idx= np.logical_and.reduce((b>2, b<9, b%2==0))')
idx= np.logical_and.reduce((b>2,b<9,b%2==0))
show_array_info(idx)
print('c3= b[idx]')
c3= b[idx]
show_array_info(c3)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n2-3. Numpy.where() function")

print('\nUsage1: When want to know index location of certain condition')
print('\narray "b" is already defined above')
show_array_info(b)

print('\nloc= np.where(np.logical_and(e2>=3, e2<10)) # np.where(condition)')
loc= np.where(np.logical_and(b>=3, b<10))
print('type(loc)= {}; len(loc)= {}; type(loc[0])= {}'.format(type(loc),len(loc),type(loc[0])))
print('''
for j,i in zip(*loc):
    print("j={}, i={}, value={}".format(j,i,b2[j,i]))
''')
for j,i in zip(*loc):
  print("j={}, i={}, value={}".format(j,i,b[j,i]))

print('\n\nUsage2: When want to replace values by certain condition')
print('\narray "b" is already defined above')
show_array_info(b)

print('\nd= np.where(b%3==1,-1,b)  # np.where(condition, val if True, val if False)')
d= np.where(b%3==1,-1,b)
show_array_info(d)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("Continue to Numpy Basic3\n")
