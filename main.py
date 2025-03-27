import random
import sys
from time import sleep
import os
import winsound  # For Windows sound effects
import json
from datetime import datetime

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

def play_sound(success=True):
    if success:
        winsound.Beep(1000, 500)  # Higher pitch for success
    else:
        winsound.Beep(500, 300)   # Lower pitch for failure

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("\n" * 2)
    print("=" * 50)
    print("🌟 Welcome to the Ultimate Guessing Game! 🌟")
    print("=" * 50)
    print("\n")

def show_high_scores():
    scores = load_high_scores()
    print("\n🏆 High Scores:")
    for difficulty in ["easy", "medium", "hard"]:
        print(f"\n{difficulty.title()} Mode:")
        if scores[difficulty]:
            for i, score in enumerate(scores[difficulty], 1):
                print(f"{i}. {score['attempts']} attempts - {score['date']}")
        else:
            print("No scores yet!")

def get_difficulty():
    while True:
        print("\nSelect difficulty:")
        print("1. Easy (1-50, 15 attempts)")
        print("2. Medium (1-100, 10 attempts)")
        print("3. Hard (1-200, 8 attempts)")
        try:
            choice = int(input("\nEnter difficulty (1-3): "))
            if 1 <= choice <= 3:
                return {
                    1: {"range": (1, 50), "attempts": 15, "name": "easy"},
                    2: {"range": (1, 100), "attempts": 10, "name": "medium"},
                    3: {"range": (1, 200), "attempts": 8, "name": "hard"}
                }[choice]
            print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")

def guessing_game():
    while True:  # Game loop
        clear_screen()
        print_header()
        
        # Show high scores
        show_high_scores()
        
        # Get difficulty level
        difficulty = get_difficulty()
        secret_number = random.randint(*difficulty["range"])
        attempts = 0
        max_attempts = difficulty["attempts"]
        guess_history = []
        
        print(f"\nI've picked a number between {difficulty['range'][0]} and {difficulty['range'][1]}.")
        print(f"Can you guess it in {max_attempts} tries?\n")
        
        while attempts < max_attempts:
            attempts += 1
            remaining = max_attempts - attempts
            
            # Get and validate user input
            while True:
                try:
                    prompt = f"Attempt {attempts}/{max_attempts}. Your guess ({difficulty['range'][0]}-{difficulty['range'][1]}) or 'hint': "
                    user_input = input(prompt).strip().lower()
                    
                    # Special commands
                    if user_input in ['quit', 'exit', 'q']:
                        print(f"\nGame exited. The number was {secret_number}.")
                        return
                    elif user_input == 'hint':
                        hint = "even" if secret_number % 2 == 0 else "odd"
                        print(f"Hint: The number is {hint}")
                        continue
                    elif user_input == 'history':
                        print("Your guesses:", ", ".join(map(str, guess_history)))
                        continue
                    
                    guess = int(user_input)
                    
                    if guess < difficulty["range"][0] or guess > difficulty["range"][1]:
                        print(f"Please enter a number between {difficulty['range'][0]} and {difficulty['range'][1]}.")
                        continue
                        
                    guess_history.append(guess)
                    break
                    
                except ValueError:
                    print("Invalid input. Please enter a number or command (hint/history/quit).")
                except KeyboardInterrupt:
                    print("\n\nGame interrupted. The number was", secret_number)
                    sys.exit(0)
            
            # Check guess
            if guess == secret_number:
                print(f"\n🎉 Congratulations! You guessed {secret_number} in {attempts} attempts!")
                print(f"Your guesses: {', '.join(map(str, guess_history))}")
                play_sound(True)
                save_high_score(difficulty["name"], 100 - (attempts * 10), attempts)
                break
            elif guess < secret_number:
                print(f"⬆️ Too low! {remaining} attempts remaining.")
                play_sound(False)
            else:
                print(f"⬇️ Too high! {remaining} attempts remaining.")
                play_sound(False)
        
        # Game over handling
        if guess != secret_number:
            print(f"\nGame over! The number was {secret_number}.")
            print(f"Your guesses: {', '.join(map(str, guess_history))}")
            play_sound(False)
        
        # Play again prompt
        while True:
            try:
                choice = input("\nPlay again? (y/n): ").lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    print("\nThanks for playing! Goodbye!")
                    return
                else:
                    print("Please enter 'y' or 'n'.")
            except KeyboardInterrupt:
                print("\nThanks for playing! Goodbye!")
                sys.exit(0)

# Start the game when the script is run
if __name__ == "__main__":
    try:
        guessing_game()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)