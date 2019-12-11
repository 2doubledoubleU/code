with open('input.txt', 'r') as file:
	csv = file.read()

intcode = csv.split(',')
i = list(map(int, intcode))

i[1] = 12 
i[2] = 2

p = 0
while True:
	if (i[p] == 99):
		break
	elif (i[p] == 1):
		i[i[p+3]] = i[i[p+1]] + i[i[p+2]]
	elif (i[p] == 2):
		i[i[p+3]] = i[i[p+1]] * i[i[p+2]]
	else:
		input("broken")
		break
	p += 4

input(i[0])