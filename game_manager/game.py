import time
import uuid
import random
from players_manager.admin import Admin

class Game:
    def __init__(self, answer_timeout=30, min_players=2):
        self.answer_timeout = answer_timeout
        self.min_players = min_players
        self.turn = 0
        self.status = "waiting"  # waiting, in_progress, finished
        self.players = []  # List of player dicts
        self.current_question = None
        self.answers = []  # List of {player_id, answer}
        self.turn_start_time = None
        self.admin = Admin()

    def get_state(self):
        return {
            "status": self.status,
            "turn": self.turn,
            "players": [
                {
                    "id": player["id"],
                    "name": player["name"],
                    "is_ai": player["is_ai"],
                    "eliminated": player["eliminated"]
                } for player in self.players
            ],
            "current_question": self.current_question,
            "answers": self.answers,
            "remaining_time": self.get_remaining_time()
        }

    def add_player(self, player, is_ai=False):
        player_id = str(uuid.uuid4())
        player_data = {
            "id": player_id,
            "player": player,
            "name": player.name,
            "is_ai": is_ai,
            "eliminated": False
        }
        self.players.append(player_data)
        print(f"Player {player.name} added with ID: {player_id}")
        return player_id

    def find_player(self, player_id):
        for player in self.players:
            if player["id"] == player_id:
                return player
        return None

    def generate_question(self):
        self.current_question = self.admin.ask()
        return self.current_question

    def submit_answer(self, player_id, answer):
        player = self.find_player(player_id)
        if player and not player["eliminated"]:
            self.answers.append({
                "player_id": player_id,
                "answer": answer
            })
            print(f"Player {player['name']} submitted answer: {answer}")
            return True
        else:
            print(f"Player {player_id} is not in the game or has been eliminated.")
            return False

    def collect_ai_answer(self, player_id, player_info):
        if player_info["is_ai"] and not player_info["eliminated"]:
            answer = player_info["player"].answer(self.current_question)
            self.submit_answer(player_id, answer)

    def ranking(self):
        random.shuffle(self.answers)
        print("Ranked Answers:")
        for entry in self.answers:
            player = self.find_player(entry["player_id"])
            if player:
                print(f"Player {player['name']}: {entry['answer']}")
        return self.answers

    def eliminate_player(self, player_id):
        player = self.find_player(player_id)
        if player:
            player["eliminated"] = True
            print(f"Player {player['name']} has been eliminated.")
        else:
            print(f"Player {player_id} not found.")

    def get_active_players(self):
        active_players = [p for p in self.players if not p["eliminated"]]
        return {
            "ids": [p["id"] for p in active_players],
            "names": [p["name"] for p in active_players]
        }

    def start_game(self):
        self.status = "in_progress"

    def play_turn(self):
        if self.status != "in_progress":
            print("Game is not in progress.")
            return

        self.turn += 1
        self.generate_question()
        print(f"Question for turn {self.turn}: {self.current_question}")

        for player in self.players:
            if not player["eliminated"] and player["is_ai"]:
                self.collect_ai_answer(player["id"], player)
        self.turn_start_time = time.time()
    
    def get_remaining_time(self):
        if self.turn_start_time is None:
            return self.answer_timeout
        elapsed = time.time() - self.turn_start_time
        return max(0, int(self.answer_timeout - elapsed))

    def game_loop(self):
        self.start_game()
        print("Game started!")
        while self.status == "in_progress":
            self.turn += 1
            self.generate_question()
            print(f"Turn {self.turn}: {self.current_question}")
            self.answers = []

            print("Collecting answers...")
            for player in self.players:
                if not player["eliminated"]:
                    if player["is_ai"]:
                        self.collect_ai_answer(player["id"], player)
                    else:
                        answer = input(f"{player['name']}, please submit your answer: ")
                        self.submit_answer(player["id"], answer)

            ranked_answers = self.ranking()
            if len(ranked_answers) > 1:
                eliminated_player_id = ranked_answers[-1]["player_id"]
                self.eliminate_player(eliminated_player_id)

            active = self.get_active_players()
            if len(active["ids"]) <= 1:
                print("Game over! Only one player remains.")
                self.status = "finished"
                break
