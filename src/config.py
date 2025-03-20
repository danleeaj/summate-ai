## MODEL ==========================================================================================
# This is the model LM Studio will use to perform inference.
# Ensure that this model is downloaded in Ollama first before
# using it.

MODEL = "llama3.1:8b"

## MODEL PARAMETERS ===============================================================================
# These are the default model parameters. When initializing an
# autograder class, the parameters that are not specified
# will default to these values.

TEMPERATURE = 0.8

## PROMPT TEMPLATES ===============================================================================
# These are the templates used for generating the prompt.

# PROMPT_TEMPLATE = """
# Evaluate if the student's response meets each rubric criterion.
# ## RUBRIC COMPONENTS
# {rubric_components}
# ## STUDENT RESPONSE
# {student_response}
# Return in JSON:
# {{
#     \"explanation\": (brief analysis with key points met/missed),
#     \"score\": (total points 0-5)
# }}
# Response:
# {{
#     \"explanation\": \"
# """

PROMPT_TEMPLATE = """
### Instruction:
Evaluate if the student's response meets each rubric criterion.

## RUBRIC COMPONENTS
{rubric_components}
## STUDENT RESPONSE
{student_response}

For each rubric component:

CRITERION: [Name of criterion]
EXPLANATION: [Detailed evaluation of how the response meets or fails to meet this criterion]
SCORE: [Points earned]/[Points possible]

====================

TOTAL_SCORE: [Sum of points earned]/[Sum of points possible]

### Response:
"""

# An example of what this would return would be the following:

# Evaluate if the student's response meets each rubric criterion.
# ## QUESTION
# What does a p-value of 0.03 indicate in a hypothesis test?
# ## RUBRIC COMPONENTS
# States that p-value is less than 0.05 (+1 point)
# States that the null hypothesis is rejected (+1 point)
# ## STUDENT RESPONSE
# A p-value of 0.03 means that the alternative hypothesis is rejected, and the null is accepted.
# Return in JSON:
# {
#     'score': (total points 0-5),
#     'explanation': (brief analysis with key points met/missed)
# }
# Response:
# {
#     "explanation": "
# }

## STRUCTURED OUTPUT ==============================================================================
# JSON schema for a structured output. This has not been implemented yet.

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