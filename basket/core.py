import random

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

class Card(object):
    '''The Card class. 
    ''' 
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return '%s%s' %(self.suit, self.rank) 

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_point(self): 
        return VALUES[self.rank] 

    
class Deck(object):
    '''All the cards on the deck. 
    ''' 
    def __init__(self):
        self.deck = [Card(s, r) for r in RANKS for s in SUITS]
                        
    def shuffle(self):
        random.shuffle(self.deck)

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

class Player(object): 
    ''' player or dealer. 
    ''' 
    def __init__(self, dealer=True, chips=100): 
        self.dealer = dealer 
        self.cards = [] 
        self.stood = False 
        if dealer: 
            self.chips = float('inf') 
        else: 
            self.chips = chips 

    def stand(self): 
        self.stood = True 

    def add_card(self, card): 
        self.cards.append(card) 
    
    def clear_cards(self): 
        self.cards = [] 
        self.stood = False

    def get_chips(self): 
        return self.chips 

    def inc_chips(self, bet): 
        self.chips += bet 

    def dec_chips(self, bet): 
        self.chips -= bet 

    def get_points(self):
        rank_list = map(lambda c: c.get_rank(), self.cards) 
        points = sum(map(lambda c: c.get_point(), self.cards)) 

        if 'A' in rank_list:
            return points + 10 if points + 10 <= 21 else points

        return points 

    def get_second_value(self):
        '''the value of the known card of dealer's hand 
        ''' 
        return self.cards[0].get_point()

class Game(object): 
    
    def __init__(self): 
        self.started = False 
        self.deck = Deck() 
        self.player = Player(dealer=False) 
        self.dealer = Player(dealer=True) 
        self.bet = 1 

    def issue_card(self): 
        return self.deck.deal_card() 

    def start(self): 
        self.deck.shuffle() 

        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

        self.started = True 

    def stop(self): 
        self.started = False 
        self.player.clear_cards()
        self.dealer.clear_cards() 
        self.deck = Deck() 

    def get_player(self): 
        return self.player 

    def get_dealer(self): 
        return self.dealer 

    def get_bet(self): 
        return self.bet 

    def set_bet(self, bet): 
        self.bet = bet

    def restart(self): 
        self.start() 

