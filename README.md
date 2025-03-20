## Summate AI

A Python application that uses locally-run LLMs, through Ollama and LangChain, to evaluate student responses against provided rubrics.

This project ensures privacy by running completely offline, and is designed to provide consistent, objective evaluations while reducing the manual workload for educators.

### Requirements
* Python 3.13
* Ollama
* Dependencies listed in `pyproject.toml`

### Usage

Try the autograder out at `src/hello.py`. Replace the rubric components as a list of tuples `(component, score)`, and update the student response. Run the script! Your wait time will vary depending on how archaic your computer is.

```python
from backend.call_llm import Autograder
from config import MODEL

# We initialize the model
autograder = Autograder(llm_model=MODEL)

# Then we update the rubric
autograder.set_rubric([
    ("States that p-value is less than 0.05", 1),
    ("States that the null hypothesis is rejected", 1),
])

# We can optionally update the temperature. This will default to whatever the temperature is set at in config.py
autograder.set_temperature(0.5)

student_response = """
A p-value of 0.03 means that the alternative hypothesis is rejected, and the null is accepted.
"""

# We can now ask the autograder to grade a student response.
# This student seems to have confused the null with the alternative hypothesis.
evaluation = autograder.evaluate(student_response)
print(evaluation)
```

This outputs:

```
# CRITERION: States that p-value is less than 0.05
EXPLANATION: The student's response does not meet this criterion because they state that the alternative hypothesis is rejected when the p-value is 0.03, which implies the null hypothesis is true (since it doesn't indicate a significant result). However, this misunderstanding of how to interpret results can be seen as failing to directly address whether the p-value is less than 0.05.
SCORE: 0/1

# CRITERION: States that the null hypothesis is rejected
EXPLANATION: The student's response does not meet this criterion because they state that the alternative hypothesis is rejected, and the null is accepted when a p-value of 0.03 is obtained. This shows confusion about how to interpret the results in relation to rejecting or accepting the null hypothesis.
SCORE: 0/1

# TOTAL_SCORE: 0/2
```

### Setup
1. Download and install [Ollama](https://ollama.com/)
2. Check that installation is successful by checking version
```cli
ollama --version
```
3. Pull model (browse through all the models at your disposal [here](https://ollama.com/search)). We recommend pulling `llama3.1:8b`:
```cli
ollama pull llama3.1:8b
```
4. (Optional) If you pulled another model, update the `MODEL` constant in `src/config.py`
5. Success!