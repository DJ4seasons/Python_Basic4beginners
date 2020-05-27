'''
Python Basic(2)
: List

By Daeho Jin
'''


###---- List
print("\n*** List ***")
### List basic
print("\n1. Define a list with []")
print("a = []  # Define an empty list" )
a = []
print("len(a) = {}:\ttype(a) = {}".format(len(a),type(a)))

print("\na = [1, 'abc', 3.141592]  # Define a list" )
a = [1, 'abc', 3.141592]
print("len(a) = {}:\ttype(a) = {}".format(len(a),type(a)))
print("\nMembership test")
print("1 in a ?")
print(1 in a)

print("\nx, y, z = a  # Define variables from a list" )
x, y, z = a
print("values of x, y, z = {}, {}, {}".format(x,y,z))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2. List operation")
print("a+a = {}".format(a+a))
print("a*3 = {}".format(a*3))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n3. List copy")
print("a = {}".format(a))
print("b = a; b[0] = 0  # Change element of 'b'\n")
b = a; b[0] = 0
print("a = {}".format(a))
print("b = {}".format(b))

print("\na[0] = 1  # Change element of 'a'\n")
a[0] = 1
print("a = {}".format(a))
print("b = {}".format(b))
print("---> 'b' is not a copyt of 'a' but they share the same memory location")
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("c = a[:]; c[0] = -1  # Change element of 'c'\n")
c = a[:]; c[0] = -1
print("a = {}".format(a))
print("c = {}".format(c))
print("---> By slicing, 'c' becomes independent of 'a'")
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")


### Popular list methods
### append(), insert(), remove(), index(), pop(), sort()
### and some intrinsic fuctions(len(), max(), min(), etc.)
print("\n4. List method(1): append and insert")
print("a = {}".format(a))
print("a.append(10)")
a.append(10)
print("a = {}".format(a),"\n")

print("a.append(['abc','efg'])")
a.append(['abc','efg'])
print("a = {}".format(a),"\n")

print("Access the element of list in list")
print("a[-1] = {}".format(a[-1]))
print("a[-1][0] = {}".format(a[-1][0]))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

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
input("\nPress Enter to continue...\n")
print("How about 'b' now?")
print("b = {}".format(b),"\n")

print("\n5. List method(2): index, del, remove (and pop is not introduced...)")
print("a = {}".format(a))
print("a.index(10)")
print(a.index(10))
print("a[a.index(10)]")
print(a[a.index(10)])
print("\na.index(-99.9)")
print(a.index(-99.9))
print("---> Return the index of first item")
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("a = {}".format(a))
print("del a[0]  # Remove by index")
del a[0]
print("a = {}".format(a))
print("a.remove(-99.9)  # Remove by value")
a.remove(-99.9)
print("a = {}".format(a))
print("---> Remove the first value")
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n6. List method(3): count, sort, and slicing")
print("d = [1,5,2,4,3,1]  # Define a list")
d = [1,5,2,4,3,1]
print("d.count(1)  # How many the value occurs")
print(d.count(1))
print("d.sort()  # Working in-place")
d.sort()
print("d = {}".format(d))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("d[::2] = {}  # = d[0:len(d):2]".format(d[::2]))
print("d[1::2] = {}".format(d[1::2]))
print("d[::-1] = {}  # Flip the order".format(d[::-1]))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n7. Some built-in functions of python")
print("e = [1,5,2,4,3]  # Define a list")
e = [1,5,2,4,3]
print("sorted(e) = {}".format(sorted(e)))
print("min(e), max(e), sum(e) = {}, {}, {}  # but no 'mean'".format(min(e), max(e), sum(e)))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("map function: map(func, iter); apply func to each member of iter")
print("map(str,e) = {}".format(map(str,e)))
print("f = list(map(str,e))  # Transform map object to list")
f = list(map(str,e))
print("f = {}".format(f))

print("\ng = list(map(float,f))")
g = list(map(float,f))
print("g = {}".format(g))

print("\ng2 = [float(i) for i in f]  # Result in the same output")
g2 = [float(i) for i in f]
print("g2 = {}".format(g2))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\nLastly,")
print("h = 'abcdef'")
h = 'abcdef'
print("list(h) = {}".format(list(h)))

print("\nh = 12345")
h = 12345
print("[h] = {}".format([h]))
try:
    print("try list(h)  # Try to apply 'list' function to int")
    list(h)
except Exception as err:
    print("Error message\n:",err)

input("\nPress Enter to continue...\n")
print("THE END")
