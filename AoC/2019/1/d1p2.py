import math

with open('input.txt', 'r') as file:
	modules = file.readlines()

def getFuel(weight):
	return math.floor(weight/3) - 2

def getFuelRecursive(weight):
	if weight <=8:
		return 0
	else:
		fuel = getFuel(weight)
		return fuel + getFuelRecursive(fuel)

totalFuel = 0
for weight in modules:
	totalFuel += getFuelRecursive(int(weight))

print(totalFuel)