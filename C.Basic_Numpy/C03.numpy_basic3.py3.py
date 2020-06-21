input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n2-4. Concatenated application of numpy functions")

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")
print("\n . Random module examples")


input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2-3. In-place operation")

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2-4. Array transformation") # hsatck, vstack, ...

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n NaN and Masked Array")

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

loc=np.where(np.logical_and(e2>5,e2<10))
print(type(loc),len(loc))
for j,i in zip(*loc):
  print("j={}, i={}, value={}".format(j,i,e2[j,i]))


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
