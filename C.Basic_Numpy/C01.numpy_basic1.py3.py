'''
Numpy Basic(1)
1. How to create a numpy array
1-1. Using pre-defined template
1-2. Transform to numpy array
1-3. 'arange' and 'linspace'
1-4. Reshaping array

By Daeho Jin
'''

print("\n0. Before Start")

print("\nImport numpy package:\nimport numpy as np")
import numpy as np

print("\nFor convenience, define a function showoing numpy array information:")
print('''
def show_array_info(a,show_contents=True):
   """
   Print information of numpy array
   """
   result="N_Dims={}, Shape={}, Data_Type={}".format(a.ndim, a.shape, a.dtype)
   print(result)
   if show_contents:
      print(a)
   return
''')

def show_array_info(a,show_contents=True):
   """
   Print information of numpy array
   """
   result="N_Dims={}, Shape={}, Data_Type={}".format(a.ndim, a.shape, a.dtype)
   print(result)
   if show_contents:
      print(a)
   return

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

### Make new array
print("\n1. How to create a numpy array")
print("\n1-1. Using pre-defined template")
print("array = np.function(dimension, dtype=dtype, ...)")
print("array = np.function_like(other_array, dtype=dtype, ...)\n")

print("zeros = np.zeros([2,3])")
zeros = np.zeros([2,3])
print("show_array_info of zeros:")
show_array_info(zeros)

print("\nones = np.ones_like(zeros, dtype=int)")
ones = np.ones_like(zeros, dtype=int)
print("show_array_info of ones:")
show_array_info(ones)

print("\nempty = np.empty_like(ones, dtype=np.float32)")
empty = np.empty_like(ones, dtype=np.float32)
print("show_array_info of empty:")
show_array_info(empty)

print("\nfull = np.full_like(ones, -999.9)")
full = np.full_like(ones, -999.9)
print("show_array_info of full:")
show_array_info(full)
print("\nThis is also same: full = np.full(ones.shape, -999.9, dtype=ones.dtype)")
full = np.full(ones.shape, -999.9, dtype=ones.dtype)
print(full)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n1-2. Transform to numpy array")
print("Example: lsit to numpy array")
print("a=[[0,1,2],[4,5,6]]  # A list")
a=[[0,1,2],[4,5,6]]  ### A list
print('''
Test 3 methods:
b=np.array(a)
c=np.asarray(a)
d=np.asfarray(a)
''')
b=np.array(a)
c=np.asarray(a)
d=np.asfarray(a)

print("show_array_info of np.array:")
show_array_info(b)

print('\nshow_array_info of np.asarray')
show_array_info(c)
print("""
# np.array vs. np.asarray: 'np.array' is more general,
# and default is copying the input,
# while 'np.asarray' will return uncopied if it's compatible.""")

print('\nshow_array_info of np.asfarray')
show_array_info(d)
print("\nThis is same as 'np.asarray(input,dtype=float)'")
show_array_info(np.asarray(a,dtype=float))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n1-3. 'arange' and 'linspace'")

print("\ne=np.arange(5)  # Similar to range()")
e=np.arange(5)
show_array_info(e)

print("\nf=np.arange(0,5,0.5)  # Non-integer increment is possible while not in range()")
f=np.arange(0,5,0.5)
show_array_info(f)

print("\ng=np.linspace(1,10,4)  # 3 even spaces (4 boundary values) between 1 and 10")
g=np.linspace(1,10,4)
show_array_info(g)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n1-4. Reshaping array")

print("\nh=np.arange(12)  # 1-d array")
h=np.arange(12)
print("\nh=np.reshape(h,[3,4])  # 2-d array")
h=np.reshape(h,[3,4])   ### Reshape: Very Important!
show_array_info(h)
print("""
# This is also same: h=np.arange(12).reshape([3,4])
""")
print("\nh=h.T  # Transpose")
h=h.T  ### Same: np.transpose()
show_array_info(h)

print("\nh=h.reshape([2,2,3])")
h=h.reshape([2,2,3])
show_array_info(h)

print("\nh=h.swapaxes(1,2)  # Swap between axis1 and axis2")
h=h.swapaxes(1,2)
show_array_info(h)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("Continue to Numpy Basic2\n")
