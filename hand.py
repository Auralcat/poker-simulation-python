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

# These are the global variables used by the module:
CARD_VALUES = list(range(2, 11)) + ["J", "Q", "K", "A"]
CARD_SUITS = ["H", "S", "C", "D"]
HAND_NAMES = ["High Card", "One Pair", "Two Pairs", "Three of a Kind",
              "Straight", "Flush", "Full House", "Four of a Kind",
              "Straight Flush"]

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
    def _generate(self):
        """Generates a random hand with 5 cards."""
        # Seeding
        random.seed(os.urandom(random.randint(1, 1000)))
        while len(self.cards) != 5:
            self.cards.append(Card(random.choice(CARD_VALUES),
                                   random.choice(CARD_SUITS)))
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

    def evaluate(self):
         """Checks what kind of hand it is and returns a string with
            its name and value when applicable."""

         # We're going to check the values of the cards using that value set from earlier!
         # We'll also need to get a count list of the values in the hand:
         buf_list = [card.value for card in self.cards]
         count_list = [buf_list.count(card.value) for card in self.cards]

         # If the value set has a length of 5, you can have either a
         # High Card, Straight, Flush or Straight Flush
         if len(self.value_list) == 5:
             if len(self.suit_list) == 1:
                 self.hand_types["Flush"] = True

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
