"""
Numpy - basic methods
"""

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
   
### Make new array
zeros = np.zeros([3,4]) 
ones = np.ones([3,4],dtype=int)  
empty = np.empty([3,4],dtype=np.float32)  
full = np.full_like(zeros,-999.9)
print('\nnp.zeros') ;show_array_info(zeros)
print('\nnp.ones')  ;show_array_info(ones)
print('\nnp.empty') ;show_array_info(empty)
print('\nnp.full') ;show_array_info(full)

a=[[0,1,2,3],[4,5,6,7],[8,9,10,11]]  ### A list
b=np.array(a)  
c=np.asarray(a) 
d=np.asfarray(a) 

print('\nnp.array') ;show_array_info(b)
print('\nnp.asarray')  ;show_array_info(c,show_contents=False)
print('\nnp.asfarray') ;show_array_info(d,show_contents=False)

e=np.arange(12)  ### Similar to range()
print('\nnp.arange(12)',e.shape)
e=np.reshape(e,[4,3])   ### Reshape: Very Important!
print('\n After Reshape')
show_array_info(e)
e=e.T  ### Same: transpose()
print('\n After Transpose')
show_array_info(e)
# e=np.arange(12).reshape([4,3])

f=np.linspace(1,10,4)
print('\n np.linspace(1,10,4)'); show_array_info(f)


### Simple operation
print('\n Adding Array')
tmp_plus= ones+ones
show_array_info(tmp_plus)

print('\n Adding Int Array and Float Array')
tmp_plus2= ones+full
show_array_info(tmp_plus2)

print('\n Array*Array')
tmp_multiply= tmp_plus*tmp_plus
show_array_info(tmp_multiply)

print('\n Array*number')
tmp_multiply2= tmp_multiply*3
show_array_info(tmp_multiply2)

print('\n Array_2D*Array_1D')
tmp_multiply3= tmp_multiply*f[None,:]
show_array_info(tmp_multiply3)


### Copy or not copy
ones2=ones
ones2[0,0]=2
print('\n Copy or not?')
show_array_info(ones)

ones3=np.copy(ones)
ones3[0,0]=3
print('\n Copy or not?')
show_array_info(ones)

ones4=ones[:]
ones4[0,0]=4
print('\n Copy or not?')
show_array_info(ones)


### Transform the array
print('\n Starting Array before Transformation')
show_array_info(e)

print('\n Array.astype(np.int16)')
e2=e.astype(np.int16)
show_array_info(e2,show_contents=False)

print('\n Partial sum of array')
show_array_info(e2.reshape([3,2,2]).sum(axis=2))

print('\n Swap Axes')
e2=e2.reshape([-1,2,2]).swapaxes(1,2).reshape([-1,4]) ### "-1" in reshape means "all others"
show_array_info(e2)

print('\n Slicing with index list [:,[1,3]]')
index_list=[1,3]
e3=e2[:,index_list]
show_array_info(e3)


### Indexing
print('\n Find location satisfying specific condition')
loc=np.where(np.logical_and(e2>5,e2<10))
print(type(loc),len(loc))
for j,i in zip(*loc):
  print("j={}, i={}, value={}".format(j,i,e2[j,i]))

print('\n Usually don\'t need to know the location')
idx=np.logical_and(e2>5,e2<10)
show_array_info(idx)
show_array_info(e2[idx])

'''
### Logical operation
np.logical_and()
np.logical_or()
np.logical_not()

### Expanding Array
repeat()
np.tile()
np.concatenate()
np.hstack()
np.vstack()

### Simple statistical methods
dot()
max()
mean(); np.average()
min()
sum()
std()
var()
np.median()
np.around()
sort()
np.cumsum()
np.percentile()
np.digitize()
np.histogram()
np.corrcoef()

### Argument methods
argmax() # Return index of maximum value
argmin()
argsort()

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

### https://docs.scipy.org/doc/numpy/reference/



'''
