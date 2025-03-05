import requests
import json

# The following is meant to resolve any import issues. It's not ↵
# important for the project:

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import SERVER_URL

## STRUCTURED OUTPUT ---------------------------------------------------
# A structured output is used. These settings are configured manually ↵
# in LM studio:

# {
#   "type": "object",
#   "properties": {
#     "score": {
#       "type": "integer",
#       "description": "Score assigned to this response"
#     },
#     "explanation": {
#       "type": "string",
#       "description": "Breakdown of each rubric component"
#     }
#   },
#   "required": [
#     "score",
#     "explanation"
#   ]
# }

## SYSTEM PROMPT -------------------------------------------------------
# This is an example system prompt:

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

    def __init__(self, server_url = SERVER_URL):
        self.server_url = server_url
        self.rubric_components = []
    
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
        'score': (total points 0-5),
        'explanation': (brief analysis with key points met/missed)
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

        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": student_response}
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            r = requests.post(self.server_url, headers=headers, json=data)
            r.raise_for_status()

            # This is where we should implement debug/error logs in the future.

            response_data = r.json()
            content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                return {
                    "error": "Failed to parse LLM response as JSON",
                    "raw_response": content
                }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"API call failed: {str(e)}",
            }

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

    print(json.dumps(result, indent=2))