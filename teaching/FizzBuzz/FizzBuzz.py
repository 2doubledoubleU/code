class Solution:

	def run(self, N, M):
		
		if not (isinstance(N,int) and isinstance(M,int) and M>=N):
			sequence = "Please supply two integers as inputs, where M is greater or equal to N"
		else:
			sequence = ""
		
			for number in range (N,M+1):
				if (number % 15 == 0):
					sequence += "FizzBuzz,"
				elif (number % 3 == 0): 
					sequence += "Fizz,"
				elif (number % 5 == 0): 
					sequence += "Buzz,"
				else:
					sequence += str(number) + ","
					
			sequence = sequence[:-1]				
			
		return sequence
