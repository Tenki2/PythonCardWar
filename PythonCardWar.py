import os
from random import randint
import time

class cards:
    def __init__(self):
        pass

    def make_deck(self):
        suits = ["diamonds", "hearts", "clubs", "spades"]
        points = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12" ,"13"]
        deck = []
        for suit in suits:
            for point in points:
                deck.append(point + " of " + suit)
        return deck


    
class game:
    def __init__(self):
        self.rounds = 0


class player:


card_game = game()
name = input("What is your name: ")

card_game.player1 = player(name)
card_game.player2 = player("computer")
card_game.player2.name = "Computer"
card_game.player1.score = 0
card_game.player2.score = 0
card_game.round = 1
print(card_game.player1.name, "vs", card_game.player2.name)
