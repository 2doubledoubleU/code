a = [2,2,10,5,4,6,7,5,8,8,6,4,7]

l = len(a)
a.sort()

single = a[l-1]

for pos in range(1,len(a)-1,2):
	if not a[pos] == a[pos-1]:
		single = a[pos-1]
		break

input(single)