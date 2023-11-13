import os
import random
import time
import pickle
import platform
from termcolor import colored, cprint

def clear():
    """
    This function clears the terminal screen depending on the operating system
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class cards:
    """
    This class creates a deck of cards and splits it in half
    """
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
        self.deck.append(["16", "special"])
        self.deck.append(["16", "special"])
        self.deck.append(["16", "special"])
        self.deck.append(["15", "jocker"])
        self.deck.append(["15", "jocker"])
        return self.deck
    
    def shuffle_deck(self):
        for i in range(random.randint(1, 10)): #shuffle the deck a random amount of times
            random.shuffle(self.deck)
        return self.deck

    def split_deck(self):
        half = len(self.deck) // 2 #finds the middle of the deck
        return self.deck[:half], self.deck[half:]

class game:
    def __init__(self, rounds, slot):
        self.rounds = rounds
        self.slot = slot
        self.cards = cards()
        deck1, deck2 = self.cards.split_deck()
        self.player1 = player(deck1)
        self.player2 = player(deck2)
        self.round = 1
        self.DeckIsEmpty = False
    def save_game(self):
        with open(f'{self.slot}.pkl', 'wb') as f:
            pickle.dump(self, f)
            cprint("Game saved", "cyan", "on_red")

    @staticmethod #this decarator makes the method static so it can be called without an instance of the class
    def load_game(slot):
        with open(f'{slot}.pkl', 'rb') as f:
            return pickle.load(f)
            cprint("Game loaded", "cyan", "on_red")

    def war(self):
        print(colored("YOU ARE NOW AT WAR!!!! >:3", 'yellow'))
        input("Press enter to continue")
        clear()
        for i in range(3):
            if len(self.player1.cards) < 1 or len(self.player2.cards) < 1:
                if len(self.player1.cards) < 1:
                    self.player1.DeckIsEmpty = True
                if len(self.player2.cards) < 1:
                    self.player2.DeckIsEmpty = True
                return
            self.player1.draw_card()
            self.player2.draw_card()
        print("Both players drew 3 cards who ever wins this round wins the war")
        self.player1.draw_card()
        self.player2.draw_card()
        self.round_win_check()

    def round_win_check(self):
        if self.player1.hand[-1][1] == "skipped" and self.player2.hand[-1][1] == "skipped":
            print("Both players skipped their turn")
            self.player1.skip_turn = False
            self.player2.skip_turn = False
        elif self.player1.hand[-1][1] == "skipped":
            print(f"{colored(self.player2.name, 'green')} wins by default")
            for card in self.player2.hand:
                self.player2.score += int(card[0])
            self.player2.skip_turn = False
        elif self.player2.hand[-1][1] == "skipped":
            print(f"{colored(self.player1.name, 'red')} wins by default")
            for card in self.player1.hand:
                self.player1.score += int(card[0])
            self.player2.skip_turn = False
        elif int(self.player1.hand[-1][0]) > int(self.player2.hand[-1][0]):
            print(f"{colored(self.player1.name, 'red')} wins")
            for card in self.player1.hand:
                self.player1.score += int(card[0])
        elif int(self.player1.hand[-1][0]) < int(self.player2.hand[-1][0]):
            print(f"{colored(self.player2.name, 'green')} wins")
            for card in self.player2.hand:
                self.player2.score += int(card[0])
        else:
            print("Tie")
            self.war()          

    def play(self):
        while self.player1.DeckIsEmpty == False and self.player2.DeckIsEmpty == False:
            clear()
            self.player1.empty_hand()
            self.player2.empty_hand()
            print(f"Round {self.round}")
            if self.player1.skip_turn:
                self.player1.hand.append(["0", "skipped"])
            else:
                self.player1.draw_card()
                if not self.player1.skip_turn and not self.player2.skip_turn: #dont output what card they drew if a player is skipping their turn
                    self.player1.card_output('red')
                self.player1.special_card_handler(self.player2)
            time.sleep(1)
            if self.player2.skip_turn:
                self.player2.hand.append(["0", "skipped"])
            else:
                self.player2.draw_card()
                if not self.player1.skip_turn and not self.player2.skip_turn: #dont output what card they drew if a player is skipping their turn
                    self.player2.card_output('green')
                self.player2.special_card_handler(self.player1)
            time.sleep(2)
            self.round_win_check()
            print("")
            time.sleep(1)
            print(colored(self.player1.name, 'red'), "score:", self.player1.score)
            print(colored(self.player2.name, 'green'), "score:", self.player2.score)
            print("")
            self.save_game()
            print("")
            choice = input("type 'exit' if you want to leave the game: ")
            if choice == "exit" or choice == "exit":
                return
            clear()
            self.round += 1
            if len(self.player1.cards) == 0:
                self.player1.DeckIsEmpty = True
            if len(self.player2.cards) == 0:
                self.player2.DeckIsEmpty = True
            if self.rounds > 0:
                if self.round > self.rounds:
                    self.player1.DeckIsEmpty = True
        print(colored(self.player1.name, 'red'), "score:", self.player1.score)
        print(colored(self.player2.name, 'green'), "score:", self.player2.score)
        print("")
        print("")
        if self.player1.score > self.player2.score:
            print(f"{colored(self.player1.name.upper(), 'red')} WINS THE GAME!!")
        elif self.player1.score < self.player2.score:
            print(f"{colored(self.player2.name.upper(), 'green')} WINS THE GAME!!")
        else:
            print("Its a tie!!")
        input("Press enter to continue")
        os.remove(f'{self.slot}.pkl')

class player:
    def __init__(self, deck):
        self.name = input("What is your name: ")
        self.score = 0
        self.hand = []
        self.cards = deck
        self.DeckIsEmpty = False
        self.skip_turn = False
        self.card_number = ""
        self.card_suit = ""
        
    def draw_card(self):
        self.hand.append(self.cards.pop(0))
        self.card_number = self.card_convert()
        self.card_suit = self.hand[-1][1]
        return self.hand

    def card_output(self, colour):
        if self.card_number == "16":
            print(f"{colored(self.name, colour)} drew a special card")
        elif self.card_number == "0":
            print(f"{colored(self.name, colour)}'s turn is skipped")
        elif self.card_number == "15":
            print(f"{colored(self.name, colour)} drew a jocker")
        else:
            print(f"{colored(self.name, colour)} drew {self.card_number} of {self.card_suit}")

    def empty_hand(self):
        self.hand = []
        return self.hand

    def special_card_handler(self, opponent):
        if self.hand[-1][1] == "special":
            special_card_effect = random.randint(1, 3)
            if special_card_effect == 1:
                if len(self.cards) >= 2:
                    print("")
                    print("The special card's effect is: ")
                    print("You get to draw 2 cards")
                    print("")
                    self.hand.pop(0)
                    self.draw_card()
                    self.draw_card()
                    self.hand.append(["16", "special"])
            elif special_card_effect == 2:
                print("")
                print("The special card's effect is: ")
                print("Your opponent's turn is skipped")
                print("")
                opponent.skip_turn = True
            elif special_card_effect == 3:
                print("")
                print("The special card's effect is: ")
                print("Your points are doubled for this round")
                print("")
                self.hand[-1][0] = str(int(self.hand[-1][0]) * 2)
                

    def card_convert(self):
        self.card_number = self.hand[-1][0]
        if self.card_number == "11":
            return "Jack"
        elif self.card_number == "12":
            return "Queen"
        elif self.card_number == "13":
            return "King"
        elif self.card_number == "14":
            return "Ace"
        else:
            return self.card_number

def main_menu():
    while True:
        game_over = False
        clear()
        print("Welcome to Card War")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = input("What would you like to do: ")
        if choice == "1":
            while choice != "b" and not game_over:
                clear()
                slot = int(input("Please select a slot to save to: "))
                if slot in [1, 2, 3, 4, 5]:
                    while choice != "3" and not game_over:
                        clear()
                        print("What game mode would you like to play")
                        print("1. Clasic")
                        print("2. Round based")
                        print("3. Back")
                        choice = input("What would you like to do: ")
                        if choice == "1":
                            card_game = game(0, slot)
                            print(colored(card_game.player1.name, 'red'), "vs", colored(card_game.player2.name, 'green'))
                            card_game.play()
                            game_over = True
                            break
                        elif choice == "2":
                            rounds = int(input("How many rounds would you like to play: "))
                            card_game = game(rounds, slot)
                            print(colored(card_game.player1.name, 'red'), "vs", colored(card_game.player2.name, 'green'))
                            card_game.play()
                            game_over = True
                elif slot == "b":
                    break
                else:
                    print("Invalid choice")
                    input("Press enter to continue")
        elif choice == "2":
            while choice != "b":
                clear()
                for i in range(1, 6):
                    filename = f"{i}.pkl"
                    if filename in os.listdir():
                        print(f"Save slot {i}: Save file exists")
                    else:
                        print(f"Save slot {i}: No save file")
                print("")
                print("b. Back")
                choice = input("What save slot would you like to load from: ")
                if choice in ["1", "2", "3", "4", "5"]:
                    try:
                        card_game = game.load_game(int(choice))
                        card_game.play()
                        break
                    except FileNotFoundError:
                        cprint("No saved game found", "cyan", "on_red")
                        input("Press enter to continue")
                elif choice == "b":
                    break
                else:
                    print("Invalid choice")
                    input("Press enter to continue")

        elif choice == "3":
            break
        else:
            print("Invalid choice")
            input("Press enter to continue")
def main():
    main_menu()



if __name__ == "__main__":
    main()
