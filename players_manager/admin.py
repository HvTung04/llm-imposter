from models.groq_model import GroqModel
from dotenv import load_dotenv
import os

load_dotenv()

class Admin:
    def __init__(self, model_name=os.getenv("ADMIN_MODEL"), system_prompt=None):
        self.model = GroqModel(
            model_name=model_name,
            system_prompt=system_prompt
            )

    def ask(self):
        """
        Create a question for the current turn

        Returns:
            str: The generated question.
        """
        question = "What is life?"
        return question
    
    def rank(self, answers):
        """
        Rank the answers provided by players.

        Args:
            answers (list): List of answers provided by players.

        Returns:
            list: Ranked list of answers.
        """
        pass

    def eliminate(self, player_id):
        """
        Eliminate a player from the game.

        Args:
            player_id (str): The ID of the player to eliminate.
        """
        pass