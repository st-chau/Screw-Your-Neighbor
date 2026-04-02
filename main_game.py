# main_game.py
import random #random import to randomize cards 
import sys #import allows for sys.exit to quickly quit out of the program
from player_actions import player_turn  # gets user defined function from another file

def start_game(player_name, num_players, first_player): #function initializes the game
    players = {
        player_name: {'lives': 3, 'hand': None, 'active': True}
    }
    for i in range(1, num_players): #add other players based on user input
        players[f'Computer {i}'] = {'lives': 3, 'hand': None, 'active': True}
    deck = create_deck()
    
    # Create player order with specified first player
    player_order = []
    if (first_player == player_name):
        player_order = [player_name] + [f'Computer {i}' for i in range(1, num_players)]
    else:
        comp_num = int(first_player.split()[-1])
        player_order = [f'Computer {i}' for i in range(1, num_players)]
        player_order.insert(comp_num-1, player_name)
    
    return players, deck, player_order

def get_name(): #function gets player name 
    while True:
        name = input("Enter your name (or 'end' to quit): ").strip()
        if name.lower() == 'end':
            print("Goodbye!")
            sys.exit() #exits program if user inputs 'end'
        if name:
            return name
        print("Please enter a valid name.")

def get_players(): #function gets number of players (2-5 other players = 3-6 total)
    while True:
        try:
            num = input("Enter number of other players (2-5) or 'end' to quit: ").strip()
            if num.lower() == 'end':
                print("Goodbye!")
                sys.exit()
            num = int(num)
            if 2 <= num <= 5:
                return num + 1  #gets the total number of players (including you)
            print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Please enter a valid number.")

def create_deck(): #function creates a deck of standard cards and shuffles deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal_cards(players, deck): #function deals one card from the deck to each player
    for player in players:
        if players[player]['active']:
            if len(deck) > 0:
                players[player]['hand'] = deck.pop()
            else:
                print("Deck is empty! Reshuffling...")
                deck = create_deck()
                players[player]['hand'] = deck.pop()
    return deck

def evaluate_round(players): #function determines which player has the highest card in the round
    rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    highest_rank = None
    losers = []
    
    for player, data in players.items():
        if not data['active']:
            continue
        current_rank = data['hand']['rank']
        if highest_rank is None or rank_order.index(current_rank) > rank_order.index(highest_rank):
            highest_rank = current_rank
            losers = [player]
        elif rank_order.index(current_rank) == rank_order.index(highest_rank):
            losers.append(player)
    
    return losers

def computer_decision(player, players, deck, player_name, player_order): #function determines whether the computers keep or pass the card
    if not players[player]['active']:
        return
    
    # Check if only two players remain (cannot pass)
    active_players = [p for p in players if players[p]['active']]
    if len(active_players) <= 2:
        print(f"{player} cannot pass (only two players remain)")
        return
    
    rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    current_rank = players[player]['hand']['rank']
    
    if rank_order.index(current_rank) > 8 and random.random() < 0.75:  # 75% chance to pass if card is greater than 8
        current_index = player_order.index(player)
        next_index = (current_index + 1) % len(player_order)
        target = player_order[next_index]
        
        # Find next active player to the left
        attempts = 0
        while not players[target]['active'] and attempts < len(player_order):
            next_index = (next_index + 1) % len(player_order)
            target = player_order[next_index]
            attempts += 1
        
        if players[target]['active']:
            players[target]['hand'], players[player]['hand'] = players[player]['hand'], players[target]['hand']
            print(f"{player} passed their card to {target}")
        else:
            print(f"{player} wanted to pass but no active players available")
    else:
        print(f"{player} kept their card")

def show_hands(players, player_name): #function shows all players cards at the end of the round
    print("\nFinal cards this round:")
    for player in players:
        if players[player]['active']:
            if player == player_name:
                print(f"You: {players[player]['hand']['rank']} of {players[player]['hand']['suit']}")
            else:
                print(f"{player}: {players[player]['hand']['rank']} of {players[player]['hand']['suit']}")
        else:
            print(f"{player} is out of the game")

def show_lives(players, player_name): #function shows remaining lives after each round
    print("\nRemaining lives:")
    for player in players:
        if player == player_name:
            print(f"You: {players[player]['lives']} lives")
        else:
            print(f"{player}: {players[player]['lives']} lives")

def active_status(players): #function updates player status and eliminates them if they reach <= 0 lives
    for player in players:
        if players[player]['lives'] <= 0:
            players[player]['active'] = False

def main():
    while True:  # Added game loop
        print("\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ sᴄʀᴇᴡ ʏᴏᴜʀ ɴᴇɪɢʜʙᴏʀ!")

        player_name = get_name()
        num_players = get_players()

        print(f"\nHello, {player_name}! Each player starts with 3 lives. Try not to get the highest card each round!")
        print("(2 is lowest and A is highest)")
        print(f"You can only pass your card to the player to your left.\n")
        
        # Randomly select first player
        first_player = random.choice([player_name] + [f'Computer {i}' for i in range(1, num_players)])
        print(f"{first_player} will go first this game!")
        
        players, deck, player_order = start_game(player_name, num_players, first_player)
        round_num = 1
        
        while sum(1 for p in players if players[p]['active']) > 1:
            print(f"\n--- Round {round_num} ---")
            
            deck = deal_cards(players, deck)
            
            for player in player_order: #gets player order and turns to next player
                if not players[player]['active']:
                    continue
                    
                if player == player_name:
                    deck = player_turn(players, player, deck, player_name, player_order)
                else:
                    computer_decision(player, players, deck, player_name, player_order)
            
            show_hands(players, player_name) #at the end of the round show hands
            
            losers = evaluate_round(players) #evaluate the round to determine loser(s)
            
            if len(losers) > 0:
                for loser in losers:
                    players[loser]['lives'] -= 1
                    print(f"\n{loser} lost a life!")
            
            show_lives(players, player_name)
            active_status(players)
            
            active_players = [p for p in players if players[p]['active']]
            if len(active_players) == 1:
                winner = active_players[0]
                if winner == player_name:
                    print(f"\nCongratulations, {player_name}! You won the game!")
                else:
                    print(f"\n{winner} wins the game!")
                break
            
            round_num += 1
        
        print("\nGame over! Final scores:")
        for player in players:
            if player == player_name:
                print(f"You: {players[player]['lives']} lives remaining")
            else:
                print(f"{player}: {players[player]['lives']} lives remaining")
        
        # Play again prompt
        while True:
            play_again = input("\nWould you like to play again? (y/n): ").lower()
            if play_again == 'n':
                print("Thanks for playing! Goodbye!")
                sys.exit()
            elif play_again == 'y':
                break
            else:
                print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()