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

autograder = Autograder(llm_model=MODEL)

autograder.set_rubric([
    ("States that p-value is less than 0.05", 1),
    ("States that the null hypothesis is rejected", 1),
])

student_response = """
A p-value of 0.03 means that the alternative hypothesis is rejected, and the null is accepted.
"""

print(autograder.evaluate(student_response))
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