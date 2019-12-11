import math

with open('input.txt', 'r') as file:
	modules = file.readlines()

def getFuel(weight):
	return math.floor(weight/3) - 2

totalFuel = 0
for weight in modules:
	totalFuel += getFuel(int(weight))

print(totalFuel)