from langchain_ollama import OllamaLLM
from langchain_core.prompts.prompt import PromptTemplate
from typing import Optional

# The following is meant to resolve any import issues. It's not ↵
# important for the project:

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import MODEL, TEMPERATURE, PROMPT_TEMPLATE

SUPPORTED_LLM_HOSTS = ['ollama']

class Autograder:

    def __init__(self, llm_host: str = "ollama", llm_model: Optional[str] = None):

        self.rubric_components = []
        self.temperature = TEMPERATURE
        self.llm_host = str(llm_host)
        self.llm_model = llm_model
        self.prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

        if self.llm_host not in SUPPORTED_LLM_HOSTS:
            raise ValueError(f"{self.llm_host} not supported. Current supported hosts include: {SUPPORTED_LLM_HOSTS}.")
        else:
            if self.llm_host.lower() == 'ollama' and self.llm_model:
                self.model = OllamaLLM(model=self.llm_model)

            elif self.llm_host.lower() == 'ollama':
                raise ValueError("No LLM model provided. Please provide an LLM model when initializing Autograder.")

    def set_rubric(self, components):
        """Set rubric components for evaluation.
        
        Args:
            components (List[Tuples[rubric: str, score: int]]: A list of tuples, each containing the rubric and associated score
        """

        self.rubric_components = components

        parsed_components = ""
        for criterion, score in self.rubric_components:
            parsed_components += f"{criterion} (+{score} point{'s' if score > 1 else ''})\n"

        self.prompt = self.prompt.partial(rubric_components=parsed_components)
    
    def set_temperature(self, temperature: float):
        """Set temperature for autograder.
        
        Args:
            temperature (float): A temperature ranging between 0 and 1, where 0 is the most deterministic, and 1 is the most stochastic
        """
        if temperature < 0 or temperature > 1:
            raise ValueError(f"Temperature should be within 0 to 1. Your temperature was set to: {temperature}")
        else:
            self.temperature = temperature
    
    def evaluate(self, student_response):
        """Evaluate a student response based on rubric set using set_rubric method.

        Args:
            student_response (str): A string containing the student response

        Returns:
            Dictionary with evaluation results
        """

        if not self.rubric_components:
            return {"error": "Rubric components are not set. Use set_rubric method first to set the rubrics."}

        self.prompt = self.prompt.format_prompt(student_response=student_response)

        response = self.model.invoke(self.prompt)
        
        return response

if __name__ == "__main__":

    autograder = Autograder(llm_model=MODEL)

    autograder.set_rubric([
        ("States that p-value is less than 0.05", 1),
        ("States that the null hypothesis is rejected", 1),
    ])

    student_response = """
    A p-value of 0.03 means that the alternative hypothesis is rejected, and the null is accepted.
    """

    print(autograder.evaluate(student_response))