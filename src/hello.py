from backend.call_llm import Autograder
from config import MODEL

autograder = Autograder(llm_model=MODEL)

autograder.set_rubric([
    ("States that p-value is less than 0.05", 1),
    ("States that the null hypothesis is rejected", 1),
])

student_response = """
A p-value of 0.03 means that the alternative hypothesis is rejected, and the null is accepted.
"""

print(autograder.evaluate(student_response))