class HumanPlayer:
    def __init__(self, name: str):
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