#my code is also available on repl.it: https://replit.com/@Tenki204/course-work

import os #used to clear the screen
import random #used to get random numbers
import time #used to add delays to the game
import pickle #used to serialize the game object
import platform #used to find what operating system the script is running on
from termcolor import colored, cprint #used to output colored text

def clear(): #clears the terminal screen depending on the operating system
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class cards:
    def __init__(self):
        self.deck = [] #used to store the deck
        self.make_deck() #first create the deck
        self.shuffle_deck() #then shuffle it
        self.split_deck() #then split it

    def make_deck(self):
        suits = ["diamonds", "hearts", "clubs", "spades"]
        points = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12" ,"13", "14"]# using numers for the backend and converting them to words for the user
        for suit in suits: #for each card im each suit add the card to the deck
            for point in points: 
                self.deck.append([point, suit])
        self.deck.append(["16", "special"])#add the special cards to the deck
        self.deck.append(["16", "special"])
        self.deck.append(["16", "special"])
        self.deck.append(["15", "jocker"])#add the jockers to the deck
        self.deck.append(["15", "jocker"])
        return self.deck
    
    def shuffle_deck(self):
        for i in range(random.randint(1, 10)): #shuffle the deck a random amount of times
            random.shuffle(self.deck)
        return self.deck

    def split_deck(self):
        half = len(self.deck) // 2 #finds the middle of the deck
        return self.deck[:half], self.deck[half:] #returns both halves of the deck

class game:
    def __init__(self, rounds, slot):
        self.rounds = rounds #used to set the amount of rounds in round based mode
        self.slot = slot #used to determine what slot to save to
        self.cards = cards() #create a new deck
        deck1, deck2 = self.cards.split_deck() #give each part of the deack to a variable
        self.player1 = player(deck1) #create a new player with the first half of the deck
        self.player2 = player(deck2) #create a new player with the second half of the deck
        self.round = 1 #used to keep track of what round the game is on even after loading a save
        self.DeckIsEmpty = False #used to check if a players deck is empty
    
    def save_game(self):
        with open(f'{self.slot}.pkl', 'wb') as f: #open/make a .pkl file with the name of the slot
            pickle.dump(self, f) #pickle the game object and save it to a file
            cprint("Game saved", "cyan", "on_red")

    @staticmethod #this decarator makes the method static so it can be called without an instance of the class
    def load_game(slot):
        with open(f'{slot}.pkl', 'rb') as f: #open the .pkl file
            cprint("Game loaded", "cyan", "on_red")
            return pickle.load(f) #unpickle the game object and return it
            

    def war(self):
        """
        if there is a tie this method is called
        """
        print(colored("YOU ARE NOW AT WAR!!!!", 'yellow'))
        input("Press enter to continue")
        clear()
        for i in range(3):#both players draw 3 cards
            if len(self.player1.cards) < 1 or len(self.player2.cards) < 1: #checks if the players can draw cards 
                if len(self.player1.cards) < 1:#if they cant then set their deck to empty so the game ends
                    self.player1.DeckIsEmpty = True
                if len(self.player2.cards) < 1:
                    self.player2.DeckIsEmpty = True
                return
            self.player1.draw_card()
            self.player2.draw_card()
        print("Both players drew 3 cards who ever wins this round wins the war")
        self.player1.draw_card()#draw another card to decide who wins the war
        self.player2.draw_card()
        self.round_win_check() #compare the cards to see who wins the war

    def round_win_check(self):
        if self.player1.hand[-1][1] == "skipped" and self.player2.hand[-1][1] == "skipped": #check if both players skipped their turn
            print("Both players skipped their turn")
            self.player1.skip_turn = False
            self.player2.skip_turn = False
        elif self.player1.hand[-1][1] == "skipped": #check if player 1 skipped their turn
            print(f"{colored(self.player2.name, 'green')} wins by default")
            for card in self.player2.hand: #add player2's hand to their score
                self.player2.score += int(card[0])
            self.player2.skip_turn = False #reset the skip turn variable
        elif self.player2.hand[-1][1] == "skipped": #check if player 2 skipped their turn
            print(f"{colored(self.player1.name, 'red')} wins by default")
            for card in self.player1.hand: #add player1's hand to their score
                self.player1.score += int(card[0])
            self.player2.skip_turn = False #reset the skip turn variable
        elif int(self.player1.hand[-1][0]) > int(self.player2.hand[-1][0]): #check if player 1's card is higher than player 2's
            print(f"{colored(self.player1.name, 'red')} wins")
            for card in self.player1.hand: #add player1's hand to their score
                self.player1.score += int(card[0])
        elif int(self.player1.hand[-1][0]) < int(self.player2.hand[-1][0]): #check if player 2's card is higher than player 1's
            print(f"{colored(self.player2.name, 'green')} wins")
            for card in self.player2.hand: #add player2's hand to their score
                self.player2.score += int(card[0])
        else: #if both cards are the same then call the war method
            print("Tie")
            self.war()          

    def play(self):
        while self.player1.DeckIsEmpty == False and self.player2.DeckIsEmpty == False: #while both players still have cards
            clear() #clear the screen
            self.player1.empty_hand() #empty both players hands
            self.player2.empty_hand()
            print(f"Round {self.round}") #print what round it is
            if self.player1.skip_turn: #check if a player is skipping their turn
                self.player1.hand.append(["0", "skipped"]) #add a card to their hand to represent that they skipped their turn1
            else:#if they are not skipping their turn then draw a card
                self.player1.draw_card()
                if not self.player1.skip_turn and not self.player2.skip_turn: #dont output what card they drew if a player is skipping their turn
                    self.player1.card_output('red')#output what card they drew in red
                self.player1.special_card_handler(self.player2) #check if the card they drew is a special card
            time.sleep(1) #wait 1 second
            if self.player2.skip_turn:
                self.player2.hand.append(["0", "skipped"])
            else:
                self.player2.draw_card()
                if not self.player1.skip_turn and not self.player2.skip_turn: #dont output what card they drew if a player is skipping their turn
                    self.player2.card_output('green')
                self.player2.special_card_handler(self.player1)
            time.sleep(2) #wait 2 seconds
            self.round_win_check() #check who won the round
            print("") #print a blank line
            time.sleep(1) #wait 1 second
            print(colored(self.player1.name, 'red'), "score:", self.player1.score) #print the players scores
            print(colored(self.player2.name, 'green'), "score:", self.player2.score)
            print("")
            self.save_game() #
            print("")
            choice = input("type 'exit' if you want to leave the game: ") #ask the user if they want to exit the game
            if choice == "exit" or choice == "exit": #if they do then exit the game
                return
            clear() #clear the screen
            self.round += 1 #increment round
            if len(self.player1.cards) == 0: #check if a players deck is empty
                self.player1.DeckIsEmpty = True
            if len(self.player2.cards) == 0:
                self.player2.DeckIsEmpty = True
            if self.rounds > 0: #if the game is in round based mode then check if the game is over
                if self.round > self.rounds:
                    self.player1.DeckIsEmpty = True
        print(colored(self.player1.name, 'red'), "score:", self.player1.score) #print the final scores
        print(colored(self.player2.name, 'green'), "score:", self.player2.score)
        print("")
        print("")
        if self.player1.score > self.player2.score: #check who won the game
            print(f"{colored(self.player1.name.upper(), 'red')} WINS THE GAME!!") 
        elif self.player1.score < self.player2.score:
            print(f"{colored(self.player2.name.upper(), 'green')} WINS THE GAME!!")
        else:
            print("Its a tie!!")
        input("Press enter to continue")
        os.remove(f'{self.slot}.pkl') #when the game is over delete the save file

class player:
    def __init__(self, deck):
        self.name = input("What is your name: ") #get the players name
        self.score = 0 #used to keep track of the players score
        self.hand = [] #used to store the players hand
        self.cards = deck #used to store the players half of the deck
        self.DeckIsEmpty = False #used to check if the players deck is empty    
        self.skip_turn = False #used to check if the player is skipping their turn
        self.card_number = "" #used to store the number of the card the player drew
        self.card_suit = "" #used to store the suit of the card the player drew
        
    def draw_card(self): #draws a card from the deck
        self.hand.append(self.cards.pop(0)) #add the card to the players hand from the deck
        self.card_number = self.card_convert() #convert the card number to the card name
        self.card_suit = self.hand[-1][1] #get the suit of the card
        return self.hand #return the players hand

    def card_output(self, colour): #outputs the card the player drew
        if self.card_number == "16": #check if the card is special
            print(f"{colored(self.name, colour)} drew a special card")
        elif self.card_number == "0": #check if the card is a skiped
            print(f"{colored(self.name, colour)}'s turn is skipped")
        elif self.card_number == "15": #check if the card is a jocker
            print(f"{colored(self.name, colour)} drew a jocker")
        else: #if the card is not special then output the card name and suit
            print(f"{colored(self.name, colour)} drew {self.card_number} of {self.card_suit}")

    def empty_hand(self): #empties the players hand
        self.hand = []
        return self.hand

    def special_card_handler(self, opponent): #determines what effect the special card has
        if self.hand[-1][1] == "special": #check if the card is special
            special_card_effect = random.randint(1, 3) #randomly choose a special card effect
            if special_card_effect == 1: #if the effect is 1 then draw 2 cards
                if len(self.cards) >= 2: #check if there are enough cards in the deck to draw 2
                    print("")
                    print("The special card's effect is: ")
                    print("You get to draw 2 cards")
                    print("")
                    self.hand.pop(0) #remove the special card from the hand
                    self.draw_card() #draw 2 cards
                    self.draw_card()
                    self.hand.append(["16", "special"]) #add back the special card at the end of the hand so its used when deciding who wins the round
                else: #if there are not enough cards in the deck then draw 1 card instead
                    print("")
                    print("The special card's effect is: ")
                    print("You get to draw 1 card")
                    print("")
                    self.hand.pop(0) #remove the special card from the hand
                    self.draw_card()
                    self.hand.append(["16", "special"]) #add back the special card at the end of the hand so its used when deciding who wins the round
            elif special_card_effect == 2: #if the effect is 2 then skip the opponents turn
                print("")
                print("The special card's effect is: ")
                print("Your opponent's turn is skipped")
                print("")
                opponent.skip_turn = True #set the opponents skip turn variable to true
            elif special_card_effect == 3: #if the effect is 3 then double the players points for the round
                print("")
                print("The special card's effect is: ")
                print("Your points are doubled for this round")
                print("")
                self.hand[-1][0] = str(int(self.hand[-1][0]) * 2) #double the points of the players card
                

    def card_convert(self): #converts the card number to the card name
        self.card_number = self.hand[-1][0] #get the card number
        if self.card_number == "11": 
            return "Jack"
        elif self.card_number == "12":
            return "Queen"
        elif self.card_number == "13":
            return "King"
        elif self.card_number == "14":
            return "Ace"
        else: #if the card is not special then return the card number
            return self.card_number

def main_menu(): #the main menu of the game
    while True: #loop the menu
        game_over = False #used to break multiple loops
        clear()
        print("Welcome to Card War")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = input("What would you like to do: ")
        if choice == "1": #1 if the user wants to start a new game
            while choice != "b" and not game_over: #b is used to go back to the previous menu
                clear()
                print("Please select a slot to save to") #ask the user what slot they want to save to
                slot = input("or type 'b' to go back: ")
                if slot in ["1", "2", "3", "4", "5"]: #check if the slot is valid
                    while choice != "3" and not game_over: #3 is used to go back to the previous menu
                        clear()
                        print("What game mode would you like to play")
                        print("1. Clasic")
                        print("2. Round based")
                        print("3. Back")
                        choice = input("What would you like to do: ") #ask the user what game mode they want to play
                        if choice == "1": #1 is clasic mode
                            card_game = game(0, slot) #0 is used to tell the game that its not in round based mode
                            print(colored(card_game.player1.name, 'red'), "vs", colored(card_game.player2.name, 'green'))
                            card_game.play() #start the game
                            game_over = True #used to go back to the start of the main menu
                        elif choice == "2": #2 is round based mode
                            rounds = int(input("How many rounds would you like to play: "))
                            card_game = game(rounds, slot) #create a new game object with the amount of rounds the user chose
                            print(colored(card_game.player1.name, 'red'), "vs", colored(card_game.player2.name, 'green'))
                            card_game.play() #start the game
                            game_over = True #used to go back to the start of the main menu
                        elif choice == "3": #3 is used to go back to the start of the main menu
                            game_over = True #although the game may not be over this can still be used to break multiple loops
                elif slot == "b": #b is used to go back to the start of the main menu
                    break #break the loop
                else:
                    print("Invalid choice")
                    input("Press enter to continue")
        elif choice == "2": #2 is used to load a game
            while choice != "b": #b is used to go back to the start of the main menu
                clear()
                for i in range(1, 6): #check if there is a save file in each slot
                    filename = f"{i}.pkl" 
                    if filename in os.listdir(): #lists all pkl files in the directory
                        print(f"Save slot {i}: Save file exists")
                    else:
                        print(f"Save slot {i}: No save file")
                print("")
                print("b. Back")
                choice = input("What save slot would you like to load from: ")
                if choice in ["1", "2", "3", "4", "5"]: #check if the slot is valid
                    try: #try to load the game
                        card_game = game.load_game(int(choice)) #load the game
                        card_game.play() #start the game
                        break
                    except FileNotFoundError: #if there is no save file then tell the user and continue the loop
                        cprint("No saved game found", "cyan", "on_red")
                        input("Press enter to continue")
                elif choice == "b": #b is used to go back to the start of the main menu
                    break
                else: #if the slot is not valid then tell the user and continue the loop
                    print("Invalid choice")
                    input("Press enter to continue")

        elif choice == "3": #3 is used to exit the game
            break
        else: #if the choice is not valid then tell the user and continue the loop
            print("Invalid choice")
            input("Press enter to continue")



if __name__ == "__main__": #if the script is run directly then run the main menu function
    main_menu()
