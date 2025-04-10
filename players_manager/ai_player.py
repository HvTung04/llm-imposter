from models.groq_model import GroqModel
from players_manager.player import Player
from prompts.ai_player import system_prompt
from dotenv import load_dotenv
import random
import os

load_dotenv()


class AIPlayer(Player):
    def __init__(
        self, name, model_name=os.getenv("AI_PLAYER_MODEL"), system_prompt=system_prompt
    ):
        super().__init__(name)
        self.style = random.choice([
            "nhàm chán",
            "hài hước",
            "rảnh rỗi",
            "vui vẻ",
            "thích chơi bời",
            "nghiêm túc",
            "chăm học",
            "thích đùa giỡn",
            "thiếu kiên nhẫn",
            "học giỏi",
            "thích khám phá",
            "thích tìm hiểu"
        ])
        self.model = GroqModel(model_name=model_name, system_prompt=system_prompt.format(style=self.style))

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
