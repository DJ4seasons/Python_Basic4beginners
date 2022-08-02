#Bubble sort
L= eval(input("enter a list))
print("The unsorted list is",L)
l=len(L)
for y in range(0,l):
    for x in range(0,l-1):
        if L[x]>L[x+1]:
            L[x],L[x+1]=L[x+1],L[x]
print("sorted list is", L)

#Insertion sort
L1=eval(input("enter a list))
print("unsorted lsi is",L1)
l1=len(L1)
for i in range(1,l1):
    key=L1[i]
    j=i-1
    while j>=0 and key<L1[j]:
        L1[j+1]=L1[j]
        j=j-1
    else:
        L1[j+1]=key
print("sorted list is", L1)             
