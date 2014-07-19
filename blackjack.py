import pygame
import random
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = 100
player_value = 0
dealer_value = 0
bet = 1

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        self.card = []

    def __str__(self):
##        test = ""
##        for i in range(len(self.card)):
##            test += " " + str(self.card[i])
        return list(self.card)

    def add_card(self, card):
        return self.card.append(card)

    def get_value(self):
        hand_rank_list = []
        value = 0
        
        for i in range(len(self.card)):
            hand_rank_list.append(self.card[i].get_rank())
            value += VALUES[self.card[i].get_rank()]
            
        if "A" in hand_rank_list:
            if value + 10 <= 21:
               value = value + 10
        return value

# first value is the value of the known card of dealer's hand 
    def get_first_value(self):
        first_value = 0
        first_value = VALUES[self.card[0].get_rank()]
        return first_value
    
    def draw(self, canvas, pos):
        for card in self.card:
            pos[0] += 100
            card.draw(canvas, pos)
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                test = Card(suit, rank)
                self.deck.append(test)
                
    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    def deal_card(self):
        return self.deck.pop(-1)
        
    def __str__(self):
        test = ""
        for i in range(len(self.deck)):
            test += " " + str(self.deck[i])
        return "Deck contains" + test     


#define event handlers for buttons
def setbet():
    global bet,score, betmessage
    bet=int(raw_input("Enter your bet(minimum 1): "))
    score -= bet
    betmessage = "Bet  " + str(bet)

def deal():
    global outcome, message, score, in_play, deck, player_hand, dealer_hand, player_value, dealer_value
    score -= bet
    betmessage = "Bet  " + str(bet)

    if score < 0 :
        message = "Game Over"
    else:
        if in_play == False:
            outcome = ""
            message = "Hit or stand?"
            in_play = True
            player_hand = Hand()
            dealer_hand = Hand()
        
        
            deck = Deck()
            deck.shuffle()
            
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())

            player_value = player_hand.get_value()
            dealer_value = dealer_hand.get_value()

            if player_hand.get_value() == 21:
               message = "Blackjack! "
               if player_hand.get_value() == dealer_hand.get_value():
                  message += " Push"
                  score += bet
               else:
                  message += " You Win!"
                  score += 2*bet
                  in_play = False
            
        else:
              outcome = "You give up and lose."
              message = "New deal?"
              in_play = False
      

  
def hit():
    global in_play, score, outcome, message, player_hand, player_value
    
    # if the hand is in play, hit the player
    if in_play == True:
        player_hand.add_card(deck.deal_card())
        player_value = player_hand.get_value()
        
    # if busted, assign a message to outcome, update in_play and score
    if (player_hand.get_value() > 21) and (in_play == True):
        in_play = False
        outcome = "You went bust and lose."
        message = "New deal?"
        player_value = player_hand.get_value()
        
def double():
    global in_play, score, outcome, message, player_hand, player_value, bet
    # double the bet
    score -= bet
    bet = 2*bet
    betmessage = "Bet  " + str(bet)
    # if the hand is in play, hit the player
    if in_play == True:
        player_hand.add_card(deck.deal_card())
        player_value = player_hand.get_value()
        
        # if busted, assign a message to outcome, update in_play and score
        if (player_hand.get_value() > 21):
            in_play = False
            outcome = "You went bust and lose."
            message = "New deal?"
            player_value = player_hand.get_value()

        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            dealer_value = dealer_hand.get_value()
        if dealer_hand.get_value() > 21:
            outcome = "Dealer went bust and you win."
            message = "New deal?"
            score += 2*bet
            
            
        elif player_hand.get_value() > dealer_hand.get_value():
            outcome = "You win."
            message = "New deal?"
            score += 2*bet

        elif player_hand.get_value() == dealer_hand.get_value():
            outcome = "Push."
            message = "New deal?"
            score += bet    

        else:
            outcome = "You lose."
            message = "New deal?"            
    
   
    bet = bet/2
   
    
def stand():
    global in_play, score, outcome, message, dealer_hand, player_value, dealer_value
    player_value = player_hand.get_value()
    if (player_hand.get_value() > 21) and (in_play == True):
        in_play = False
        outcome = "You went bust and lose."
        message = "New deal?"
        dealer_value = dealer_hand.get_value()
        
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            dealer_value = dealer_hand.get_value()
        if dealer_hand.get_value() > 21:
            outcome = "Dealer went bust and you win."
            message = "New deal?"
            score += 2*bet
            
            
        elif player_hand.get_value() > dealer_hand.get_value():
            outcome = "You win."
            message = "New deal?"
            score += 2*bet

        elif player_hand.get_value() == dealer_hand.get_value():
            outcome = "Push."
            message = "New deal?"
            score += bet    

        else:
            outcome = "You lose."
            message = "New deal?"            
            
    in_play = False


# draw handler    
def draw(canvas):
    global dealer_hand, player_hand, player_value
   
    dealer_hand.draw(canvas, [0, 200])
    player_hand.draw(canvas, [0, 400])
    
    if in_play == False:
        canvas.draw_text("Dealer:  " + str(dealer_value), [100, 180], 30, "Black")
    else:
        canvas.draw_text("Dealer:  ? + " + str(dealer_value - dealer_hand.get_first_value()), [100, 180], 30, "Black")
    canvas.draw_text("Player:  " + str(player_value), [100, 380], 30, "Black")    
    canvas.draw_text("Blackjack", [150, 100], 50, "Blue")
    canvas.draw_text("Chips " + str(score)+"     Bet "+ str(bet), [400, 100], 30, "Black")
    canvas.draw_text(outcome, [250, 180], 30, "Black")
    canvas.draw_text(message, [300, 380], 30, "Black")
    
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Double", double, 200)
frame.add_button("Change Bet", setbet, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

