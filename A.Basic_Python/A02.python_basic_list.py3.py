'''
Python Basic Part2
: List

By Daeho Jin
'''


###---- List
print("\n*** List ***")
### List basic
print("\n1. Define a list with []")
print("a = []  # Define an empty list" )
a = []
print("len(a) = {};\ttype(a) = {}".format(len(a),type(a)))

print("\na = [1, 'abc', 3.141592]  # Define a list" )
a = [1, 'abc', 3.141592]
print("len(a) = {};\ttype(a) = {}".format(len(a),type(a)))
print("\nMembership test")
print("1 in a  # Test if a includes 1")
print(1 in a)
print("1 not in a  # Test if a doesn't include 1")
print(1 not in a)

print("\nx, y, z = a  # Define variables from a list" )
x, y, z = a
print("values of x, y, z = {}, {}, {}".format(x,y,z))
print("Caution: Number of variables must be same to list length!")
print("\nPress Enter to continue... (1)\n")
input("----------------------------------------\n")

print("\n2. List operation")
print("a = {}".format(a))
print("a+a = {}".format(a+a))
print("a*3 = {}".format(a*3))
print(": Same to string; other operators are not defined.")
print("\nPress Enter to continue... (2)\n")
input("----------------------------------------\n")

print("\n3. List copy")
print("a = {}".format(a))
print("b = a")
b = a
print("b = {}".format(b))

print("\nb[0] = 0  # Change element of 'b'")
b[0] = 0
print("a = {}".format(a))
print("b = {}".format(b))

print("\na[0] = 1  # Change element of 'a'")
a[0] = 1
print("a = {}".format(a))
print("b = {}".format(b))
print("---> 'b = a' doesn't make a copy, but 'b' shares the memory location assigned to 'a'")
input("\nPress Enter to continue... (3-1)\n")

print("c = a.copy(); c[0] = -1  # Change element of 'c'\n")
c = a[:]; c[0] = -1
print("a = {}".format(a))
print("c = {}".format(c))
print("""
Cf. Other copy methods for List
c = a[:]  # Slicing all elements --> #7
c = list(a)  # New list object""")
print("\nPress Enter to continue... (3-2)\n")
input("----------------------------------------\n")


### Popular list methods
### append(), insert(), remove(), index(), pop(), sort()
### and some intrinsic fuctions(len(), max(), min(), etc.)
print("\n4. List method(1): append and insert")
print("a = {}".format(a))
print("a.append(10)  # Caution: 'a=a.append(10)' doesn't work!")
a.append(10)
print("a = {}".format(a),"\n")

print("a.append(['abc','efg'])")
a.append(['abc','efg'])
print("a = {}".format(a),"\n")

print("How to access the element of list in list:")
print("a[-1] = {}".format(a[-1]))
print("a[-1][0] = {}".format(a[-1][0]))
input("\nPress Enter to continue... (4-1)\n")

print("a = {}".format(a))
print("a.insert(1, -99.9)")
a.insert(1, -99.9)
print("a = {}".format(a))
print("a.insert(-1, -99.9)")
a.insert(-1, -99.9)
print("a = {}".format(a))
print("a.insert(len(a), -99.9)")
a.insert(len(a), -99.9)
print("a = {}".format(a))
print("\nPress Enter to continue... (4-2)\n")
input("----------------------------------------\n")

print("\n5. List method(2): index, del, remove (and pop)")
print("a = {}".format(a))
print("a.index('abc')")
print(a.index('abc'))
print("a[a.index('abc')]")
print(a[a.index('abc')])
print("\na.index(-99.9)")
print(a.index(-99.9))
print("---> Return the index of first item")
input("\nPress Enter to continue... (5-1)\n")

print("a = {}".format(a))
print("del a[0]  # Remove by index")
del a[0]
print("a = {}".format(a))
print("Cf. 'a.pop[0]' also remove the item at index 0, AND return the removed item \n")
print("a.remove(-99.9)  # Remove by value")
a.remove(-99.9)
print("a = {}".format(a))
print("---> Remove the first value")
print("\nPress Enter to continue... (5-2)\n")
input("----------------------------------------\n")

print("\n6. List method(3): count and sort")
print("d = [1,5,2,4,3,1]  # Define a list")
d = [1,5,2,4,3,1]
print("d.count(1)  # How many times the value occurs")
print(d.count(1))
print("d.sort()  # Working in-place, i.e. no return")
d.sort()
print("d = {}".format(d))
print("\nPress Enter to continue... (6)\n")
input("----------------------------------------\n")

print("\n7. List method(4): slicing")
print("d = {}".format(d))
print("d[1:3] = {}  # [start:end(not including):1]".format(d[1:3]))
print("d[::2] = {}  # = d[0:len(d):2]".format(d[::2]))
print("d[1::2] = {}".format(d[1::2]))
print("d[::-1] = {}  # Flip the order, = d[-1:None:-1]".format(d[::-1]))

print("\nCf. 'None': a keyword to define a null value")
print("d[None:4] = {}  # = d[:4]".format(d[None:4]))
print("d[-4:None] = {}  # = d[-4:]".format(d[-4:None]))
print("\nPress Enter to continue...(7)\n")
input("----------------------------------------\n")

print("\n8. Some built-in functions of python")
print("e = [1,5,2,4,3]  # Define a list")
e = [1,5,2,4,3]
print("sorted(e) = {}".format(sorted(e)))
print("Still, e = {} \n".format(e))
print("min(e), max(e), sum(e) = {}, {}, {}".format(min(e), max(e), sum(e)))
print("mean = sum(e)/len(e) = {}".format(sum(e)/len(e)))

print("""
'eval' function: evaluate string as a python variable
x1= 1
x2= 10
x3= 'a'
xx= [eval('x{}'.format(i)) for i in range(3)]  # Same as xx=[x1,x2,x3]""")
x1= 1
x2= 10
x3= 'a'
xx= [eval('x{}'.format(i)) for i in range(3)]  # Same as xx=[x1,x2,x3]
print(xx)

input("\nPress Enter to continue... (8-1)\n")

print("'map' function: map(func, iter); apply func to each member of iter")
f= map(str,e)
print("f = map(str,e); f = {} \n".format(f))
print(" '1' in f  # Membership test")
print('1' in f,"\n")
print("f = list(map(str,e))  # Transform map object to list")
f = list(map(str,e))
print("f = {}".format(f))

print("\ng = list(map(float,f))")
g = list(map(float,f))
print("g = {}".format(g))

print("\ng2 = [float(val) for val in f]  # Result in the same output")
g2 = [float(val) for val in f]
print("g2 = {}".format(g2))
print("Cf. Details of 'for' loop are in A04")
print("\nPress Enter to continue... (8-2)\n")
input("----------------------------------------\n")

print("\n9. Miscellaneous")
print("For a list, h = [1,2,'a']")
h = [1,2,'a']
print("h vs. *h")
print(h)
print(*h)

print('''
Sometimes it is convenient:
print("{}, {}, {}".format(h[0],h[1],h[2]))
print("{}, {}, {}".format(*h))
''')
print("{}, {}, {}".format(h[0],h[1],h[2]))
print("{}, {}, {}\n".format(*h))

print("----------\n")

print("h = 'abcdef'")
h = 'abcdef'
print("list(h) = {}".format(list(h)))

print("\nh = 12345")
h = 12345
try:
    print("try list(h)  # Try to apply 'list' function to int")
    list(h)
except Exception as err:
    print("Error message\n:",err)

print("\nPress Enter to continue... (9)\n")
input("----------------------------------------\n")

print("THE END: Python Basic Part2 - List\n")
