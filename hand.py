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
import functools

CARD_VALUES = list(range(2, 11)) + ["J", "Q", "K", "A"]
CARD_SUITS = ["H", "S", "C", "D"]
HAND_TYPES = {"High Card": False,
              "One Pair": False,
              "Two Pairs": False,
              "Three of a Kind": False,
              "Straight": False,
              "Flush": False,
              "Full House": False,
              "Four of a Kind": False,
              "Straight Flush": False}

class Card():
    """A card has the attributes value and suit."""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

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

    hand_types = {"High Card": False,
                  "One Pair": False,
                  "Two Pairs": False,
                  "Three of a Kind": False,
                  "Straight": False,
                  "Flush": False,
                  "Full House": False,
                  "Four of a Kind": False,
                  "Straight Flush": False}

    def __init__(self):
        self.name = None
        self.cards = []
        self._nullify_hand()

    def _generate(self):
        """Generates a random hand with 5 cards."""
        # Seeding
        random.seed(os.urandom(random.randint(1, 1000)))
        while len(self.cards) != 5:
            self.cards.append(Card(random.choice(CARD_VALUES),
                                   random.choice(CARD_SUITS)))

    def show_hand(self):
        """Prints all the cards in the hand"""
        print("This hand contains:\n")
        for card in self.cards:
            print(card.name)

        self.evaluate()
        for hand, state in self.hand_types.items():
            if state:
                print("This hand's type is %s" % hand)

    def _nullify_hand(self):
        """Sets all the values for the hand type dictionary to False"""
        for key in self.hand_types:
            self.hand_types[key] = False

    def evaluate(self):
        """Checks what kind of hand it is and returns a string with
           its name and value when applicable."""

        # We need to dump the strings into two arrays for values and suits
        value_dump = []
        suit_dump = []

        for card in self.cards:
            value_dump.append(card.value)
            suit_dump.append(card.suit)

        # Now we need toself search the hand for the patterns
        for card in self.cards:
            print("Checking for cards with the value %s" % card.value)
            print(value_dump.count(card.value))
            # If there's two cards with the same value, it's a pair.
            if value_dump.count(card.value) == 2:
                self.hand_types["One Pair"] = True

            # If there's one more pair, you have... two pairs!
            if value_dump.count(card.value) == 2 and self.hand_types["One Pair"]:
                self._nullify_hand()
                self.hand_types["Two Pairs"] = True

            # For three cards of the same value in the hand, it's 3 of a kind
            if value_dump.count(card.value) == 3:
                self._nullify_hand()
                self.hand_types["3 of a Kind"] = True

            # When you have consecutive cards (e.g.: 2 to 6), it's a straight

            # If all cards in the hand have the same suit, it's a flush
            if suit_dump.count(card.suit) == len(self.cards):
                self.hand_types["Flush"] = True

            # If there's one pair and three of a kind, it's a full house
            if self.hand_types["One Pair"] and self.hand_types["3 of a Kind"]:
                self._nullify_hand()
                self.hand_types["Full House"] = True

            # If there are 4 cards with the same value, it's 4 of a kind
            if value_dump.count(card.value) == 4:
                self._nullify_hand()
                self.hand_types["4 of a Kind"] = True

            # If there's a straight and a flush, it's a straight flush
            if self.hand_types["Straight"] and self.hand_types["Flush"]:
                self._nullify_hand()
                self.hand_types["Straight Flush"] = True

        # If there's no pattern, it's a high card
        buf = functools.reduce(lambda x,y: x and y, self.hand_types.values())
        if not buf:
            self.hand_types["High Card"] = True

# Creating a deck
deck = [Card(value, suit) for value in CARD_VALUES for suit in CARD_SUITS]

for item in deck:
    print(item.name)

for i in range(20):
    h = Hand()
    print("Hand %s" % i)
    h._generate()
    h.show_hand()
