import random
from .card import Card

class Decks:
    """
    Deck class
    
    Attributes:
        num_decks: Number of decks used
        joker: Whether to include joker cards
        cards: All cards in the deck
    """
    
    def __init__(self, num_decks: int = 1, joker: bool = False):
        self.num_decks = num_decks
        self.joker = joker
        self.cards = []
        self._init_cards()
    
    def _init_cards(self):
        """Initialize the deck"""
        self.cards = []
        
        # Add regular cards (52 cards per deck)
        for _ in range(self.num_decks):
            for suit in range(1, 5):  # 1-4: Spades, Hearts, Diamonds, Clubs
                for rank in range(1, 14):  # 1-13: A, 2-10, J, Q, K
                    self.cards.append(Card(suit, rank))
            
            # Add jokers if needed
            if self.joker:
                self.cards.append(Card(0, 0))  # Small joker
                self.cards.append(Card(0, 14))  # Big joker
    
    def reset(self):
        """Reset the deck"""
        self._init_cards()
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        """Deal one card"""
        if not self.cards:
            # If deck is empty, automatically reshuffle
            self.reset()
            self.shuffle()
            
        return self.cards.pop()
    
    def __len__(self):
        """Return number of remaining cards in deck"""
        return len(self.cards)
