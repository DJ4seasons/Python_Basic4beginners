'''
Python Basic(5)
: Defining custom function

By Daeho Jin
'''

### Functions
print("\n*** Custom Function ***")
print("\n1. Function basic")
print("def function_name(*args,**kwrds):")
print("    some_contents  # Keep 'consistent' spacing")
print("    return something   # Optional\n")

print('''Example1:
def test_function():
   #Some contents
   return "Yes"\n''')
def test_function():
   #No contents now
   return "Yes"

print("Result of test_function() = {}\n".format(test_function()))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print('''Example2:
def sum_every2(num):
   """
   Simple Function Example
   Sum by every 2.
   """
   sum1=0
   for i in range(0,num,2):
      sum1+=i
   return sum1\n''')

def sum_every2(num):
   """
   Simple Function Example
   Sum by every 2.
   """
   sum1=0
   for i in range(0,num,2):
      sum1+=i
   return sum1

print("print document of function sum_every2:\nsum_every2.__doc__ = {}"\
        .format(sum_every2.__doc__))
print("sum_every2(10) = {}".format(sum_every2(10)))
print("sum_every2(100) = {}".format(sum_every2(100)))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2. Lambda Function")
print("function_name = lambda *args,**kwrds: some 1-line content\n")

print('''Example:
sum_ev2 = lambda num: sum(list(range(0,num,2))) if num>0 else -99\n''')
sum_ev2 = lambda num: sum(list(range(0,num,2))) if num>0 else -99
print("print document of function sum_ev2:\nsum_ev2.__doc__ = {}"\
        .format(sum_ev2.__doc__))
print("sum_ev2(10) = {}".format(sum_ev2(10)))
print("sum_ev2(-1) = {}".format(sum_ev2(-1)))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n3. Function with keywords (defalut value(s))")
print('''Example:
def sum_every_n(num,n=2):
   """
   Simple Function Example with default argument
   num: maximum limit to be summed, should be >0
   n  : to be summed by n, default=2
   """
   if num<=0:
      print("Input should be >0")
      return -99
   sum1=0
   for i in range(0,num,n):
      sum1+=i
   return sum1\n''')
def sum_every_n(num,n=2):
   '''
   Simple Function Example with default argument
   num: maximum limit to be summed, should be >0
   n  : to be summed by n, default=2
   '''
   if num<=0:
      print("Input should be >0")
      return -99
   sum1=0
   for i in range(0,num,n):
      sum1+=i
   return sum1

print("print document of function sum_every_n:\nsum_every_n.__doc__ = {}"\
        .format(sum_every_n.__doc__))
print("sum_every_n(10) = {}".format(sum_every_n(10)))
print("sum_every_n(10,3) = {}".format(sum_every_n(10,3)))
print("sum_every_n(10,n=3) = {}".format(sum_every_n(10,n=3)))
print("sum_every_n(num=10,n=3) = {}".format(sum_every_n(num=10,n=3)))
print("sum_every_n(-1) = {}".format(sum_every_n(-1)))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n4. Function example1")
print("Functions to transform Lon/Lat to index\n")
from math import ceil
def lon_deg2x(lon,lon0,dlon):
    '''
    For given longitude information, return index of given specific longitude
    lon: target longitude to be transformed to index
    lon0: the first (smallest) value of longitude grid
    dlon: the increment of longitude grid
    return: integer index
    '''
    x = ceil((lon-lon0)/dlon)
    nx = int(360/dlon)
    if x<0:
        while(x<0):
            x+= nx
    if x>=nx: x=x%nx
    return x
lat_deg2y = lambda lat,lat0,dlat: ceil((lat-lat0)/dlat)

print("print document of function lon_deg2x:\nlon_deg2x.__doc__ = {}"\
        .format(lon_deg2x.__doc__))
print("lon0, dlon = -179.5, 1.\nlat0, dlat = -89.5, 1.")
lon0, dlon = -179.5, 1.
lat0, dlat = -89.5, 1.
print("Index of (0E,0N) = ",lon_deg2x(0,lon0,dlon),lat_deg2y(0,lat0,dlat))
print("Index of (-0.5E,-0.5N) = ",lon_deg2x(-0.5,lon0,dlon),lat_deg2y(-0.5,lat0,dlat))
print("Index of (-180E,-90N) = ",lon_deg2x(-180,lon0,dlon),lat_deg2y(-90,lat0,dlat))
print("Index of (360E,90N) = ",lon_deg2x(360,lon0,dlon),lat_deg2y(90,lat0,dlat))

input("\nPress Enter to continue...\n")
print("THE END: Python Basic(5) - Defining a function\n")
