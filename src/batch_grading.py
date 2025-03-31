# This script will demo how to batch grade.

from backend.call_llm import Autograder
from config import MODEL

# Here are the student responses we want to grade.
# We organize them into a list.

student_responses = [
    "A p-value of 0.03 means that the alternative hypothesis is rejected, and the null is accepted.",
    "Since p is less than alpha, the null is rejected.",
]

def main():

    # We initialize the model
    autograder = Autograder(llm_model=MODEL)

    # Then we update the rubric
    autograder.set_rubric([
        ("States that p-value is less than 0.05", 1),
        ("States that the null hypothesis is rejected", 1),
    ])

    # We can optionally update the temperature
    autograder.set_temperature(0.5)

    # We initialize an empty list to store the evaluations.

    evaluations = []

    # We intend to create a list of dictionaries so we can store information
    # on response ID and the evaluation.

    # We can now set up a for loop to iterate through the student responses
    for i, response in enumerate(student_responses):
        data = {'id': i, 'evaluation': autograder.evaluate(response)}
        evaluations.append(data)

    # We can now print out the results:
    print(evaluations)

if __name__ == "__main__":
    main()