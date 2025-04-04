from models.groq_model import GroqModel
from dotenv import load_dotenv
import os

load_dotenv()

class AIPlayer:
    def __init__(self, model_name=os.getenv("AI_PLAYER_MODEL"), system_prompt=None):
        self.model = GroqModel(
            model_name=model_name,
            system_prompt=system_prompt
            )

    def answer(self, question):
        """
        Generate a response to the given question using the AI model.

        Args:
            question (str): The question to ask the AI model.

        Returns:
            str: The generated response from the AI model.
        """
        response = self.model.generate_plain_text(question)
        return response
    
    def submit(self):
        """
        Submit the AI player's answer to the game.
        """
        pass