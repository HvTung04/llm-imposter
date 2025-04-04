import time
import uuid
import random

class Game:
    def __init__(self, answer_timeout=30, min_players=2):
        # Unique game identifier
        self.session_id = str(uuid.uuid4())

        # Game configuration
        self.answer_timeout = answer_timeout  # seconds
        self.min_players = min_players
        self.turn = 0
        self.status = "waiting" # waiting, in_progress, finished
        self.players = {} # Key: Player_ID, Value: Player info
        self.current_question = None
        self.answers = {} # Key: Player_ID, Value: Answer

    def add_player(self, player_name, is_ai=False):
        """
        Add a player to the game.

        Args:
            player_name (str): The name of the player.
            is_ai (bool): Whether the player is an AI player or not.

        Returns:
            str: The unique ID of the added player.
        """
        player_id = str(uuid.uuid4())
        self.players[player_id] = {
            "name": player_name,
            "is_ai": is_ai,
            "eliminated": False
        }
        print(f"Player {player_name} added with ID: {player_id}")
        return player_id
    
    def generate_question(self):
        """
        Generate a question for the current turn.

        Returns:
            str: The generated question.
        """
        # Placeholder for question generation logic
        return f"What is the answer to life, the universe, and everything? (Turn {self.turn})"
