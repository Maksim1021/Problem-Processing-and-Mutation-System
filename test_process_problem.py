import unittest
from mutations import mutate_problem
from problem import Problem

class TestMutation(unittest.TestCase):
    
    def test_rephrase_mutation(self):
        problem = Problem(id=1, statement="Create a function that calculates the factorial of a number using recursion.")
        mutated_problem = mutate_problem(problem, "rephrase")
        self.assertNotEqual(mutated_problem.statement, problem.statement)
    
    def test_expand_mutation(self):
        problem = Problem(id=2, statement="Design an algorithm to find the longest common subsequence in two strings.")
        mutated_problem = mutate_problem(problem, "expand")
        self.assertTrue(len(mutated_problem.statement) > len(problem.statement))

    def test_simplify_mutation(self):
        problem = Problem(id=3, statement="Write a function that merges two sorted lists into one sorted list.")
        mutated_problem = mutate_problem(problem, "simplify")
        self.assertTrue("easy" in mutated_problem.statement.lower())  # Assuming simplified problem will be easier to understand

    def test_mutation_score(self):
        problem = Problem(id=4, statement="Create a class-based system to manage a library of books.")
        mutated_problem = mutate_problem(problem, "add_constraints")
        score = mutated_problem.mutation_score
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
if __name__ == '__main__':
    unittest.main()
