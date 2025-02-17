from typing import Dict, Optional
import logging
from openai import OpenAI
from app.utils.helpers import generate_id
from tenacity import retry, stop_after_attempt, wait_exponential

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChatGPTBot:
    def __init__(self, api_key: str, model_name: str):
        """Initialize the ChatGPT bot with API credentials."""
        print(f"Initializing ChatGPTBot with model: {model_name}")
        self.prompts: Dict[str, str] = {}
        try:
            self.client = OpenAI(api_key=api_key)
            print("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {str(e)}")
            raise
        self.model_name = model_name

    def create_prompt(self, prompt: str) -> str:
        """Create and store a new prompt."""
        print(f"Creating new prompt: {prompt[:50]}...")
        prompt_id = generate_id()
        self.prompts[prompt_id] = prompt
        print(f"Prompt created with ID: {prompt_id}")
        return prompt_id

    @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=4, max=10),
            reraise=True
        )
    def get_response_sync(self, prompt_id: str) -> Optional[str]:
        """Get ChatGPT's response for a stored prompt with retry logic."""
        print(f"Getting response for prompt ID: {prompt_id}")
        prompt = self.prompts.get(prompt_id)
        
        if not prompt:
            logger.warning(f"Prompt not found for ID: {prompt_id}")
            return None
            
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
            
        except Exception as e:
            if "insufficient_quota" in str(e):
                logger.error("API quota exceeded. Please check your OpenAI plan.")
                raise Exception("API quota exceeded. Please try again later.")
            raise