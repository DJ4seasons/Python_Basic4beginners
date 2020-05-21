###---- List
print("\n*** List ***")
### List basic
print("\n1. Define a list with []")
print("a = [1, 'abc', 3.141592]  # Define a list" )
a = [1, 'abc', 3.141592]
print("a = {}:\ttype = {}".format(a,type(a)))
print("\n2. List operation")
print("a+a = {}".format(a+a))
print("a*2 = {}".format(a*2))
input("\nPress Enter to continue...\n")

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

print("c = a[:]; c[0] = -1  # Change element of 'c'\n")
c = a[:]; c[0] = -1
print("a = {}".format(a))
print("c = {}".format(c))
print("---> By slicing, 'c' becomes independent of 'a'")
input("\nPress Enter to continue...\n")


### Popular list methods
### append(), insert(), remove(), index(), pop(), sort()
### and some intrinsic fuctions(len(), max(), min(), etc.)
print("\n4. Some methods of list")
e.append(1)
e.append('abc')
e.append(['abc','efg'])
print("\n After appending")
print(e)
print(e[-1][0])
print("\n")

print("* e.insert(1,1)")
e.insert(1,1)
print(e)
print("* e.index(1)")
print(e.index(1))
print("* e.index('abc')")
print(e.index('abc'))
print("\n")

print("* e[:5].sort()")
# e.sort()   ### This causes an error because strs and numbers are mixed in
f=e[:5]
f.sort()
print(f,sorted(e[:5]))
print("* min, max, sum")
print(min(e[:5]),max(e[:5]),sum(e[:5]))
print("\n")

print("* Slicing")
print(e)
print(e[::2]) ### = e[0:len(e):2]
print(e[::-1])
print("\n")

print("* Map(func, iter)")
aa=['abc','def','ghi']
bb=list(map(list,aa))
print(aa)
print("list(map(list,aa))=",bb)
print(list(aa[0]))
cc=list(range(5))
dd=list(map(float,cc))
print(cc)
print("list(map(float,cc))",dd)
