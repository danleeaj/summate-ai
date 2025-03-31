from langchain_ollama import OllamaLLM
from langchain_core.prompts.prompt import PromptTemplate
from typing import Optional
import logging

from src.config import MODEL, TEMPERATURE, PROMPT_TEMPLATE

logger = logging.getLogger(__name__)
langchain_logger = logging.getLogger("langchain")

# List of supported hosts
SUPPORTED_LLM_HOSTS = ['ollama']

def configure_logging(enable_logging = True, log_level = logging.INFO):
    """Configure logging status. Defaults to True, and logging.INFO."""
    if enable_logging:
        # These are the configuration settings for the logger
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("autograder.log"),
                logging.StreamHandler()
            ],
            force=True
        )

        # Set specific level for langchain logger
        langchain_logger.setLevel(log_level)

        logger.info("Logging enabled")
    else:

        logging.basicConfig(level=logging.CRITICAL + 1, force=True)
        langchain_logger.setLevel(logging.CRITICAL + 1)

class Autograder:

    def __init__(self, llm_host: str = "ollama", llm_model: Optional[str] = None, enable_logging: bool = True):

        configure_logging(enable_logging)

        logger.info("Initializing autograder...")

        self.rubric_components = []
        self.temperature = TEMPERATURE
        self.llm_host = str(llm_host)
        self.llm_model = llm_model
        self.prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

        if self.llm_host not in SUPPORTED_LLM_HOSTS:
            logger.error(f"{self.llm_host} not supported.")
            raise ValueError(f"{self.llm_host} not supported. Current supported hosts include: {SUPPORTED_LLM_HOSTS}.")
        else:
            if self.llm_host.lower() == 'ollama' and self.llm_model:
                self.model = OllamaLLM(model=self.llm_model)

            elif self.llm_host.lower() == 'ollama':
                logger.error("No LLM model provided.")
                raise ValueError("No LLM model provided. Please provide an LLM model when initializing Autograder.")

    def set_rubric(self, components):
        """Set rubric components for evaluation.
        
        Args:
            components (List[Tuples[rubric: str, score: int]]: A list of tuples, each containing the rubric and associated score
        """

        self.rubric_components = components

        logger.info("Parsing rubric components...")

        parsed_components = ""
        for criterion, score in self.rubric_components:
            parsed_components += f"{criterion} (+{score} point{'s' if score > 1 else ''})\n"

        logger.info(f"{len(self.rubric_components)} rubric component(s) set.")

        self.prompt = self.prompt.partial(rubric_components=parsed_components)
    
    def set_temperature(self, temperature: float):
        """Set temperature for autograder.
        
        Args:
            temperature (float): A temperature ranging between 0 and 1, where 0 is the most deterministic, and 1 is the most stochastic
        """
        if temperature < 0 or temperature > 1:
            logger.error(f"Temperature should be within 0 to 1. Your temperature was set to: {temperature}")
            raise ValueError(f"Temperature should be within 0 to 1. Your temperature was set to: {temperature}")
        else:
            self.temperature = temperature
            logger.info(f"Temperature set at {self.temperature}")
    2
    def evaluate(self, response):
        """Evaluate a student response based on rubric set using set_rubric method.

        Args:
            response (str): A string containing the student response

        Returns:
            Dictionary with evaluation results
        """

        if not self.rubric_components:
            logger.error("No rubric components found.")
            return {"error": "Rubric components are not set. Use set_rubric method first to set the rubrics."}

        # Here we use prompt instead of self.prompt because we don't
        # want our formatted prompt (prompt with rubrics and question,
        # but without student response) to be overwritten...

        # I think there is a better way to implement this but,
        # I can't think of one yet.

        logger.info("Initiating request to Ollama.")

        prompt = self.prompt.format_prompt(student_response=response)

        output = self.model.invoke(prompt)
        
        return output