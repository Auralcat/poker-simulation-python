#!usr/bin/python3
# -*- encoding: utf-8 -*-

"""Another shot at simulating a poker game"""

import random
import os

class Card():
    value = None
    suit = None

# Just the card values here
card_values = list(range(2, 11)) + ["J", "Q", "K", "A"]

# Now, the suits (clubs, diamonds, hearts, spades):
suits = ["C", "D", "S", "H"]

# Now we pack everything together WITH LIST COMPREHENSION!
deck = [str(card)+suit for card in card_values for suit in suits]

print(deck)
print("There are %s cards in the deck." % len(deck))

# Drawing a card:
random.seed(os.urandom(random.randint(0,1000)))
print("The drawn card is %s." % random.choice(deck))

# Drawing a hand:
for i in range(1, 10):
    print("The drawn hand is %s." % random.sample(deck, 5))
