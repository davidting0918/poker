from .deck import Decks
from .card import Card
import uuid
class Player:

    def __init__(self, name: str, balance: int = 1000):
        self.id = str(uuid.uuid4())
        self.name = name
        self.balance = balance
        self.hand: list[Card] = []
        self.bet = 0

    
    def place_bet(self, amount: int) -> bool:
        """Place a bet if player has enough balance."""
        if amount <= 0 or amount > self.balance:
            return False
        
        self.bet = amount
        self.balance -= amount
        return True

    def place_bet_by_percent(self, percent: float) -> bool:
        """Place a bet by percentage of the balance."""
        if percent <= 0 or percent > 1:
            return False
        
        self.bet = int(self.balance * percent)
        self.balance -= self.bet
        return True
    
    def add_cards(self, cards: list[Card]) -> None:
        """Add a card to player's hand."""
        self.hand.extend(cards)
    
    def get_hand_value(self) -> int:
        """Calculate the value of the hand in Blackjack."""
        value = 0
        aces = 0
        
        for card in self.hand:
            if card.rank == 1:  # Ace
                aces += 1
                value += 11
            elif card.rank >= 11:  # Face cards
                value += 10
            else:
                value += card.rank
        
        # Adjust for aces if needed
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
            
        return value
    
    def is_busted(self) -> bool:
        """Check if player's hand is busted."""
        return self.get_hand_value() > 21
    
    def clear_hand(self) -> None:
        """Clear player's hand for a new round."""
        self.hand = []
        self.bet = 0
    
    def has_blackjack(self) -> bool:
        """Check if player has blackjack (an ace and a 10-value card)."""
        if len(self.hand) != 2:
            return False
        
        return self.get_hand_value() == 21

    def get_hand_string(self, hide_num: int = 0) -> str:
        """Get player's hand as a string."""
        hand_str = ""
        for i, card in enumerate(self.hand):
            if i < hide_num:
                hand_str += "🂠 "  # Back of card
            else:
                hand_str += f"{card} "
        
        return hand_str


class BlackjackGame:
    """
    This is the main engine for the Blackjack game.
    Whole game will have 4 states:
    1. betting:
        - Let each player place their bet

    2. player_turn:
        - Each player have 3 options:
            - Hit: Draw a card
            - Stand: End the turn
            - Double: Double the bet and draw one card
    3. dealer_turn:
        - Dealer will draw card if the value of the hand is less than 17
    4. settling:
        - Compare each player's hand with the dealer's hand
    """

    card_dealt_log = {"dealer": [], "players": {}}

    def __init__(self, players: list[dict], decks_num: int = 1, min_bet: int = 100, max_bet: int = 1000, reset_threshold: float = 0.2):
        # Convert players list to dictionary with player.id as key
        self.players = self._init_players(players)
        self.dealer = Player("Dealer", 0)
        self.deck = Decks(decks_num, joker=False)
        self.game_state = "betting" # betting, player_turn, dealer_turn, settling
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.reset_threshold = reset_threshold
        self.active_players = self.get_active_players()
        self.round = 0

    def _init_players(self, players: list[dict]) -> dict[str, Player]:
        info = {}
        for player in players:
            player = Player(player["name"], player["balance"])
            info[player.id] = player
            self.card_dealt_log["players"][player.id] = []
        return info

    def get_active_players(self) -> dict[str, Player]:
        """Get dictionary of players that have enough balance to play."""
        return {player_id: player for player_id, player in self.players.items() 
                if player.balance >= self.min_bet}

    def init_round(self):
        """
        1. Give each player 2 cards
        2. Give dealer 2 cards
        """
        self.round += 1
        
        if self.deck.get_left_ratio() < self.reset_threshold:
            self.deck.reset()

        for player in self.active_players.values():
            cards = self.deck.deal(2)
            player.add_cards(cards)
            self.card_dealt_log["players"][player.id] = cards

        cards = self.deck.deal(2)
        self.dealer.add_cards(cards)
        self.card_dealt_log["dealer"] = cards
        return

    def set_bets(self, bets: dict):
        for player in self.active_players:
            player.bet = bets[player.name]
            player.balance -= player.bet
        return
    
    def get_game_state(self, hide_dealer_num: int = 1) -> str:
        state = f"Current game state: {self.game_state}\n\n"
        
        # Show dealer's info
        state += f"Dealer's cards: {self.dealer.get_hand_string(hide_dealer_num)}\n"
        if hide_dealer_num == 0:
            state += f"Dealer's points: {self.dealer.get_hand_value()}\n"
        state += "\n"
        
        # Show each player's info
        for player in self.active_players.values():
            state += f"{player.name}'s cards: {player.get_hand_string()}\n"
            state += f"Points: {player.get_hand_value()}\n"
            state += f"Balance: ${player.balance}\n"
            state += f"Current bet: ${player.bet}\n"
            state += "\n"

        return state
    

    def settle_pnl(self):
        """
        Based on the hand of each player to settle their pnl.
        """

        for player in self.active_players.values():
            if player.is_busted():
                player.balance -= player.bet
            elif self.dealer.is_busted():
                player.balance += 2 * player.bet
            elif player.get_hand_value() > self.dealer.get_hand_value():
                player.balance += 2 * player.bet
            elif player.get_hand_value() == self.dealer.get_hand_value():
                player.balance += player.bet
        
            player.clear_hand()
        self.dealer.clear_hand()
        self.active_players = self.get_active_players()
        return True
    
    def player_hit(self, id: str) -> Card:
        """Give a card to the player with the given id."""
        if id in self.active_players:
            player = self.active_players[id]
            card = self.deck.deal()
            player.add_cards(card)
            self.card_dealt_log["players"][id].extend(card)
            return card
        
    def dealer_turn(self):
        """Dealer will draw card if the value of the hand is less than 17"""
        while self.dealer.get_hand_value() < 17:
            card = self.deck.deal()
            self.dealer.add_cards(card)
            self.card_dealt_log["dealer"].extend(card)
        return
