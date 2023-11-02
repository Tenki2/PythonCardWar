import os
import random
import time

class cards:
    def __init__(self):#delete later
        pass
    
    deck = []

    def make_deck(self):
        suits = ["diamonds", "hearts", "clubs", "spades"]
        points = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12" ,"13"]
        for suit in suits:
            for point in points:
                self.deck.append([point, suit])
        random.shuffle(self.deck)
        return self.deck
        
class game:
    def __init__(self, rounds):
        self.rounds = rounds
        self.player1 = player("")
        self.player2 = player("")
        self.cards = cards()
    
    def play(self):
        for i in range(self.rounds+1):
            print("Round", i)
            self.cards.make_deck()
            self.player1.draw_card()
            print(self.player1.name, "drew", self.player1.hand[0][0], "of", self.player1.hand[0][1])
            self.player2.draw_card()
            print(self.player2.name, "drew", self.player2.hand[0][0], "of", self.player2.hand[0][1])
            if int(self.player1.hand[0][0]) > int(self.player2.hand[0][0]):
                print(self.player1.name, "wins")
                self.player1.score += 1
            elif int(self.player1.hand[0][0]) < int(self.player2.hand[0][0]):
                print(self.player2.name, "wins")
                self.player2.score += 1
            else:
                print("Tie")
            input("Press enter to continue")
class player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
    
    def draw_card(self):
        self.hand = []
        #print(cards.deck[0])
        self.hand.append(cards.deck.pop(0))
        #print(cards.deck[0])
        #print(self.hand)
        return self.hand



"""test = cards()
deck2 = test.make_deck()
#deck = test.shuffle_deck()
for i in range(len(test.make_deck())):
    print(deck2[i][0], "of", deck2[i][1])"""


card_game = game(5)
name = input("What is your name: ")
card_game.player1.name = name
card_game.player2.name = "Computer"
print(card_game.player1.name, "vs", card_game.player2.name)
card_game.play()
"""test = cards()
test.make_deck()
card_game.player1.draw_card()
"""



def main():
    pass
if __name__ == "__main__":
    main()
