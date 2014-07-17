#!/usr/bin/env python 

import sys 

from basket.core import Game 
from basket.core import Card 
from basket.core import Player 

def stand(game, player): 
    pass 

def hit(game, player): 
    player.add_card(game.issue_card()) 

def check(game, player, dealer): 
    pass 

def player_stats(player): 
    if player.dealer: 
        print 'Dealer: ' 
    else: 
        print 'Player: ' 

def print_usage(): 
    print 'Available Commands'
    print 's --start    start the game.' 
    print 'h --hit      fetch a card.' 
    print 't --stand    stand.' 
    print 'r --restart  give up and start a new round.' 
    print 'b --bet      set bet value at the beginning.' 
    print 'd --double   double the bet.' 
    print 'h --help     print usage.' 

def main(): 
    print 'Welcome to Basket!' 
    print 'type h for instructions' 

    game = Game() 
    player = None 
    dealer = None 

    while True: 
        if player: 
            sys.stdout.write('<player> ') 
        else: 
            sys.stdout.write('> ') 

        cmd = sys.stdin.readline() 
        if cmd in ['s', 'start']: 
            game.start() 
            player = game.get_player() 
            dealer = game.get_dealer() 
            player_stats(player) 
            player_stats(dealer) 

        elif cmd in ['h', 'hit']: 
            hit(game, player) 


