from flask import Flask, render_template, request, jsonify, session
import random
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

# High scores file path
HIGH_SCORES_FILE = "high_scores.json"

def load_high_scores():
    try:
        with open(HIGH_SCORES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"easy": [], "medium": [], "hard": []}

def save_high_score(difficulty, score, attempts):
    scores = load_high_scores()
    new_score = {
        "score": score,
        "attempts": attempts,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    scores[difficulty].append(new_score)
    scores[difficulty].sort(key=lambda x: x["attempts"])
    scores[difficulty] = scores[difficulty][:5]  # Keep top 5 scores
    
    with open(HIGH_SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html', high_scores=load_high_scores())

@app.route('/start_game', methods=['POST'])
def start_game():
    difficulty = request.json.get('difficulty')
    difficulties = {
        'easy': {"range": (1, 50), "attempts": 15, "name": "easy"},
        'medium': {"range": (1, 100), "attempts": 10, "name": "medium"},
        'hard': {"range": (1, 200), "attempts": 8, "name": "hard"}
    }
    
    diff = difficulties[difficulty]
    secret_number = random.randint(*diff["range"])
    
    session['secret_number'] = secret_number
    session['attempts'] = 0
    session['max_attempts'] = diff["attempts"]
    session['difficulty'] = diff
    session['guess_history'] = []
    
    return jsonify({
        'message': f"I've picked a number between {diff['range'][0]} and {diff['range'][1]}. Can you guess it in {diff['attempts']} tries?",
        'range': diff['range'],
        'max_attempts': diff['attempts']
    })

@app.route('/guess', methods=['POST'])
def guess():
    if 'secret_number' not in session:
        return jsonify({'error': 'Game not started'}), 400
    
    guess = request.json.get('guess')
    try:
        guess = int(guess)
    except ValueError:
        return jsonify({'error': 'Please enter a valid number'}), 400
    
    session['attempts'] += 1
    attempts = session['attempts']
    max_attempts = session['max_attempts']
    secret_number = session['secret_number']
    diff = session['difficulty']
    
    if guess < diff['range'][0] or guess > diff['range'][1]:
        return jsonify({
            'error': f"Please enter a number between {diff['range'][0]} and {diff['range'][1]}"
        }), 400
    
    session['guess_history'].append(guess)
    
    if guess == secret_number:
        score = 100 - (attempts * 10)
        save_high_score(diff['name'], score, attempts)
        return jsonify({
            'success': True,
            'message': f'🎉 Congratulations! You guessed {secret_number} in {attempts} attempts!',
            'attempts': attempts,
            'guess_history': session['guess_history']
        })
    
    remaining = max_attempts - attempts
    if remaining <= 0:
        return jsonify({
            'game_over': True,
            'message': f'Game over! The number was {secret_number}',
            'attempts': attempts,
            'guess_history': session['guess_history']
        })
    
    hint = "⬆️ Too low!" if guess < secret_number else "⬇️ Too high!"
    return jsonify({
        'message': f'{hint} {remaining} attempts remaining.',
        'attempts': attempts,
        'remaining': remaining
    })

@app.route('/hint', methods=['POST'])
def get_hint():
    if 'secret_number' not in session:
        return jsonify({'error': 'Game not started'}), 400
    
    secret_number = session['secret_number']
    hint = "even" if secret_number % 2 == 0 else "odd"
    return jsonify({'hint': f'The number is {hint}'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True) 