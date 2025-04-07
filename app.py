from game_manager.game import Game
from players_manager.ai_player import AIPlayer
from players_manager.human_player import HumanPlayer

if __name__ == "__main__":
    # Initialize players
    player1 = AIPlayer(name="AI Player 1")
    player2 = HumanPlayer(name="Human Player 1")
    
    # Initialize admin
    
    # Create a game instance
    game = Game()

    game.add_player(player1, is_ai=True)
    game.add_player(player2, is_ai=False)
    
    # Start the game
    game.game_loop()