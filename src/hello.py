from backend.call_llm import Autograder
from config import MODEL

# We initialize the model
autograder = Autograder(llm_model=MODEL)

# Then we update the rubric
autograder.set_rubric([
    ("States that p-value is less than 0.05", 1),
    ("States that the null hypothesis is rejected", 1),
])

# We can optionally update the temperature
autograder.set_temperature(0.5)

student_response = """
A p-value of 0.03 means that the alternative hypothesis is rejected, and the null is accepted.
"""

# We can now ask the autograder to grade a student response
evaluation = autograder.evaluate(student_response)
print(evaluation)