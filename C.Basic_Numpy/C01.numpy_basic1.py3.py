'''
Numpy Basic Part1
1. How to create a numpy array
1-1. Using pre-defined template
1-2. Transform to numpy array
1-3. 'arange' and 'linspace'
1-4. Reshaping array

By Daeho Jin
'''

print("\n0. Before Start")

print("""
We need to import numpy package:
import numpy as np
""")
import numpy as np

print("For convenience, define a function showoing numpy array information:")
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

print("\nPress Enter to continue... (0)\n")
input("----------------------------------------\n")

### Make new array
print("\n1. How to create a numpy array")
print("\n1-1. Using pre-defined template")
print("array = np.function(dimension, dtype=dtype, ...)  # f= zeros, ones, emtpy, full")
print("array = np.function_like(other_array, dtype=dtype, ...)\n")

print("z = np.zeros([2,3])  # right-most dim is inner-most")
z = np.zeros([2,3])
print("show_array_info of z:")
show_array_info(z)

print("\no = np.ones_like(z, dtype=int)")
o = np.ones_like(z, dtype=int)
print("show_array_info of o:")
show_array_info(o)

print("\ne = np.empty_like(o, dtype=np.float32)")
e = np.empty_like(o, dtype=np.float32)
print("show_array_info of e:")
show_array_info(e)

print("\nf = np.full_like(o, -999.9)")
f = np.full_like(o, -999.9)
print("show_array_info of f:")
show_array_info(f)
print("\nThis is same as: f2 = np.full(o.shape, -999.9, dtype=o.dtype)")
f2 = np.full(o.shape, -999.9, dtype=o.dtype)
print(f2)

print("\nPress Enter to continue... (1-1)\n")
input("----------------------------------------\n")

print("\n1-2. Transform to numpy array")
print("Example: list to numpy array")
print("a=[[0,1,2],[4,5,6]]  # A list")
a=[[0,1,2],[4,5,6]]  ### A list
print('''
Test 3 methods:
b = np.array(a)
c = np.asarray(a)
d = np.asfarray(a)
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
# while 'np.asarray' will return uncopied if it's compatible.
""")

print('show_array_info of np.asfarray')
show_array_info(d)
print("\nThis is same as 'np.asarray(input,dtype=float)'")
show_array_info(np.asarray(a,dtype=float))

print("\nPress Enter to continue... (1-2)\n")
input("----------------------------------------\n")

print("FYI: If the shape of list is inconsistent?")
print("a2=[[0,1,2],[4,5,]]  # A list")
a2=[[0,1,2],[4,5,]]  ### A list
print('''
b2 = np.array(a2)
''')
b2=np.array(a2)

print("show_array_info of np.array:")
show_array_info(b2)

print("\nPress Enter to continue... (1-2b)\n")
input("----------------------------------------\n")

print("\n1-3. 'arange' and 'linspace'")

print("\ne = np.arange(5)  # Similar to range()")
e=np.arange(5)
show_array_info(e)

print("\nf = np.arange(0, 5, 0.5)  # Non-integer increment is possible while not in range()")
f=np.arange(0,5,0.5)
show_array_info(f)

print("\ng = np.linspace(1, 10, 4)  # 3 even spaces (4 boundary values) between 1 and 10")
g=np.linspace(1,10,4)
show_array_info(g)

print("\nPress Enter to continue... (1-3)\n")
input("----------------------------------------\n")

print("\n1-4. Reshaping array")

print("\nh = np.arange(12)  # 1-d array")
h=np.arange(12)
print("\nh = np.reshape(h,[3,4])  # 2-d array; right-most dim is changing first")
h=np.reshape(h,[3,4])   ### Reshape: Very Important!
show_array_info(h)
print("""
# FYI, Two (or more) steps can be concatenated: h=np.arange(12).reshape([3,4])
""")

print("\nPress Enter to continue... (1-4a)\n")
input("----------------------------------------\n")

print("\nh = h.T  # Transpose")
h=h.T  ### Same: np.transpose()
show_array_info(h)

print("\nh = h.reshape([1,4,3])  # Left-most dim is outer-most ")
h=h.reshape([1,4,3])
show_array_info(h)

print("\nh = h.swapaxes(0,1)  # Swap between axis0 and axis1")
h=h.swapaxes(0,1)
show_array_info(h)

print("\nPress Enter to continue... (1-4b)\n")
input("----------------------------------------\n")

print("Continue to Numpy Basic Part2 ==>\n")
