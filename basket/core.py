# -*- coding: utf-8 -*-

'''The core module of basket, providing basic data structures. 
''' 

import random

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {
    'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 
    'T':10, 'J':10, 'Q':10, 'K':10 }

class Card(object):
    '''The Card class. 
    ''' 
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return '[%s%s]' %(self.suit, self.rank) 

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
        return "Deck contains: " + ' '.join(map(str, self.deck))  

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
        '''calculate the maximum sum of points of the cards in hand. 
        ''' 
        rank_list = map(lambda c: c.get_rank(), self.cards) 
        points = sum(map(lambda c: c.get_point(), self.cards)) 

        for i in range(rank_list.count('A')):
            points = points + 10 if points + 10 <= 21 else points

        return points 

    def get_second_card(self):
        '''the known card of dealer's hand 
        ''' 
        return self.cards[1]

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

