# player_actions.py
import sys
import random  # Added for random decision

def player_turn(players, player, deck, player_name, player_order): #function handles each player's turn per round
    if not players[player]['active']:
        return deck
        
    print(f"\nYour card: {players[player]['hand']['rank']} of {players[player]['hand']['suit']}")
    
    # Check if only two players remain (cannot pass)
    active_players = [p for p in players if players[p]['active']]
    if len(active_players) <= 2:
        print("Cannot pass - only two players remain!")
        print("You must keep your card")
        return deck
        
    while True:
        action = input("Would you like to (k)eep or (p)ass your card?: ").lower()
        
        if action == 'end':
            print("Goodbye!")
            sys.exit()
            
        elif action == 'p':
            if len(deck) == 0:
                print("Deck is empty - cannot pass!")
                continue
                
            current_index = player_order.index(player)
            next_index = (current_index + 1) % len(player_order)
            target_player = player_order[next_index]
            
            # Find next active player to the left
            attempts = 0
            while not players[target_player]['active'] and attempts < len(player_order):
                next_index = (next_index + 1) % len(player_order)
                target_player = player_order[next_index]
                attempts += 1
            
            if not players[target_player]['active']:
                print("No active players available to pass to - must keep card")
                break
                
            players[target_player]['hand'], players[player]['hand'] = players[player]['hand'], players[target_player]['hand'] #logic to pass card
            print(f"\nYou passed your card to {target_player}")
            players[player]['hand'] = deck.pop()
            print(f"Your new card: {players[player]['hand']['rank']} of {players[player]['hand']['suit']}")
            break
            
        elif action == 'k':
            print("\nYou kept your card")
            break
            
        else:
            print("Invalid input. Enter 'k', 'p', or 'end'.")
    
    return deck

def computer_decision(player, players, deck, player_name, player_order): #function determines whether the computers keep or pass the card
    if not players[player]['active']:
        return
    
    rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    current_rank = players[player]['hand']['rank']
    
    # Modified decision logic with 75% chance to pass high cards
    if rank_order.index(current_rank) > 8 and random.random() < 0.75:  # 75% chance to pass if card is greater than 8
        current_index = player_order.index(player) #gets the player order to determine player to the left
        next_index = (current_index + 1) % len(player_order)
        target = player_order[next_index]
        
        if players[target]['active']:
            players[target]['hand'], players[player]['hand'] = players[player]['hand'], players[target]['hand']
            print(f"{player} passed their card to {target}")
        else:
            print(f"{player} wanted to pass but {target} is out of the game")
    else:
        print(f"{player} kept their card")