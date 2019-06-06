'''
Python Basic(2)
3. IF
4. FOR
5. WHILE
'''

### If basic
if True:
   print("IF True\n")
elif False:
   print("Not printing here")
else:
   print("Not printing here")

### For basic
list1, list2, list3 = [], [], []
for i in range(20):  
### range(20) = range(0,20) = range(0,20,1)
   if i%3==0:
      list1.append(i)
   elif i%3==1:
      list2.append(i)
   else:
      list3.append(i)

print(list1)
print(list2)
print(list3, '\n')

### For + zip
list4=[]
for i,j in zip(list1,list2):
   list4.append(str(i)+str(j))
#print(list4)
for a in list4:
   print(a)

print('\n')
list5=[]
for i,j,k in zip(list1,list2,list3):
   list5.append(str(i)+str(j)+str(k))
#print(list5)
### For + enumerate
for i,a in enumerate(list5):
   print(i,a)

### While
print('\n')
i=0
while i<len(list5):
   print(int(list5[i])-i)
   i+=1

print('\n')

### Functions
def test_function():
   #Some contents
   return "Yes"

print(test_function(),'\n')

###---

def sum_every2(num):
   '''
   Simple Function Example
   Argument "num" should be >0
   '''   
   if num<=0:
      print("Input should be >0")
      return -999

   sum1=0
   for i in range(0,num,2):
      sum1+=i

   return sum1

print(sum_every2.__doc__)
print(sum_every2(10))
print(sum_every2(100))
print(sum_every2(-1),'\n')

###---
print("Function: Simple version (lambda)")
sum_ev2 = lambda num: sum(list(range(0,num,2))) if num>0 else -999
print(sum_ev2(10))
print(sum_ev2(100))
print(sum_ev2(-1),'\n')

 
print("Function with default value(s)")
def sum_every_n(num,n=2):
   '''
   Simple Function Example with default argument
   Arg "num" should be >0
   Arg "n" default value is 2
   '''
   if num<=0:
      print("Input should be >0")
      return -999

   sum1=0
   for i in range(0,num,n):
      sum1+=i

   return sum1

print(sum_every_n.__doc__)
print(sum_every_n(10))
print(sum_every_n(100,3))
print(sum_every_n(100,n=3))
print(sum_every_n(num=100,n=3))
print(sum_every_n(-1),'\n')

###---
from math import ceil
def lon_deg2x(lon,lon0,dlon):
    x=ceil((lon-lon0)/dlon)
    if lon0<0 and lon>180:
        x-= int(360/dlon)
    if lon0>0 and lon<0:
        x+= int(360/dlon)

    return x
lat_deg2y = lambda lat,lat0,dlat: ceil((lat-lat0)/dlat)

lon0=-179.5; dlon=1.
lat0=-89.5; dlat=1.
print("(0E,0N)=",lon_deg2x(0,lon0,dlon),lat_deg2y(0,lat0,dlat))

