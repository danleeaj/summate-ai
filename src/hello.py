from langchain_core.prompts.prompt import PromptTemplate
from config import PROMPT_TEMPLATE

test_template = "What's the distance between {here} and {there}?"
prompt = PromptTemplate.from_template(test_template)

prompt = prompt.partial(here="Singapore")
prompt = prompt.partial(here="California")

output = prompt.format(there="China")
output = prompt.format(there="Singapore")

print(output)

# prompt.format(rubric_components="==COMPONENT==", student_response="==STUDENT==")
# print(prompt)