from classes import Card, Deck, Player, Table
import random

def play_game():
    # Initialize the deck and shuffle it
    deck = Deck()
    deck.shuffle()

    # Create two players
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    # Split the deck into two halves
    half = len(deck.cards) // 2
    player1.receive_cards(deck.cards[:half])
    player2.receive_cards(deck.cards[half:])

    # Initialize the table
    table = Table(num_players=2)
    table.place_five_cards(player1, 0)
    table.place_five_cards(player2, 5)

    # Counters
    current_rounds_since_stuck = 0  # Includes rounds before the first stuck event
    rounds_between_stuck = []
    total_rounds = 0
    total_stuck_events = 0

    # Function to handle pairing logic
    def handle_pair(table, players):
        nonlocal current_rounds_since_stuck, rounds_between_stuck, total_stuck_events
        top_cards = table.top_cards

        for i, card1 in enumerate(top_cards):
            for j, card2 in enumerate(top_cards):
                if i < j and card1 and card2 and card1.face_value == card2.face_value:
                    probabilities = random.choices([
                        (0, 2),  # Player 1 places 2 cards
                        (1, 2),  # Player 2 places 2 cards
                        (0, 1, 1)  # Both players place 1 card
                    ], weights=[0.4, 0.4, 0.2])[0]

                    if len(probabilities) == 2:  # Single player places cards
                        chosen_player = players[probabilities[0]]
                        if len(chosen_player.hand) >= 2:
                            table.place_card(i, chosen_player.hand.pop())
                            table.place_card(j, chosen_player.hand.pop())
                        else:
                            return players[1 - probabilities[0]].name
                    else:  # Both players place 1 card each
                        if players[0].hand:
                            table.place_card(i, players[0].hand.pop())
                        else:
                            return players[1].name
                        if players[1].hand:
                            table.place_card(j, players[1].hand.pop())
                        else:
                            return players[0].name
                    current_rounds_since_stuck += 1
                    return None

        # No pairs found
        total_stuck_events += 1
        rounds_between_stuck.append(current_rounds_since_stuck)
        current_rounds_since_stuck = 0

        table.collect_stacks(players[0], 0)
        table.collect_stacks(players[1], 5)
        table.place_five_cards(players[0], 0)
        table.place_five_cards(players[1], 5)
        return None

    # Main game loop
    players = [player1, player2]
    while True:
        total_rounds += 1
        current_rounds_since_stuck += 1  # Increment the counter at the start of each round

        # Check if any player has no cards left
        if not player1.hand:
            return {
                "winner": "Player 2",
                "total_rounds": total_rounds,
                "rounds_between_stuck": rounds_between_stuck,
                "total_stuck_events": total_stuck_events
            }
        if not player2.hand:
            return {
                "winner": "Player 1",
                "total_rounds": total_rounds,
                "rounds_between_stuck": rounds_between_stuck,
                "total_stuck_events": total_stuck_events
            }

        # Handle pairs and moves
        winner = handle_pair(table, players)
        if winner:
            return {
                "winner": winner,
                "total_rounds": total_rounds,
                "rounds_between_stuck": rounds_between_stuck,
                "total_stuck_events": total_stuck_events
            }


print(play_game())