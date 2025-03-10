## Summate AI

A Python application that uses locally-run LLMs, through Ollama, to evaluate student responses against provided rubrics.

This project ensures privacy by running completely offline, and is designed to provide consistent, objective evaluations while reducing the manual workload for educators.

### Requirements
* Python 3.13
* LM Studio (we will be performing API calls to a locally hosted server, interfaced by LM Studio)
* Dependencies listed in `pyproject.toml`

### Setup
1. Download and install LM Studio
2. Pull model, in our `config.py`, it is set to `meta-llama-3.1-8b-instruct` by default:
```cli
lms get meta-llama-3.1-8b-instruct
```
3. Load model
```cli
lms load meta-llama-3.1-8b-instruct
```
4. Start server
```cli
lms server start
```