#Linear search 
#Linear search does not require the list to be sorted 
#However linear search is more time consuming as it goes through each element one after the other
L= eval(input("enter a list "))
x=int(input("enter the element to be serched for"))
for i in range(0,len(L)):
    if x==L[i]:
        pos=i+1
        print("element found at position", pos)
        break
else:
    print("element not found")
