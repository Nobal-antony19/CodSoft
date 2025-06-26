import random
import time

def get_user_choice():
    """Prompts the user for their choice."""
    valid_choices = ['rock', 'paper', 'scissors']
    while True:
        user_input = input("Your move! Choose (rock, paper, or scissors): ").lower().strip()
        if user_input in valid_choices:
            return user_input
        else:
            print("Hmm, that's not a valid choice. Please try 'rock', 'paper', or 'scissors'.")

def get_computer_choice():
    """Generates a random choice for the computer."""
    choices = ['rock', 'paper', 'scissors']
    print("Computer is thinking...")
    time.sleep(0.7)
    computer_choice = random.choice(choices)
    return computer_choice

def determine_winner(user_choice, computer_choice):
    """Determines the winner of the round."""
    print(f"\nYou chose: {user_choice.capitalize()}!")
    print(f"The computer chose: {computer_choice.capitalize()}!")

    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        return 'win'
    else:
        return 'lose'

def main_game():
    """Main function to run the Rock-Paper-Scissors game."""
    user_score = 0
    computer_score = 0
    round_count = 0

    print("Welcome to the Ultimate Rock-Paper-Scissors Showdown!")
    print("Let's see if you can outwit the mighty AI!")
    print("--------------------------------------------------")

    while True:
        round_count += 1
        print(f"\n--- Round {round_count} ---")
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()

        outcome = determine_winner(user_choice, computer_choice)

        if outcome == 'win':
            print("You won this round! Excellent move!")
            user_score += 1
        elif outcome == 'lose':
            print("Ouch! The computer got you this time. Better luck next round!")
            computer_score += 1
        else:
            print("It's a tie! Great minds think alike... or just got lucky together!")
        print("-" * 30)

        print(f"Current Score: You {user_score} | Computer {computer_score}")

        play_again = input("Wanna play another round? (yes/no): ").lower().strip()
        if play_again != 'yes':
            break

    print("\n--------------------------------------------------")
    print("Game Over! Here are the final results:")
    print(f"Final Score: You {user_score} | Computer {computer_score}")

    if user_score > computer_score:
        print("CONGRATULATIONS! You are the CHAMPION of this game!")
        print("Your human intuition triumphs over silicon logic!")
    elif computer_score > user_score:
        print("The computer reigns supreme this time. Don't worry, even grandmasters lose sometimes!")
        print("Keep practicing, and you'll get 'em next time!")
    else:
        print("It's a glorious tie! A true battle of wits without a clear victor. Well played!")

    print("Thanks for playing! See you next time!")

# Ensure the game starts when the script is executed directly
if __name__ == "__main__":
    main_game()
