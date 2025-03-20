## Summate AI

A Python application that uses locally-run LLMs, through Ollama and LangChain, to evaluate student responses against provided rubrics.

This project ensures privacy by running completely offline, and is designed to provide consistent, objective evaluations while reducing the manual workload for educators.

### Requirements
* Python 3.13
* Ollama
* Dependencies listed in `pyproject.toml`

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