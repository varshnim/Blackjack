import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.all_cards = []
        for rank in ranks:
            for suit in suits:
                self.all_cards.append(Card(suit, rank))

    def deal_one(self):
        return self.all_cards.pop()

    def shuffle_deck(self):
        random.shuffle(self.all_cards)


class Person:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.dealt_cards = []
        self.card_value = 0

    def calculate_card_value(self):
        for card in self.dealt_cards:
            self.card_value += card.value
        return self.card_value

    def print_cards(self):
        for dealt_card in self.dealt_cards:
            print(dealt_card)

    def __str__(self):
        return self.name + " has $" + str(self.chips) + " left"

    def deal_a_card(self, deck):
        temp = deck.deal_one()
        self.dealt_cards.append(temp)
        self.card_value += temp.value


if __name__ == "__main__":
    new_deck = Deck()
    new_deck.shuffle_deck()

    current_player_bet = 0

    # STEP ONE
    player_name = input("What's your name? ")
    player_chips = int(input("Enter the amount to be converted to chips: "))
    print(
        f"Converting ${player_chips} to chips...\n\n\nWelcome to the BlackJack Table!"
        f"\nI'm Jarvis and I'll be your dealer tonight.")

    player = Person(player_name, player_chips)
    dealer = Person("Dealer", 1000)

    # Placing bet and checking if player has enough chips for it
    ask_to_bet = True
    while ask_to_bet:
        current_player_bet = int(input(f"Place your bet, {player_name}. \n"))
        if current_player_bet <= player.chips:
            player.chips -= current_player_bet
            ask_to_bet = False
            print("You've bet successfully!")
        else:
            print("You don't have sufficient chips to place that bet. Try again with a lower amount.")

    # STEP TWO
    # Dealing
    for i in range(2):
        player.deal_a_card(new_deck)
        dealer.deal_a_card(new_deck)

    print(f"\n{player.name}, your cards are: ")
    for i in player.dealt_cards:
        print(i)
    print("\nDealer's exposed card:")
    print(dealer.dealt_cards[0])

    # STEP 3
    to_hit = True
    while to_hit:
        if player.card_value == 21:
            if len(player.dealt_cards) == 2:
                player.chips += current_player_bet * 2.5
            else:
                player.chips += current_player_bet * 2
            print("That's a Natural! You have a blackjack!")
            print(f"You've won ${current_player_bet * 2} and have ${player.chips} left to bet!")
            to_hit = False
            quit()
        elif player.card_value > 21:
            print(f"That's a bust! You've lost this round. You have ${player.chips} left to bet!")
            to_hit = False
            quit()
        else:
            hit_or_stay = input("Would you like to hit or stand?(hit/stand): ").lower()
            if hit_or_stay == "hit":
                player.deal_a_card(new_deck)
                print(f"\n{player.name}, your new card is")
                print(player.dealt_cards[-1])
            else:
                to_hit = False

    # STEP 4
    dealer_to_hit = True
    print(f"\nDealer's other card:{dealer.dealt_cards[1]}")
    while dealer_to_hit:
        if dealer.card_value < 17:
            dealer.deal_a_card(new_deck)
            print(f"Dealer has drawn {dealer.dealt_cards[-1]}")
        elif dealer.card_value >= 21:
            player.chips += (current_player_bet * 2)
            print(f"Dealer has a bust! Player wins ${current_player_bet * 2} and has ${player.chips} left to bet!")
            dealer_to_hit = False
            quit()
        else:
            dealer_to_hit = False

    # STEP 5
    player_diff = 21 - player.card_value
    dealer_diff = 21 - dealer.card_value

    print("\n\n\n")

    print("PLAYER CARDS")
    player.print_cards()
    print(f"Player's card value: {player.card_value}\n")

    print("DEALER CARDS")
    dealer.print_cards()
    print(f"Dealer's card value: {dealer.card_value}\n")

    if player_diff < dealer_diff:
        player.chips += (current_player_bet * 2)
        print(f"Player wins ${current_player_bet * 2} this round!")
    elif dealer_diff < player_diff:
        print(f"Player lost bet of ${current_player_bet} this round!")
        dealer.chips = current_player_bet
        current_player_bet = 0
    else:
        print(f"Player and dealer at a standoff! {player.name} collects bet of ${current_player_bet}!")
        player.chips += current_player_bet

    print(f"Player's has ${player.chips} to bet.")
