# Screw-Your-Neighbor

A Python-based implementation of the classic card game Screw Your Neighbor. This program supports 1 human player and 2-5 computer opponents each starting with 3 lives. Be the last one standing by avoiding holding the highest card at the end of each round through passing/holding onto your card.

Setup:
1. Ensure main_game.py and player_actions.py are in the same directory.
2. Open a terminal/command prompt.
3. Execute the following command to start: python main_game.py

How to Use:
1. Start by entering name and selecting computer opponents (2-5) to set up the player dictionary and shuffle the 52 card deck.
2. Observe the randomly selected first player and review your dealt card’s rank and suit displayed in the terminal. The highest card is Ace and the lowest card is 2.
3. Decide either to keep (k) card or pass (p) card to the neighbor on the left. The pass option is automatically disabled if only 2 players remain.
4. View the final hands of all players at the end of the round. The system will automatically detect the highest card and deduct 1 life from the holder.

Exit the program anytime by typing **end**.
