import random
import sys
from time import sleep

def guessing_game():
    while True:  # Game loop
        # Game setup
        secret_number = random.randint(1, 100)
        attempts = 0
        max_attempts = 10
        guess_history = []
        
        # Clear screen and show welcome
        print("\n" * 50)  # Simple screen clear
        print("🌟 Welcome to the Ultimate Guessing Game! 🌟")
        print(f"I've picked a number between 1 and 100. Can you guess it in {max_attempts} tries?\n")
        
        while attempts < max_attempts:
            attempts += 1
            remaining = max_attempts - attempts
            
            # Get and validate user input
            while True:
                try:
                    prompt = f"Attempt {attempts}/{max_attempts}. Your guess (1-100) or 'hint': "
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
                    
                    if guess < 1 or guess > 100:
                        print("Please enter a number between 1 and 100.")
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
                break
            elif guess < secret_number:
                print(f"Too low! {remaining} attempts remaining.")
            else:
                print(f"Too high! {remaining} attempts remaining.")
        
        # Game over handling
        if guess != secret_number:
            print(f"\nGame over! The number was {secret_number}.")
            print(f"Your guesses: {', '.join(map(str, guess_history))}")
        
        # Play again prompt
        while True:
            try:
                choice = input("\nPlay again? (y/n): ").lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    print("Thanks for playing! Goodbye!")
                    return
                else:
                    print("Please enter 'y' or 'n'.")
            except KeyboardInterrupt:
                print("\nThanks for playing! Goodbye!")
                sys.exit(0)

if __name__ == "__main__":
    try:
        guessing_game()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)