class Card:
    """
    This is the class for a single card.
    """
    SUITS = {1: "♠", 2: "♥", 3: "♦", 4: "♣", 0: "🤡"}
    RANKS = {1: "A", 11: "J", 12: "Q", 13: "K"}
    
    def __init__(self, suit: int, rank: int):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        
        rank_str = self.RANKS.get(self.rank, str(self.rank))
        suit_str = self.SUITS.get(self.suit, "?")
        
        return f"{rank_str}{suit_str}"
    
    def __repr__(self):
        return self.__str__()
    
    
