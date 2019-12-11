#for num in range (272091,815433):

for num in range (0,100):
	stringed = str(num)
	for i,each in enumerate(stringed):
		for each2 in stringed[i+1:]:
			if int(each2) < int(each):
				print(stringed)
				continue
		if i>0:
			if i

