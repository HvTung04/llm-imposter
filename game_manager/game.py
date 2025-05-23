import random
import time
import uuid

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
                    "eliminated": player["eliminated"],
                }
                for player in self.players
            ],
            "current_question": self.current_question,
            "answers": self.answers,
            "remaining_time": self.get_remaining_time(),
        }

    def add_player(self, player, is_ai=False):
        player_id = str(uuid.uuid4())
        player_data = {
            "id": player_id,
            "player": player,
            "name": player.name,
            "is_ai": is_ai,
            "eliminated": False,
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
            self.answers.append({"player_id": player_id, "answer": answer})
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
        players = [
            {
                "id": player["id"],
                "name": player["name"],
                "is_ai": player["is_ai"],
                "eliminated": player["eliminated"],
            }
            for player in self.players
        ]

        player_answered = [item["player_id"] for item in self.answers]
        answer_dict = {}
        for answer in self.answers:
            answer_dict[answer["player_id"]] = answer["answer"]

        for idx, player in enumerate(players):
            if player["eliminated"]:
                continue

            if player["id"] not in player_answered:
                players[idx]["eliminated"] = True
                self.eliminate_player(player["id"])
                continue

            if answer_dict[player["id"]] == "":
                players[idx]["eliminated"] = True
                self.eliminate_player(player["id"])
                continue
            
        all_ids = [answer["player_id"] for answer in self.answers]
        all_answers = [answer["answer"] for answer in self.answers]

        all_ranks = self.admin.rank(self.current_question, all_answers)

        return {
            "scores": [
                {
                    "player_id": all_ids[i],
                    "answer": all_answers[i],
                    "rank": all_ranks[i],
                }
                for i in range(len(all_ids))
            ],
            "players": players,
        }

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
            "names": [p["name"] for p in active_players],
        }

    def start_game(self):
        self.status = "in_progress"

    def play_turn(self):
        if self.status != "in_progress":
            print("Game is not in progress.")
            return

        self.turn += 1
        self.generate_question()
        self.answers = []
        print(f"Question for turn {self.turn}: {self.current_question}")
        self.turn_start_time = time.time()

    def play_turn_ai(self):
        if self.status != "in_progress":
            print("Game is not in progress.")
        for player in self.players:
            if not player["eliminated"] and player["is_ai"]:
                self.collect_ai_answer(player["id"], player)

    def get_remaining_time(self):
        if self.turn_start_time is None:
            return self.answer_timeout
        elapsed = time.time() - self.turn_start_time
        return max(0, int(self.answer_timeout - elapsed))