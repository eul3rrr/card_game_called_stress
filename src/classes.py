class Card:
    def __init__(self, face_value, suit):
        """
        Initialize a card with a face value and a suit.

        Args:
            face_value (int): An integer representing the face value (1 to 13).
            suit (int): An integer representing the suit (1 to 4).
        """
        if not (1 <= face_value <= 13):
            raise ValueError("face_value must be between 1 and 13")
        if not (1 <= suit <= 4):
            raise ValueError("suit must be between 1 and 4")

        self.face_value = face_value
        self.suit = suit

    def __repr__(self):
        """Return a string representation of the card."""
        suit_names = {1: "Hearts", 2: "Diamonds", 3: "Clubs", 4: "Spades"}
        face_names = {
            1: "Ace", 11: "Jack", 12: "Queen", 13: "King"
        }
        face = face_names.get(self.face_value, str(self.face_value))
        suit = suit_names[self.suit]
        return f"{face} of {suit}"

class Deck:
    def __init__(self):
        """
        Initialize a deck of 52 cards, one for each (face_value, suit) pair.
        """
        self.cards = [Card(face_value, suit) for suit in range(1, 5) for face_value in range(1, 13 + 1)]

    def shuffle(self):
        """
        Shuffle the cards in the deck randomly.
        """
        import random
        random.shuffle(self.cards)

    def reset(self):
        """
        Reset the deck to the full 52 cards in order.
        """
        self.cards = [Card(face_value, suit) for suit in range(1, 5) for face_value in range(1, 13 + 1)]

class Player:
    def __init__(self, name):
        """
        Initialize a player with a name and an empty hand.

        Args:
            name (str): The name of the player.
        """
        self.name = name
        self.hand = []

    def receive_cards(self, cards):
        """
        Add a list of cards to the player's hand.

        Args:
            cards (list of Card): The cards to add to the player's hand.
        """
        self.hand.extend(cards)

    def show_hand(self):
        """
        Display the player's current hand.
        """
        return f"{self.name}'s hand: {', '.join(map(str, self.hand))}"

class Table:
    def __init__(self, num_players=2, stacks_per_player=5):
        """
        Initialize a table with slots for card stacks.

        Args:
            num_players (int): Number of players at the table.
            stacks_per_player (int): Number of stacks per player.
        """
        self.stacks = [[] for _ in range(num_players * stacks_per_player)]
        self.top_cards = [None] * (num_players * stacks_per_player)

    def place_card(self, stack_index, card):
        """
        Place a card in a specific stack.

        Args:
            stack_index (int): The index of the stack (0-based).
            card (Card): The card to place.

        Raises:
            ValueError: If the stack index is invalid.
        """
        if not (0 <= stack_index < len(self.stacks)):
            raise ValueError("Invalid stack index")
        self.stacks[stack_index].append(card)
        self.top_cards[stack_index] = card

    def place_five_cards(self, player, start_stack_index):
        """
        Place the top 5 cards from a player's hand onto their attributed stacks.

        Args:
            player (Player): The player placing the cards.
            start_stack_index (int): The starting stack index for the player.
        """
        for i in range(5):
            if player.hand:
                self.place_card(start_stack_index + i, player.hand.pop())

    def collect_stacks(self, player, start_stack_index):
        """
        Collect all stacks attributed to a player and add them to the bottom of their hand.

        Args:
            player (Player): The player collecting the stacks.
            start_stack_index (int): The starting stack index for the player.
        """
        for i in range(5):
            stack_index = start_stack_index + i
            while self.stacks[stack_index]:
                player.hand.insert(0, self.stacks[stack_index].pop(0))

    def show_table(self):
        """
        Display the current state of the table.
        """
        for i, stack in enumerate(self.stacks):
            stack_str = ', '.join(map(str, stack)) if stack else "Empty"
            print(f"  Stack {i + 1}: {stack_str}")
        print("\nTop cards on all stacks:")
        print(', '.join(str(card) if card else "Empty" for card in self.top_cards))