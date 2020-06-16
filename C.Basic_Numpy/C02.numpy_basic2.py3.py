'''
Numpy Basic(2)
: Some characteristics of array and popular functions

By Daeho Jin
'''

print("\n2. characteristics of numpy array")
print("\n2-1. Operation of array(s)")

### Simple operation
print('\nFirst define sample arrays')
print('''ones= np.ones([2,2])
fulls= np.full_like(ones,-1.5)''')
ones= np.ones([2,2])
fulls= np.full_like(ones,-1.5)
print('\nAdd: twos = ones+ones')
twos = ones+ones
show_array_info(twos)

print('\nAdd: i_plus_f = ones(int)+fulls(float)')
i_plus_f = ones+fulls
show_array_info(i_plus_f)

print('\nMultiplication: mult1 = twos*fulls')
mult1 = twos*fulls
show_array_info(mult1)

print('\nMultiplication: mult2 = twos*3')
mult2= twos*3
show_array_info(tmp_multiply2)

print('\nMulitplication: mult3 = twos(2D)*array_1d')
print('array_1d = fulls[0,:]')
array_1d = fulls[0,:]
mult3= twos*array_1d
show_array_info(mult3)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n1-5. Array Operation")

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
