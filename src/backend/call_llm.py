import json
import lmstudio as lms

# The following is meant to resolve any import issues. It's not ↵
# important for the project:

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import MODEL, TEMPERATURE

## STRUCTURED OUTPUT ---------------------------------------------------
# A structured output is used. These settings are configured manually ↵
# in LM studio:

schema = {
  "type": "object",
  "properties": {
    "score": {
      "type": "integer",
      "description": "Score assigned to this response"
    },
    "explanation": {
      "type": "string",
      "description": "Explanation for why each of the points were given or were not given."
    }
  },
  "required": [
    "score",
    "explanation"
  ]
}

## SYSTEM PROMPT -------------------------------------------------------
# This is an example system prompt. The ↵
# Autograder._generate_system_prompt() method converts a list of ↵
# tuples provided by the user into the prompt format below:

# Evaluate if the student's response meets each rubric criterion:

# Resample from data (+1 point)
# Resampling with replacement (+1 point)
# Take several sets of resamplings (+1 point)
# Find coefficients for each resampling (+1 point)
# Gather all lines to assess reliability (+1 point)

# Return in JSON:
# {
# 'score': (total points 0-5),
# 'explanation': (brief analysis with key points met/missed)
# }

class Autograder:

    def __init__(self, temperature: float = TEMPERATURE):
        self.rubric_components = []
        self.temperature = temperature
    
    def set_rubric(self, components):
        """Set rubric components for evaluation.
        
        Args:
            compoments (List[Tuples[rubric: str, score: int]]: A list of tuples, each containing the rubric and associated score
        """
        self.rubric_components = components

    def _generate_system_prompt(self):
        """Using the rubric components, generate a system prompt."""
        prompt = "Evaluate if the student's response meets each rubric criterion:\n\n"

        for criterion, score in self.rubric_components:
            prompt += f"{criterion} (+{score} point{'s' if score > 1 else ''}\n\n)"
        
        prompt += """
        Return in JSON:
        {
        'explanation': (brief analysis with key points met/missed)
        'score': (total points 0-5),
        }
        """

        return prompt
    
    def evaluate(self, student_response):
        """Evaluate a student response based on rubric set using set_rubric method.

        Args:
            student_response (str): A string containing the student response

        Returns:
            Dictionary with evaluation results
        """

        if not self.rubric_components:
            return {"error": "Rubric components are not set. Use set_rubric method first to set the rubrics."}
        
        system_prompt = self._generate_system_prompt()

        with lms.Client() as client:

            model = client.llm.model(MODEL)

            prompt = lms.Chat(system_prompt)
            prompt.add_user_message(student_response)

            response = model.respond(prompt, config={
                "temperature": self.temperature,
            })
        
        return response

if __name__ == "__main__":

    autograder = Autograder()

    autograder.set_rubric([
        ("Resample from data", 1),
        ("Resampling done with replacement", 1),
        ("Take several sets of resamplings", 1),
        ("Find coefficients for each resampling", 1),
        ("Gather all lines to assess reliability", 1),
    ])

    student_response = """
    First, the dataset is resampled with replacement multiple times, usually n times where n is the size of the dataset (each dataset is also of size n). The new resampled datasets are then plotted to obtain coefficients such as residuals, gradient of the line of best fit, etc. These coefficients are then plotted together in a histogram and summary statistics are obtained. For example, the range of coefficients can provide insight as to the uncertainty of the coefficients fit by a linear model.
    """

    result = autograder.evaluate(student_response)

    print(result.content)
    print(result.stats)