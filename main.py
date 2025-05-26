from poker.blackjack import BlackjackGame

def init_players():
    """Initialize players."""
    players = [
        {"name": "P1", "balance": 1000},
        {"name": "P2", "balance": 1000},
        {"name": "P3", "balance": 1000}
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

        # Create bets dictionary using player IDs
        bets = {}
        for player_id, player in game.active_players.items():
            player.place_bet_by_percent(0.1)
            bets[player_id] = player.bet
        
        # Start the round
        game.init_game()
        
        # Check for dealer blackjack
        state = game.get_game_state(hide_dealer_num=0 if game.dealer.has_blackjack() else 1)
        print(state)

        # Process each player's turn
        for player_id, player in game.active_players.items():
            done = False
            while not done:
                action = input(
                    f"{player.name}, it's your turn. What do you want to do?\n"
                    f"Hand: {player.get_hand_string()}\n"
                    f"Points: {player.get_hand_value()}\n"
                    f"1. Hit\n"
                    f"2. Stand\n"
                )

                if action == "1":
                    card = game.player_hit(id=player_id)
                    print(f"{player.name} drew {card}")

                    # Check if player busted after hitting
                    if player.is_busted():
                        print(f"{player.name} busted with {player.get_hand_value()}!")
                        done = True
                elif action == "2":
                    done = True
            continue
        
        # Dealer's turn would be implemented here
        game.dealer_turn()
        state = game.get_game_state(hide_dealer_num=0)
        print(state)
        # Settle the round
        game.settle_pnl()
        
        # Ask to continue
        play_again = input("Play another round? (y/n): ")
        if play_again.lower() != 'y':
            break
    
    print("\nThanks for playing Blackjack!")

if __name__ == "__main__":
    print("Welcome to Blackjack!")
    main() 