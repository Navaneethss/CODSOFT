import random

def computer_pick():
    return random.choice(['rock', 'paper', 'scissors'])

def evaluate_winner(player_choice, comp_choice):
    winning_combinations = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }

    if player_choice == comp_choice:
        return "It's a draw!"
    elif winning_combinations[player_choice] == comp_choice:
        return "Congratulations, you won!"
    else:
        return "Oh no, you lost!"

def start_game():
    player_points = 0
    comp_points = 0

    choice_mapping = {'r': 'rock', 'p': 'paper', 's': 'scissors'}

    while True:
        print("\nPick your move:")
        print("r for Rock")
        print("p for Paper")
        print("s for Scissors")

        player_input = input("Your move: ").lower()

        if player_input not in choice_mapping:
            print("Invalid input! Choose r, p, or s.")
            continue

        player_choice = choice_mapping[player_input]
        comp_choice = computer_pick()

        print(f"Computer chose: {comp_choice}")

        match_result = evaluate_winner(player_choice, comp_choice)
        print(match_result)

        if match_result == "Congratulations, you won!":
            player_points += 1
        elif match_result == "Oh no, you lost!":
            comp_points += 1

        print(f"Current Score - You: {player_points}, Computer: {comp_points}")

        retry = input("Play again? (y/n): ").lower()
        if retry != 'y':
            break

    print("Thanks for playing with us!")

if __name__ == "__main__":
    start_game()