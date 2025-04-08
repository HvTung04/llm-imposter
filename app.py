from game_manager.game import Game
from players_manager.ai_player import AIPlayer
from players_manager.human_player import HumanPlayer
from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO
import qrcode
import base64

app = Flask(__name__)
CORS(app)

# Store all active game sessions (in-memory; TODO: consider a persistent store)
games = {}

@app.route('/create_game', methods=['POST'])
def create_game():
    """
    Create a new game session.
    """
    data = request.get_json() or {}

    min_players = data.get('min_players', 2)
    answer_timeout = data.get('answer_timeout', 60)

    game = Game(min_players=min_players, answer_timeout=answer_timeout)
    games[game.session_id] = game

    return jsonify({
        "session_id": game.session_id,
        "min_players": min_players,
        "answer_timeout": answer_timeout,
        "message": "Game session created successfully."
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
        "active_count": len(active_ids)
    })

@app.route('/join_game', methods=['POST'])
def join_game():
    data = request.get_json()
    session_id = data.get('session_id')
    player_name = data.get('player_name')
    is_ai = data.get('is_ai', False)

    if session_id not in games:
        return jsonify({"error": "Game session not found."}), 404
    
    player = AIPlayer(player_name) if is_ai else HumanPlayer(player_name)
    
    game = games[session_id]
    player_id = game.add_player(player, is_ai)

    return jsonify({
        "message": f"{player_name} joined the game.",
        "session_id": session_id,
        "player_id": player_id
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    session_id = data.get('session_id')
    player_id = data.get('player_id')
    answer = data.get('answer')

    if session_id not in games:
        return jsonify({"error": "Game session not found."}), 404
    
    game = games[session_id]
    if game.submit_answer(player_id, answer):
        return jsonify({"message": "Answer submitted successfully."})
    else:
        return jsonify({"error": "Failed to submit answer."}), 400
    
@app.route('/game_state/<session_id>', methods=['GET'])
def game_state(session_id):
    """
    Get the current state of a game session.
    """
    if session_id not in games:
        return jsonify({"error": "Game session not found."}), 404
    
    game = games[session_id]
    state = game.get_state()
    return jsonify(state)

@app.route('/game_qr/<session_id>', methods=['GET'])
def game_qr(session_id):
    if session_id not in games:
        return jsonify({"error": "Game session not found."}), 404
    game = games[session_id]
    
    join_url = f"http://localhost:5000/join_game?session_id={session_id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(join_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    qr_data_uri = f"data:image/png;base64,{img_base64}"
    return jsonify({
        "session_id": session_id,
        "qr_code": qr_data_uri,
        "join_url": join_url
    })

if __name__ == "__main__":
    app.run(debug=True)