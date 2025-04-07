import time
import uuid
import random
from players_manager.admin import Admin

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

        # Admin
        # self.admin = Admin()

    def add_player(self, player, is_ai=False):
        """
        Add a player to the game.

        Args:
            player (Player): The name of the player.
            is_ai (bool): Whether the player is an AI player or not.

        Returns:
            str: The unique ID of the added player.
        """
        player_id = str(uuid.uuid4())
        self.players[player_id] = {
            "player": player,
            "name": player.name,
            "is_ai": is_ai,
            "eliminated": False
        }
        print(f"Player {player.name} added with ID: {player_id}")
        return player_id
    
    def generate_question(self):
        """
        Generate a question for the current turn.

        Returns:
            str: The generated question.
        """
        # Placeholder for question generation logic
        return f"What is the answer to life, the universe, and everything? (Turn {self.turn})"

    def submit_answer(self, player_id, answer):
        """
        Submit an answer for the current turn.

        Args:
            player_id (str): The ID of the player submitting the answer.
            answer (str): The submitted answer.
        """
        if player_id in self.players and not self.players[player_id]["eliminated"]:
            self.answers[player_id] = answer
            print(f"Player {self.players[player_id]['name']} submitted answer: {answer}")
        else:
            print(f"Player {player_id} is not in the game or has been eliminated.")

    def collect_ai_answers(self, player_id, player_info):
        """
        Collect answers from AI players.
        """
        if player_info["is_ai"] and not player_info["eliminated"]:
            question = self.generate_question()
            answer = player_info["player"].answer(question)  # Placeholder for AI answer generation
            self.submit_answer(player_id, answer)

    def ranking(self):
        """
        Rank the answers provided by players.
        """
        # Placeholder for ranking logic
        ranked_answers = sorted(self.answers.items(), key=lambda x: random.random())
        print("Ranked Answers:")
        for player_id, answer in ranked_answers:
            print(f"Player {self.players[player_id]['name']}: {answer}")
        return ranked_answers
    
    def eliminate_player(self, player_id):
        """
        Eliminate a player from the game.

        Args:
            player_id (str): The ID of the player to eliminate.
        """
        if player_id in self.players:
            self.players[player_id]["eliminated"] = True
            print(f"Player {self.players[player_id]['name']} has been eliminated.")
        else:
            print(f"Player {player_id} not found.")
        
    def get_active_players(self):
        """
        Get a list of active players.

        Returns:
            list: List of active players.
        """
        return [player_id for player_id, info in self.players.items() if not info["eliminated"]]
    
    def game_loop(self):
        # Wait for enough players to join
        while len(self.players) < self.min_players:
            print(f"Waiting for players to join... (Current: {len(self.players)})")
            time.sleep(2)

        self.status = "in_progress"
        print("Game started!")
        while self.status == "in_progress":
            self.turn += 1
            self.current_question = self.generate_question()
            print(f"Turn {self.turn}: {self.current_question}")

            print("Collecting answers...")
            # Collect answers from players
            for player_id, player_info in self.players.items():
                if not player_info["eliminated"]:
                    if player_info["is_ai"]:
                        self.collect_ai_answers(player_id, player_info)
                    else:
                        # Placeholder for human player answer submission
                        answer = input(f"{player_info['name']}, please submit your answer: ")
                        self.submit_answer(player_id, answer)

            # Rank answers and eliminate players if necessary
            ranked_answers = self.ranking()
            # Placeholder for elimination logic
            if len(ranked_answers) > 1:
                eliminated_player_id = ranked_answers[-1][0]
                self.eliminate_player(eliminated_player_id)

            # Check if the game should end
            active_players = self.get_active_players()
            if len(active_players) <= 1:
                print("Game over! Only one player remains.")
                self.status = "finished"
                break