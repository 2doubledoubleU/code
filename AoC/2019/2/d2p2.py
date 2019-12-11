with open('input.txt', 'r') as file:
	csv = file.read()

intcode = csv.split(',')
intcode = list(map(int, intcode))

def runCode(intcode, noun, verb):
	i = list.copy(intcode)
	i[1] = noun
	i[2] = verb
	p = 0
	while True:
		if (i[p] == 99):
			break
		elif (i[p] == 1):
			i[i[p+3]] = i[i[p+1]] + i[i[p+2]]
		elif (i[p] == 2):
			i[i[p+3]] = i[i[p+1]] * i[i[p+2]]
		else:
			return(0)
		p += 4

	return(i[0])

for noun in range(0, 100):
	for verb in range(0, 100):
		if (runCode(intcode,noun,verb) == 19690720):
			print(f'noun ={noun}, verb ={verb}')
			input(100*noun + verb)
			break