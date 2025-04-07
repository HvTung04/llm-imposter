from game_manager.game import Game
from players_manager.ai_player import AIPlayer
from players_manager.human_player import HumanPlayer
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store all active game sessions (in-memory; TODO: consider a persistent store)
games = {}

@app.route('/create_game', methods=['POST'])
def create_game():
    """
    Create a new game session.
    """
    game = Game(answer_timeout=30, min_players=2)
    games[game.session_id] = game
    return jsonify({
        "session_id": game.session_id,
        "message": "Game created successfully."
    })

@app.route('/active_players/<session_id>', methods=['GET'])
def active_players(session_id):
    """
    Get the list of active players in a game session.
    """
    game = games.get(session_id)
    if not game:
        return jsonify({"error": "Game session not found."}), 404
    
    active_ids = game.get_active_players()
    return jsonify({
        "active_player_ids": active_ids,
        "active_count": len(active_players)
    })

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