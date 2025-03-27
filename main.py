import random

def guessing_game():
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    
    print("Welcome to the Guessing Game!")
    print(f"I'm thinking of a number between 1 and 100. You have {max_attempts} attempts to guess it.")
    
    while attempts < max_attempts:
        attempts += 1
        remaining_attempts = max_attempts - attempts + 1
        
        try:
            guess = int(input(f"\nAttempt {attempts}/{max_attempts}. Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
            
        if guess < secret_number:
            print(f"Too low! You have {remaining_attempts - 1} attempts remaining.")
        elif guess > secret_number:
            print(f"Too high! You have {remaining_attempts - 1} attempts remaining.")
        else:
            print(f"\nCongratulations! You guessed the number {secret_number} in {attempts} attempts!")
            break
    # Exeption with simple if statements
    if attempts >= max_attempts and guess != secret_number:
        print(f"\nGame over! You've used all {max_attempts} attempts.")
        print(f"The secret number was {secret_number}.")

# Start the game
guessing_game()
