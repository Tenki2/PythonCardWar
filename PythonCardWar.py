import os
import random
import time
import sys #delete later
from termcolor import colored, cprint

class cards:
    def __init__(self):
        self.deck = []
        self.make_deck()
        self.shuffle_deck()
        self.split_deck()
    def make_deck(self):
        suits = ["diamonds", "hearts", "clubs", "spades"]
        points = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12" ,"13", "14"]
        for suit in suits:
            for point in points:
                self.deck.append([point, suit])
        return self.deck
    
    def shuffle_deck(self):
        for i in range(random.randint(1, 10)):
            random.shuffle(self.deck)
        return self.deck

    def split_deck(self):
        half = len(self.deck) // 2
        return self.deck[:half], self.deck[half:]

class game:
    def __init__(self, rounds):
        self.rounds = rounds
        self.cards = cards()
        deck1, deck2 = self.cards.split_deck()
        self.player1 = player(deck1)
        self.player2 = player(deck2)
        

    def play(self):
        for i in range(self.rounds):
            print(f"Round {i+1}")
            self.player1.draw_card()
            print(f"{colored(self.player1.name, 'red')} drew {self.player1.card_name} of {self.player1.card_suit}")
            self.player2.draw_card()
            print(f"{colored(self.player2.name, 'green')} drew {self.player2.card_name} of {self.player2.card_suit}")
            if int(self.player1.hand[0][0]) > int(self.player2.hand[0][0]):
                print(f"{colored(self.player1.name, 'red')} wins")
                self.player1.score += int(self.player1.hand[0][0])
            elif int(self.player1.hand[0][0]) < int(self.player2.hand[0][0]):
                print(f"{colored(self.player2.name, 'green')} wins")
                self.player2.score += int(self.player2.hand[0][0])
            else:
                print("Tie")
            input("Press enter to continue")
            os.system("cls")
        print(colored(self.player1.name, 'red'), "score:", self.player1.score)
        print(colored(self.player2.name, 'green'), "score:", self.player2.score)
        if self.player1.score > self.player2.score:
            print(f"{colored(self.player1.name, 'red')} wins!!")
        elif self.player1.score < self.player2.score:
            print(f"{colored(self.player2.name, 'green')} wins!!")
        else:
            print("Its a tie!!")
        
        def war(self):
            pass
class player:
    def __init__(self, deck):
        self.name = input("What is your name: ")
        self.score = 0
        #self.hand = []
        self.cards = deck#cards()

    def draw_card(self):
        self.hand = []
        self.hand.append(self.cards.pop(0))
        self.card_name = self.card_convert()
        self.card_suit = self.hand[0][1]
        return self.hand

    def card_convert(self):
        for i in range(len(self.hand)):
            if self.hand[i][0] == "11":
                return "Jack"
            elif self.hand[i][0] == "12":
                return "Queen"
            elif self.hand[i][0] == "13":
                return "King"
            elif self.hand[i][0] == "14":
                return "Ace"
            else:
                return self.hand[i][0]
def main():
    card_game = game(5)
    print(colored(card_game.player1.name, 'red'), "vs", colored(card_game.player2.name, 'green'))
    input("Press enter to start")
    os.system("cls")
    card_game.play()
    print(card_game.player1.hand)
    print("")
    print(card_game.player2.hand)


if __name__ == "__main__":
    main()
