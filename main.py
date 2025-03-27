import random
import sys

def guessing_game():
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    guess = None  # Initialize guess variable
    
    print("Welcome to the Guessing Game!")
    print(f"I'm thinking of a number between 1 and 100. You have {max_attempts} attempts to guess it.")
    
    while attempts < max_attempts:
        attempts += 1
        remaining_attempts = max_attempts - attempts + 1
        
        while True:  # Inner loop for input validation
            try:
                user_input = input(f"\nAttempt {attempts}/{max_attempts}. Enter your guess: ")
                
                # Allow user to exit the game early
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"\nGame exited. The secret number was {secret_number}.")
                    return
                
                guess = int(user_input)
                
                # Validate number is within range
                if guess < 1 or guess > 100:
                    print("Please enter a number between 1 and 100.")
                    continue
                    
                break  # Exit input validation loop if input is valid
                
            except ValueError:
                print("Invalid input. Please enter a whole number between 1 and 100.")
                continue
            except KeyboardInterrupt:
                print("\n\nGame interrupted by user. Exiting...")
                sys.exit(0)
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")
                continue
            
        # Game logic after successful input
        if guess < secret_number:
            print(f"Too low! You have {remaining_attempts - 1} attempts remaining.")
        elif guess > secret_number:
            print(f"Too high! You have {remaining_attempts - 1} attempts remaining.")
        else:
            print(f"\nCongratulations! You guessed the number {secret_number} in {attempts} attempts!")
            break
    
    # Final game state check
    if attempts >= max_attempts and guess != secret_number:
        print(f"\nGame over! You've used all {max_attempts} attempts.")
        print(f"The secret number was {secret_number}.")

    # Ask if player wants to play again
    while True:
        try:
            play_again = input("\nWould you like to play again? (yes/no): ").lower()
            if play_again in ['yes', 'y']:
                guessing_game()
                return
            elif play_again in ['no', 'n']:
                print("Thanks for playing! Goodbye.")
                return
            else:
                print("Please enter 'yes' or 'no'.")
        except KeyboardInterrupt:
            print("\n\nGame interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

# Start the game
if __name__ == "__main__":
    try:
        guessing_game()
    except Exception as e:
        print(f"A critical error occurred: {e}")
        sys.exit(1)