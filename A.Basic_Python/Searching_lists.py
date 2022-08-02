#Binary Search 
#This involves the list to be ordered 
L=[11,13,15,17,19,21,23] #An ordered list 
l=len(L)#length of the list 
beg= 0
end=l-1
key=int(input("enter element to be searched for"))
while beg<=end:
    mid = (beg+end) // 2
    if L[mid] < key:
        beg = mid + 1
    elif L[mid] > key:
        end = mid - 1
    else:
        p= mid 
        break
else:
    p=-1

if p==-1:
    print("The element was not found")
else:
    print("The element found at position",p+1)
