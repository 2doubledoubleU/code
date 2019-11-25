import unittest
from FizzBuzz import Solution

class SolutionMethods(unittest.TestCase):
	##
	## /!\ Unit Tests are optional but highly recommended /!\
	##
	# First Example
	##
	#def test_example(self):
	#	self.assertEqual("this is an example", "this is an example")

	def test_run(self):
		solution = Solution()
		self.assertEqual(solution.run(1.2,5), "Please supply two integers as inputs, where M is greater or equal to N")
		
	def test_run2(self):
		solution = Solution()
		self.assertEqual(solution.run(-1.0,5), "Please supply two integers as inputs, where M is greater or equal to N")
	
	def test_run3(self):
		solution = Solution()
		self.assertEqual(solution.run(1,"A"), "Please supply two integers as inputs, where M is greater or equal to N")
		
	def test_run4(self):
		solution = Solution()
		self.assertEqual(solution.run("1",2), "Please supply two integers as inputs, where M is greater or equal to N")
		
	def test_run4(self):
		solution = Solution()
		self.assertEqual(solution.run(1,-1), "Please supply two integers as inputs, where M is greater or equal to N")

	def test_run5(self):
		solution = Solution()
		self.assertEqual(solution.run(1,1), "1")

if __name__ == "__main__":
	unittest.main()