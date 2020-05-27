
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

