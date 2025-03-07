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

    def __init__(self):
        self.rubric_components = []
        self.temperature = TEMPERATURE
    
    def set_rubric(self, components):
        """Set rubric components for evaluation.
        
        Args:
            compoments (List[Tuples[rubric: str, score: int]]: A list of tuples, each containing the rubric and associated score
        """
        self.rubric_components = components
    
    def set_temperature(self, temperature: float):
        """Set temperature for autograder.
        
        Args:
            temperature (float): A temperature ranging between 0 and 1, where 0 is the most deterministic, and 1 is the most stochastic
        """
        if temperature < 0 or temperature > 1:
            raise ValueError(f"Temperature should be within 0 to 1. Your temperature was set to: {temperature}")
        else:
            self.temperature = temperature

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

    responses = [
        "Bootstrapping creates a confidence interval of possible lines of best fit. 1) Obtain a sample data set from observation/experiment with replacement. 2) Generate a new randomized data set from the sample data set (step 1) that has the same number of observations. ex: sample has 1000 points, new data set has 1000 based on this. 3) Repeat step 2 multiple times (>10) and determine the line of best fit for each scatter plot. 4) Place these lines on a scatter plot and a range of linear lines should be seen, this will determine if the original line is within the range of a reliable fit (confidence interval of linear model lines)",
        "1. Get a subsample of your data. 2. Get a linear regression model of this data. 3. Repeat the process. 4. Find the average of these lines. 5. Indicate the confidence interval of those lines through the shading […] the regression line.",
        "1. Sample the true data many times (with replacement) to create multiple (n) synthetic data sets. 2. Based on the samples, calculate the linear coefficients for the. 3. Plot and look at thie distribution of these coefficients. This will provide a confidence interval and estimate reliabilty of coefficients.",
        "Bootstrapping involves first random sampling with replacement. It is recommended that that number of samples you take out and replace is equal to the number of data points you have. Next it involves creating a regression line for each of those samples to get an estimate of the line of best fit. Ultimately you would get a confidence interval of the regression line, and where most of the data points lie.",
        "Bootstrapping is the process of taking values that lie within reasonable range of the line of best fit, and calculating a level of variance. This gives insight on how reliable the coefficients of the lines average (y = mx + b). Steps of calculating variance: 1. Set parameters to catch values that fall within a specific range or closeness of the line. 2. Find out how neat or scattered this data is and use this conclusion to inform the rest of analysis.",
        "1. Sample data x number of times, x should be high for confidence. 2. Find regression for each sample best fit line. 3. Combine regressions to get a range of these best fit lines. 4. The narrower the range the more reliable and confident, the wider the range, the less reliable and confident.",
        "1. Obtain a sample of size n. 2. With replacement, pull multiple samples of size n from the sample. 3. Calculate the correlation coefficients of each bootstrapped sample. 4. Calculate the z-score of the correlation coefficients. If the p-value is high (insignificant), we can theorize that a linear model is reliable.",
        "Bootstrapping can estimate how good of a linear fit your model is. 1. Resample your data randomly from original data set. 2. Make a linear fit of resample. 3. Plot fit alongside the original linear fit model (but with some opacity). 4. Repeat steps 1-3 n number of times, In our class, we said n = 1000 to 2000 is generally good.",
        "1. From a set of data, take a sampel of that data with replacement. 2. Repeat step 1 multiple times, still with replacement. 3. Find coefficients for each fo your individual samples. 4. Compare the coefficeitns between each of your samples to judge the reliability of your overall correlation of the entire dataset.",
        "First, the dataset is resampled with replacement multiple times, usually n times where n is the size of the dataset (each dataset is also of size n). The new resampled datasets are then plotted to obtain coefficients such as residuals, gradient of the line of best fit, etc. These coefficients are then plotted together in a histogram and summary statistics are obtained. For example, the range of coefficients can provide insight as to the uncertainty of the coefficients fit by a linear model.",
    ]

    # result = autograder.evaluate(student_response)

    # print(result.content)
    # print(result.stats)

    save_path = "/Users/anjie.wav/summate_data/Expt 2 - Temperature vs Variance - Mar 6/data"

    reps = 90
    temps = [0.2, 0.4, 0.6, 0.8, 1]

    total = reps * len(temps) * len(responses)

    for temp in temps:

        autograder.set_temperature(temp)

        for rep in range(reps):

            for i, response in enumerate(responses):

                print(f"Iteration {rep+11} of grading response {i+11} at temperature = {temp}")
                print(f"{total} evaluations left")

                filename = f"expt_temp_{temp}_resp_{i+11}_run_{rep+11}.txt"
                result = autograder.evaluate(student_response)
                with open(save_path + '/' + filename, 'w') as f:
                    f.write(str(result.content) + '\n')
                    f.write(str(result.stats))

                total -= 1