'''
Python Basic Part5
: Defining custom function

By Daeho Jin
'''

### Functions
print("\n*** Custom Function ***")
print("\n1. Function basic")
print("""
def function_name(*args,**kwrds):
    some_contents  # Keep 'consistent' spacing
    return something   # Optional
""")

print('''Example1:
def test_function():
   #No contents and just return
   return "Hello"

test_function()  # Call the function
''')
def test_function():
   #No contents now
   return "Hello"

print("Result:")
print("{}".format(test_function()))

input("\nPress Enter to continue... (1-1)\n")

print("""Example2:
def test_function2():
    print('Good morning!')

test_function2()  # Call the function
""")
def test_function2():
    print('Good morning!')

print("Result:")
print("{}".format(test_function2()))

print("""
* The conditions a function ends:
1. 'return' is invoked.
2. Function block is completed.
""")
input("\nPress Enter to continue... (1-2)\n")

print('''Example3:
def sum_every2(num):
   """
   Simple Function Example
   Sum by every 2.
   """
   sum1=0
   for i in range(0,num,2):
      sum1+=i
   return sum1
''')

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
print("Result of sum_every2(10) = {}".format(sum_every2(10)))
print("Result of sum_every2(100) = {}".format(sum_every2(100)))

print("\nPress Enter to continue... (1-3)\n")
input("----------------------------------------\n")

print("\n2. Lambda Function")
print("function_name = lambda *args,**kwrds: some 1-line content\n")

print('''Example:
sum_ev2 = lambda num: sum(list(range(0,num,2))) if num>0 else -99
''')
sum_ev2 = lambda num: sum(list(range(0,num,2))) if num>0 else -99
print("print document of function sum_ev2:\nsum_ev2.__doc__ = {}"\
        .format(sum_ev2.__doc__))
print("Result of sum_ev2(10) = {}".format(sum_ev2(10)))
print("Result of sum_ev2(-1) = {}".format(sum_ev2(-1)))

print("\nPress Enter to continue... (2)\n")
input("----------------------------------------\n")

print("\n3. Function with keywords (defalut value(s))")
print('''
Example:
def sum_every_n(num,n=1):
   """
   Simple Function Example with default argument
   num: maximum limit to be summed, should be >0
   n  : to be summed by every n, default=1
   """
   if num<=0:
      print("Input should be >0")
      return -99
   sum1=0
   for i in range(0,num,n):
      sum1+=i
   return sum1
''')
def sum_every_n(num,n=1):
   '''
   Simple Function Example with default argument
   num: maximum limit to be summed, should be >0
   n  : to be summed by every n, default=1
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
print("Result of sum_every_n(10) = {}".format(sum_every_n(10)))
print("Result of sum_every_n(10,3) = {}".format(sum_every_n(10,3)))
print("Result of sum_every_n(10,n=3) = {}".format(sum_every_n(10,n=3)))
print("Result of sum_every_n(num=10,n=3) = {}".format(sum_every_n(num=10,n=3)))
print("Result of sum_every_n(-1) = {}".format(sum_every_n(-1)))

print("\nCaution: keywords must come later than arguments!")

print("\nPress Enter to continue... (3)\n")
input("----------------------------------------\n")

print("\n4. Function inside function?")
print('''
Example:
def function_odd_even(num):
    """
    Simple Function Example embeding another funnction
    num: any number
    """
    def odd_even_tester(num):
        """
        True if even else False
        """
        if num%2==0:
            return True
        else:
            return False

    if odd_even_tester(num):
        print("Even")
    else:
        print("Odd")
    return
''')
def function_odd_even(num):
    """
    Simple Function Example embeding another funnction
    num: any number
    """
    def odd_even_tester(num):
        """
        True if even else False
        """
        if num%2==0:
            return True
        else:
            return False

    if odd_even_tester(num):
        print("Even")
    else:
        print("Odd")
    return

print("Result of function_odd_even(4) = {}".format(function_odd_even(4)))
print("Result of function_odd_even(3.5) = {}\n".format(function_odd_even(3.5)))
try:
    print("Result of odd_even_tester(3.5) = ")
    print("{}".format(odd_even_tester(3.5)))
except Exception as err:
    print("Error message\n:",err)


print("\nPress Enter to continue... (4)\n")
input("----------------------------------------\n")

print("\n5. Recursive Function")
print('''
Example:
def function_divide_by2(num,count=0,remainder=0):
    """
    Simple Example for recursive function
    num: any number
    """
    if num%2==0:
        num/=2
        count+=1
        return function_divide_by2(num,count)
    elif num==1:
        return count, remainder
    else:
        remainder=num
        return count, remainder
''')
def function_divide_by2(num,count=0,remainder=0):
    """
    Simple Example for recursive function
    num: any number
    """
    if num%2==0:
        num/=2
        count+=1
        return function_divide_by2(num,count)
    elif num==1:
        return count, remainder
    else:
        remainder=num
        return count, remainder

print("Result of function_divide_by2(8) = {} times + {}".format(
        *function_divide_by2(8)))
print("Result of function_divide_by2(20) = {} times + {}".format(
        *function_divide_by2(20)))
print("Result of function_divide_by2(4.5) = {} times + {}".format(
        *function_divide_by2(4.5)))

print("\nPress Enter to continue... (5)\n")
input("----------------------------------------\n")

print("\n6. Function examples")
print("\nQ. Variables passed to a function are copied or not?")
print("""Example Code:
def append_list(list1,val):
    if isinstance(list1,list):  # Check if variable 'list1' is 'list' object or not
        list1.append(val)
    else:
        print("list1 is not list object!")
        #sys.exit("some message")  # If want to quit the program (import sys)
""")

def append_list(list1,val):
    if isinstance(list1,list):  # Check if the 1st variable is 'list' object or not
        list1.append(val)
    else:
        print("list1 is not list object!")
        #sys.exit("some message")  # If want to quit the program

list1 = []
print("""Define a list and call the function:
list1 = []
Result of append_list(list1,1) = {}
""".format(append_list(list1,1)))

print("How about list1 now?")
print("list1 = {}".format(list1))
print("---> Keep in mind that 'list1' is not returned, but updated!\n")
print("FYI, Result of append_list(1,1) = {}".format(append_list(1,1)))

input("\nPress Enter to continue... (6-1)\n")

print("\nExample2: Functions to transform Lon/Lat to index\n")
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
print("""
lon0, dlon = -179.5, 1.
lat0, dlat = -89.5, 1.
""")
lon0, dlon = -179.5, 1.
lat0, dlat = -89.5, 1.
print("Index of (0E,0N) = ",lon_deg2x(0,lon0,dlon),lat_deg2y(0,lat0,dlat))
print("Index of (-0.5E,-0.5N) = ",lon_deg2x(-0.5,lon0,dlon),lat_deg2y(-0.5,lat0,dlat))
print("Index of (-180E,-90N) = ",lon_deg2x(-180,lon0,dlon),lat_deg2y(-90,lat0,dlat))
print("Index of (360E,90N) = ",lon_deg2x(360,lon0,dlon),lat_deg2y(90,lat0,dlat))

print("\nPress Enter to continue... (6-2)\n")
input("----------------------------------------\n")

print("THE END: Python Basic Part5 - Defining a function\n")
