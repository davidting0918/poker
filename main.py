
from poker.blackjack import Player, BlackjackGame

def init_players():
    """Initialize players."""
    players = [
        Player("P1", 1000),
        Player("P2", 1000),
        Player("P3", 1000)
    ]
    return players

def main():
    """Play a game of Blackjack."""
    # Game setup
    players = init_players()
    
    game: BlackjackGame = BlackjackGame(players, decks_num=2)
    
    # Main game loop
    while True:
        if not game.active_players:
            print("All players are bankrupt! Game over.")
            break
        
        # Betting phase
        print("\n=== Betting Phase ===")

        for player in game.active_players:
            player.place_bet_by_percent(0.1)
        
        # Start the round
        game.init_game()
        
        # Check for dealer blackjack
        state = game.get_game_state(hide_dealer_num=0 if game.dealer.has_blackjack() else 1)
        print(state)

        for player in game.active_players:
            while True:
                action = input(
                    f"{player.name}, it's your turn. What do you want to do?\n"
                    f"1. Hit\n"
                    f"2. Stand\n"
                )

                if action == "1":
                    pass
                elif action == "2":
                    break
                
        
        continue
    
    print("\nThanks for playing Blackjack!")

if __name__ == "__main__":
    print("Welcome to Blackjack!")
    main() 