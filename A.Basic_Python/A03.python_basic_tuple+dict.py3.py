###--- Tuple
g=(1,2,3)
print("\ng={} type={}".format(g,type(g)))
# g[0]=10 ### This causes an error because Tuple prohibits assignment
# g.append(4) ### Of course, no modification

###--- Dictionary
h = {"brand": "Ford", "model": "Mustang", "year": 1964 }
print("h={} type={}".format(h,type(h)))
print(h["year"])  ### Access value by key
