'''
Python Basic Part1
: Data Types
: Print Format

By Daeho Jin
'''

### Part0: Assignment
print("\n*** Before Start ***\n")
print("1. Allowed letters for Python variable name")
print(": Alphabet, lowcase or uppercase (a-z, A-Z; case-sensitive)")
print(": Digit (0-9)")
print(": Underscore (_)")
print("\n - Caution")
print(": Digit can not be the first letter.")
print(": Pre-existing function names should be avoided.")
print(":: (possible but not recommended, e.g. int, max, sum, etc.)")
print(": Conventionally lowercases are preferred to uppercases")
print(":: (e.g., myName or my_name) \n")

print("\n2. Assignment: left = right")
print(": It means value 'right' is assigned to variable 'left'")
print("\nFor example, ")
print("a = 1")
print("a, b, c = 1,2,3")
a,b,c= 1,2,3; print(a,b,c)
print("a = b = 1")
a=b=1; print(a,b)
print("\nPress Enter to continue... (0)\n")
input("----------------------------------------\n")

### Part1: Data Types
print("\n*** Data Types + Print Format ***")
print("!!! Data Type is defined when a value is assigned !!!")
### Integer and float numbers
print("\n1. Integer and float numbers\n")
a=17
b=7
print("a = {}:\ttype = {}".format(a,type(a)))
print("b = {}:\ttype = {} \n".format(b,type(b)))
print("c = a+b")
c=a+b
print("c = {}:\ttype = {} \n".format(c,type(c)))
print("c = a/b")
c=a/b
print("c = {}:\ttype = {}  # Basically 8-Byte (64bit)\n".format(c,type(c)))

print("Cf. floor divider, //")
print("d = a//b; d2= float(a)//b \n")
d=a//b; d2= float(a)//b
print("d = {}:\ttype = {}".format(d,type(d)))
print("d2 = {}:\ttype = {} \n".format(d2,type(d2)))

print("Ref. Arithmetic Operators: +, -, *, /, %, **, // ")
print("\nPress Enter to continue... (1)\n")
input("----------------------------------------\n")

### String
print("\n2. String examples\n")
print("str1, str2= 'abc1#', \"abc!2\"")
str1,str2= 'abc1#', "abc!2"
print(str1,str2,"\n")
print("d = str(c)  # Change type from float to string; c.f., int(), float()")
d=str(c)
print("d = {}:\ttype = {}\n".format(d,type(d)))
print("len(d), d[0:4], d[-3:]  # Python index starts at 0; start to end(not including)")
print("{}, {}, {}\n".format(len(d),d[0:4],d[-3:]))
print("c+c vs. d+d[:5] vs. d*2")
print("{} vs. {} vs. {}\n".format(c+c,d+d[:5],d*2))
print("len(d*3)")
print(len(d*3))
print("\nPress Enter to continue... (2)\n")
input("----------------------------------------\n")

### Printing unicode
print("\n3. Unicode example\n")
print("El Ni\u00F1o and La Ni\u00F1a \n")
print("Delta: {}, epsilon: {}, degree: {} \n".format('\u0394','\u03B5','\u00B0'))
print("Subscript: x{}, x{}, x{} \n".format('\u2081','\u2082','\u2090'))
print("Superscript: x{}, x{}, x{} \n".format('\u00B9','\u00B2','\u1D43'))
print("""
### FYI, Matplotlib supports TeX markup for easier numerical expressions
### https://matplotlib.org/stable/tutorials/text/mathtext.html
""")
print("\nPress Enter to continue... (3)\n")
input("----------------------------------------\n")

### Boolean
print("\n4. Boolean type\n")
print("boo1, boo2 = True, False")
boo1, boo2 = True, False
print("boo1 = {}:\ttype = {} \n".format(boo1,type(boo1)))
print("Value of {} and {}:".format(boo1,boo2))
print(int(boo1),int(boo2),'\n')
print("{}+{} = {}".format(boo1,boo2,boo1+boo2))
print("{}+{} = {}".format(boo1,boo1,boo1+boo1))
print("{}-{} = {} \n".format(boo2,boo2,boo2-boo2))
print("{} 'and' {} = {}".format(boo1,boo2,boo1 and boo2))
print("{} 'or' {} = {}".format(boo1,boo2,boo1 or boo2))
print("'not' {} = {} \n".format(boo1, not boo1))

print("bool(-1) = {}, bool(0) = {}, bool(1) = {}, bool(2) = {}".format(bool(-1),bool(0),bool(1),bool(2)))
print("bool(-0.1) = {}, bool(0.) = {}, bool(0.1) = {}".format(bool(-0.1),bool(0.),bool(0.1)))
print("---> Value zero(0) is False, and all others are True \n")

print("""a = 2
a = bool(a)
a = int(a)
print(a)""")
a = 2; a = bool(a); a = int(a); print(a)
print("\nPress Enter to continue... (4)\n")
input("----------------------------------------\n")

### Print format
print("\n5. Print format examples")
print("cf. https://pyformat.info/ \n")
print("a, b, c = 1, 2, 3.666667")
a, b, c = 1, 2, 3.666667

print("\nInteger")
format_test1 = '{}, {:d}, {:3d}, {:03d}'
print(format_test1)
print(format_test1.format(a,a,a,a))

print("\nFloat")
format_test2 = '{}, {:.0f}, {:.3f}, {:7.3f}, {:07.3f}'
print(format_test2)
print(format_test2.format(c,c,c,c,c))
input("\nPress Enter to continue... (5-1)\n")

print("\nIn case of input order= {}, {}, {}".format(a,b,c))
format_test2 = '{1:d}, {2:.2f}, {0:.1f}, {0:d}'
print('\n'+format_test2+' # We have only 3 inputs!')
print(format_test2.format(a,b,c))
print("cf. int-->{:.1f} (o), float-->{:d} (error)")

format_test3 = '{:d}, {other:.2f}, {:.1f}'
print('\n'+format_test3)
print(format_test3.format(a,b,other=c))
print("Keyword must be at the end")

print("\nHow about multi-lines? Use tripple quote mark!")
multi_lines='''
Hello, my name is {name}.
I am {age:d} years old.
My favorite food is {food}
'''
print(multi_lines)
keywords={"name":"Dave", "age":25, "food":"chococake"}  # This is dictionry!
print(keywords, type(keywords))
dict = { "a": "India","b": "USA")
keywords.update(dict) #To add the 'dict' dictionary to the keywords dictionary 
print(multi_lines.format(**keywords))  # two stars: distribute items of "key:value"
print("\nPress Enter to continue... (5-2)\n")
input("----------------------------------------\n")
List = ['apples','bananas','oranges','strawberry'] # This is a list 
Num_List = [ 1,2,3,4,5,6,7,8,9] # A list of numbers can also be made, a list of both strings and integers can be made 
Tup = ('football','basketball','volleyball','cricket') #This is a tuple, it is similar to a list but it cannot be mutated/edited
inp_list = eval(input("enter a list/tuple")) # A list or a tuple can be made using eval 

print("THE END: Python Basic Part1 - Data Types and Print Format\n")
