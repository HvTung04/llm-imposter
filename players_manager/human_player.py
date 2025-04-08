from players_manager.player import Player


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    def answer(self):
        """
        Get the answer from the human player.

        Returns:
            str: The answer provided by the human player.
        """
        return input(f"{self.name}, please enter your answer: ")

    def submit(self):
        """
        Submit the human player's answer to the game.
        """
        pass
