with open('input.txt', 'r') as file:
	wire = file.readlines()

wire1 = wire[0].split(',')
wire2 = wire[1].split(',')

def coords(wires):
	coordinates = [(0,0)] 
	
	for wire in wires:

		direction = wire[0]
		length = int(wire[1:])
		x = coordinates[-1][0]
		y = coordinates[-1][1]

		if (direction == 'U'):
			coordinates.append((x,y+length))
		elif (direction == 'D'):
			coordinates.append((x,y-length))
		elif (direction == 'L'):
			coordinates.append((x-length,y))
		elif (direction == 'R'):
			coordinates.append((x+length,y))
		else:
			input("broken")
			break
	return coordinates

wireOne = []
wireTwo = []

for i, each in enumerate(coords(wire1)):
	wireOne.append(each[i%2-1])

for i, each in enumerate(coords(wire2)):
	wireTwo.append(each[i%2-1])

print(wireOne[0:5])
print(wireTwo[0:5])


if ((wire1[1][0] == 0 and wire2[1][0] == 0) or (wire1[1][1] == 0 and wire2[1][1] == 0)):
	adjust = 1
else:
	adjust = 0