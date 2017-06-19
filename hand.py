"""Module to hold the Hand object.

- A hand has from 2 to 5 cards in it.
- Cards are represented by the value and the suit.
- Values range from 2 to A and suits are C, D, S and H.

- The possible hands are:

    * High card
    * One pair
    * Two pairs
    * 3 of a kind
    * Straight
    * Flush
    * Full House
    * 4 of a kind
    * Straight Flush"""

import random
import os

# These are the global variables used by the module:
CARD_VALUES = list(range(2, 11)) + ["J", "Q", "K", "A"]
CARD_SUITS = ["H", "S", "C", "D"]
HAND_NAMES = ["High Card", "One Pair", "Two Pairs", "Three of a Kind",
              "Straight", "Flush", "Full House", "Four of a Kind",
              "Straight Flush"]
CARD_ORDER = dict(zip(CARD_VALUES, range(1,14)))

class Card():
    """A card has the attributes value and suit."""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __eq__(self, other_card):
        """Allows direct card comparison"""
        return self.suit == other_card.suit and self.value == other_card.value

    @property
    def name(self):

        suits_table = dict(zip(CARD_SUITS, ["Hearts", "Spades",
                                            "Clubs", "Diamonds"]))

        cards_table = dict(zip(CARD_VALUES, ["Two", "Three", "Four",
                                             "Five", "Six", "Seven",
                                             "Eight", "Nine", "Ten",
                                             "Jack", "Queen", "King",
                                             "Ace"]))

        return "{} of {}".format(cards_table[self.value],
                                 suits_table[self.suit])

class Hand():

    def __init__(self):
        self.name = None
        self.cards = []
        self.hand_types = {name: False for name in HAND_NAMES}

    def _generate_card_data_list(self):
        """Transfers the values and suits of the cards in the hand
           to a private list object."""

        # IDEA: cast the lists into sets for evaluation.
        self.value_list = set([card.value for card in self.cards])
        self.suit_list = set([card.suit for card in self.cards])

    def _generate_set_hand(self, card_list):
        """Generates a hand with the given cards."""
        for card in card_list:
            self.cards.append(card)

        self._generate_card_data_list()

    def _generate(self):
        """Generates a random hand with 5 cards."""
        # Seeding
        random.seed(os.urandom(random.randint(1, 1000)))
        while len(self.cards) != 5:
            new_card = Card(random.choice(CARD_VALUES),
                            random.choice(CARD_SUITS))
            # Solving the duplicated card problem. __eq__ is necessary.
            if new_card not in self.cards:
                self.cards.append(new_card)
        self._generate_card_data_list()
    def show_hand(self):
        """Prints all the cards in the hand"""
        print("This hand contains:\n")
        for card in self.cards:
            print(card.name)

        self.evaluate()
        for hand, state in self.hand_types.items():
            if state:
                print("This hand's type is %s" % hand)

    def _check_for_straight(self):
        """Returns a boolean variable stating if the hand is a
           straight or not."""

        # We'll need to generate a space for straights to be recognized:
        card_values_len = len(CARD_VALUES) - 4
        possible_straights = [CARD_VALUES[i:i+5] \
                for i in range(0, card_values_len)]

        # And there's the possibility of having a straight, Ace to Five:
        possible_straights.append(["A", 2, 3, 4, 5])

        # Going through the check
        for straight in possible_straights:
            # Things work best when you use a count to record the matches
            # for a straight
            straight_count = 0
            for value in self.value_list:
                if value in straight:
                    straight_count += 1

            if straight_count == 5:
                return True
            else:
                has_straight = False

        return has_straight

    def evaluate(self):
        """Checks what kind of hand it is and returns a string with
           its name and value when applicable."""

        # We're going to check the values of the cards using that value set
        # from earlier!
        # We'll also need to get a count list of the values in the hand:
        buf_list = [card.value for card in self.cards]
        count_list = [buf_list.count(card.value) for card in self.cards]

        # If the value set has a length of 5, you can have either a
        # High Card, Straight, Flush or Straight Flush
        if len(self.value_list) == 5:
            # Checking for a flush is quite straightforward
            # (no pun intended)
            if len(self.suit_list) == 1:
                self.hand_types["Flush"] = True

            # Checking for a straight:
            if self._check_for_straight():
                self.hand_types["Straight"] = True

            # If there's both a straight and a flush,
            # it's a Straight Flush:
            if self.hand_types["Straight"] and self.hand_types["Flush"]:
                self.hand_types["Straight"] = False
                self.hand_types["Flush"] = False
                self.hand_types["Straight Flush"] = True

            # If no condition has been met, it's a High Card:
            if not self.hand_types["Flush"] \
            and not self.hand_types["Straight"] \
            and not self.hand_types["Straight Flush"]:
                self.hand_types["High Card"] = True

        # For a length of 4, the only possibility is One Pair!
        if len(self.value_list) == 4:
            self.hand_types["One Pair"] = True

        # For a length of 3, it can be either a Two Pair or 3 of a Kind
        if len(self.value_list) == 3:
            if 3 in count_list:
                self.hand_types["3 of a Kind"] = True
            else:
                self.hand_types["Two Pair"] = True

        # For a length of 2, it can be either a Full House or 4 of a Kind
        if len(self.value_list) == 2:
            if 4 in count_list:
                self.hand_types["4 of a Kind"] = True
            else:
                self.hand_types["Full House"] = True

# Creating a deck
deck = [Card(value, suit) for value in CARD_VALUES for suit in CARD_SUITS]

for item in deck:
    print(item.name)

for i in range(200):
    h = Hand()
    print("Hand %s" % i)
    h._generate()
    h.show_hand()

