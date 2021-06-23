'''
Numpy Basic Part2
2. characteristics of numpy array
2-1. Operation of array(s)
2-2. Slicing and Indexing
2-3. Numpy.where() function

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
print('''
First define sample arrays:
arr1= np.arange(6).reshape([2,3])
arr2= (np.arange(6)-1.).reshape([2,3])
''')
arr1= np.arange(6).reshape([2,3])
arr2= (np.arange(6)-1.).reshape([2,3])
show_array_info(arr1)
show_array_info(arr2)
print('\nAdd: add1 = arr1 + arr1')
add1 = arr1+arr1
show_array_info(add1)

print('\nAdd: i_plus_f = arr1(dtype=int) + arr2(dtype=float)')
i_plus_f = arr1+arr2
show_array_info(i_plus_f)

print('\nMultiplication: mult1 = arr1 * 3.')
mult1= arr1*3.
show_array_info(mult1)

print('\nMultiplication: mult2 = arr1 * arr2')
mult2 = arr1*arr2
show_array_info(mult2)
print('---> Element-wise operation!')

input("\nPress Enter to continue... (2-1a)\n")

print('\nMulitplication: mult3 = arr1(2D) * array_1d')
print('\narr_1d = arr2[0,:]')
arr_1d = arr2[0,:]
show_array_info(arr_1d)
print('\nmult3= arr1 * arr_1d')
mult3= arr1*arr_1d
show_array_info(mult3)

print('\narr_1d = arr2[:,0]')
arr_1d = arr2[:,0]
show_array_info(arr_1d)
try:
    print('mult4= arr1 * arr_1d')
    mult4= arr1*arr_1d
except Exception as err:
    print("Error message\n:",err)
print("\n---> Working only when the size matched to the last axis of 2D array. \n" )

input("\nPress Enter to continue... (2-1b)\n")

print("\n* Two methods enabling the multiplication without error")
print("Method1: mult4= arr1 * arr_1d.reshape([-1,1])")
mult4= arr1*arr_1d.reshape([-1,1])
show_array_info(mult4)

print("\nMethod2: mult4= arr1 * arr_1d[:,None]")
mult4= arr1*arr_1d[:,None]
show_array_info(mult4)


print("\nPress Enter to continue... (2-1c)\n")
input("----------------------------------------\n")

print("\n2-2. Slicing and Indexing")

print('\nSlicing: Same as shown with "List"')
print('a= np.arange(10) # Define a numpy array')
a= np.arange(10)
show_array_info(a)
print("\na[2:5] = {}  # = a[2:5:1]".format(a[2:5]))
print("a[::2] = {}  # = a[0:len(a):2]".format(a[::2]))
print("a[1::2] = {}".format(a[1::2]))
print("a[::-1] = {}  # Flip the order".format(a[::-1]))
print("a[8:1:-2] = {}  # Reversed slicing is working  # = a[-2:1:-2]".format(a[8:1:-2]))

input("\nPress Enter to continue... (2-2a)\n")

print('\nIndexing: Pull out data by providing indices')
print('index_list = [1,3,5]  # List object')
index_list=[1,3,5]
print('a[index_list] = {}'.format(a[index_list]))
print('a[::-1][index_list] = {}'.format(a[::-1][index_list]))

print('\nindex_arr= np.array([1,3,5])  # numpy array')
index_arr= np.array([1,3,5])
print('a[index_arr] = {}'.format(a[index_arr]))
print('a[::-1][index_arr] = {}'.format(a[::-1][index_arr]))

print('\nHow about the index of other than integer?')
print('index_list= np.asfarray([1,3,5])  # numpy float array')
index_list= np.asfarray([1,3,5])
try:
    print('a[::-1][index_list] = {}'.format(a[::-1][index_list]))
except Exception as err:
    print("Error message\n:",err)

input("\nPress Enter to continue... (2-2b)\n")

print('''
In the case of 2-D array,
idx= [0,2]  # List
b= np.arange(12).reshape([4,3])''')
idx= [0,2]  # List
b= np.arange(12).reshape([4,3])
show_array_info(b)
print('\nb[idx,:] = {}'.format(b[idx,:]))
print('\nb[:,idx] = {}'.format(b[:,idx]))

print("\nIf given just one index to 2-D array?")
print("b[0] = {}".format(b[0]))
print("b[-1] = {}".format(b[-1]))
print('b[idx] = {}'.format(b[idx]))
print("---> It is interpreted as the index of the first axis (axis=0)")

input("\nPress Enter to continue... (2-2c)\n")

print("\nIf multiple indexes are given?")
print("b[idx,idx] = {}".format(b[idx,idx]))

print('''
FYI, b[0,0] = {}, b[2,2] = {}
---> arr[[x1,x2],[y1,y2]] results in [arr[x1,y1], arr[x2,y2]]

b[idx,0:2] = {}
---> One index can be combined with slicing

b[idx,:][:,idx] = {}
---> This is the proper way for our expectation
'''.format(b[0,0],b[2,2],b[idx,0:2],b[idx,:][:,idx]))

input("\nPress Enter to continue... (2-2d)\n")

print('\nIndexing with some conditions')
print('Use array "b" for examples')
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

print('''
Three (or more) conditions:
idx= np.logical_and.reduce((b>2, b<9, b%2==0))
* This is same to: idx= np.logical_and(np.logical_and(b>2, b<9), b%2==0)''')
idx= np.logical_and.reduce((b>2,b<9,b%2==0))
show_array_info(idx)
print('c3= b[idx]')
c3= b[idx]
show_array_info(c3)

print("\nPress Enter to continue... (2-2e)\n")
input("----------------------------------------\n")

print("\n2-3. Numpy.where() function")

print('\nUsage1: When want to know index location of certain condition')
print('\nUse array "b" again')
show_array_info(b)

print('\nloc= np.where(np.logical_and(b>=3, b<8)) # np.where(condition)')
loc= np.where(np.logical_and(b>=3, b<8))
print('\ntype(loc)= {}; len(loc)= {}; type(loc[0])= {}'.format(type(loc),len(loc),type(loc[0])))
print('''
for i,j in zip(*loc):
    print("i={}, j={}, value={}".format(i,j,b[i,j]))''')
for i,j in zip(*loc):
    print("i={}, j={}, value={}".format(i,j,b[i,j]))

print("""
b[loc]= {}
---> For this purpose, 'b[np.logical_and(b>=3, b<8)]' is more efficient.""".format(b[loc]))
input("\nPress Enter to continue... (2-3a)\n")

print('\nUsage2: When want to replace values by certain condition(s)')
print('\nUse array "b" again')
show_array_info(b)

print('\nd= np.where(b%3==1,-1,b)  # np.where(condition, val if True, val if False)')
d= np.where(b%3==1,-1,b)
show_array_info(d)

input("\nPress Enter to continue... (2-3b)\n")
print("----------------------------------------\n")

print("Continue to Numpy Basic Part3 ==>\n")
