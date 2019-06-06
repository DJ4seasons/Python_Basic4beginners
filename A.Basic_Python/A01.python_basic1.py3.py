'''
Python Basic(1)
1. Data Type
2. List, Tuple, Dictionary
'''

print("*** Data Type ***")
### Integer and float numbers
a=17
b=7
c=a/b
print("a={} type={}".format(a,type(a)))
print("b={} type={}".format(b,type(b)))
print("c={} type={}".format(c,type(c)))
print("\n")

format_test = '{}, {:d}, {:02d}, {:03d}, {:.2f}'.format(a,a,a,b,c)
print(format_test)
print("\n")

### String
d=str(c)
print("d={} type={}".format(c,type(d)))
print(len(d),d[0:4],d[-3:])
c+=c  ## c=c+c
print(c)
d+=d  ## d=d+d
print(d)
print(len(d))
print("\n")

### Printing unicode
print("Unicode Test")
print("El Ni\u00F1o")
print("Delta: {}, epsilon: {}, degree: {}".format('\u0394','\u03B5','\u00B0'))
print("\n")

### Boolean
boo1, boo2 = True, False
print("boo1={} type={}".format(boo1,type(boo1)))
print("Value of bools")
print(int(boo1),int(boo2))
print("True+False=",boo1+boo2)
print("True and False=",boo1 and boo2)
print("bool(-1)={}, bool(0)={}, bool(1)={}, bool(2)={}".format(bool(-1),bool(0),bool(1),bool(2)))
print("bool(-0.1)={}, bool(0.)={}, bool(0.1)={}".format(bool(-0.1),bool(0.),bool(0.1)))
print('\n')

###---- List
print("*** List ***")
e=[a,b,c]
print("e={} type={}".format(e,type(e)))
print("e+e={}".format(e+e))
print("\n This is not a copy")
e2=e
e2[0]=5
print(e)
e3=e[:]
e3[0]=4
print(e)
print(e3)

### Popular list methods
### append(), insert(), remove(), index(), pop(), sort() 
### and some intrinsic fuctions(len(), max(), min(), etc.)
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

###--- Tuple
g=(1,2,3)
print("\ng={} type={}".format(g,type(g)))
# g[0]=10 ### This causes an error because Tuple prohibits assignment 
# g.append(4) ### Of course, no modification

###--- Dictionary
h = {"brand": "Ford", "model": "Mustang", "year": 1964 }
print("h={} type={}".format(h,type(h)))
print(h["year"])  ### Access value by key



