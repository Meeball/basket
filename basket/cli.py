#!/usr/bin/env python 

import sys 
import time 

from basket.core import Game 
from basket.core import Card 
from basket.core import Player 

HIT_INTERVAL = 1

def stand(game): 
    player = game.get_player() 
    dealer = game.get_dealer() 
    player.stand() 
    while dealer.get_points() < 17: 
        hit(game, dealer) 
        if not game.started: 
            return 
    
    check(game, finished=True) 

def double(game): 
    player = game.get_player() 
    nb = 2 * game.get_bet()
    if nb > player.get_chips(): 
        print "Insufficient Chips. Press 'q' to exit." 
        return 

    game.set_bet(nb) 
    print "Bet is set to %d." %(game.get_bet()) 
    hit(game, player) 
    stand(game) 

def hit(game, player): 
    time.sleep(HIT_INTERVAL) 
    try: 
        card = game.issue_card()
    except IndexError as e: 
        print 'run out of cards on the deck.'
        game.stop() 
        return 

    player.add_card(card) 

    check(game, finished=False) 

def win(game): 
    player_points = game.get_player().get_points()
    dealer_points = game.get_dealer().get_points()

    if dealer_points > 21:
        print '[Win] Dealer went bust'
    else:
        print '[Win] You got %d while dealer got %d.' %(
            player_points, dealer_points) 
    player = game.get_player() 
    player.inc_chips(game.get_bet()) 

    game.stop()
    print 'New game?[n] or Quit[q]'

def lose(game): 
    player_points = game.get_player().get_points()
    dealer_points = game.get_dealer().get_points()

    if player_points > 21:
        print '[Lose] You went bust'
    else:
        print '[Lose] You got %d while dealer got %d.' %(
            player_points, dealer_points) 

    player = game.get_player() 
    player.dec_chips(game.get_bet()) 
    if player.dec_chips <= 0: 
        print "Game Over. Press 'q' to exit."

    game.stop()
    print 'New game?[n] or Quit[q]'

def draw(game): 
    dealer_points = game.get_dealer().get_points()
    print '[Draw] You and dealer both got %d.' %(dealer_points) 
    game.stop() 

def check(game, finished=False): 
    if not game.started: 
        return
    
    print_status(game) 

    player_points = game.get_player().get_points()
    dealer_points = game.get_dealer().get_points()

    if player_points > 21: 
        lose(game)
    elif dealer_points > 21: 
        win(game) 
    elif player_points == 21 and dealer_points == 21: 
        draw(game) 
    elif player_points == 21: 
        win(game) 
    elif dealer_points == 21: 
        lose(game) 

    if finished: 
        if player_points < dealer_points: 
            lose(game) 
        elif player_points > dealer_points: 
            win(game) 
        else: 
            draw(game)
    

def player_stats(player): 
    if player.dealer: 
        print 'Dealer: ' 
    else: 
        print 'Player: ' 

def print_usage(): 
    print 'Available Commands'
    print '    n --new      start a new round.' 
    print '    p --print    print the status of current game.' 
    print '    h --hit      fetch a card.' 
    print '    s --stand    stand.' 
    print '    b --bet      set bet value at the beginning.' 
    print '    d --double   double the bet.' 
    print '    q --quit     exit.' 

def print_status(game): 
    player = game.get_player() 
    dealer = game.get_dealer() 

    if game.started:  
        print "Your hand: %s total %d." %(
                str(' '.join(map(str, player.cards))), 
                player.get_points()) 

        if player.stood: 
            print "Dealer's hand: %s total %d." %(
                    str(' '.join(map(str, dealer.cards))), 
                    dealer.get_points())
        else: 
            print "Dealer's revealed card is %s." %(
                    str(dealer.get_second_card()))
    else : 
        print "Not in play."
        print "Current bet: %d  Your remaining chips: %d" %(
                game.get_bet(), player.get_chips()) 

def main(): 
    print 'Welcome to Blackjack!' 
    print 'type [help] for instructions' 

    game = Game() 
    player = game.get_player() 
    dealer = game.get_dealer()

    print 'Default bet: %d  Remaining chips: %d ' %(
                game.get_bet(), player.get_chips()) 

    while True: 
        if game.started: 
            sys.stdout.write('<player> ') 
        else: 
            sys.stdout.write('> ') 

        cmd = sys.stdin.readline().strip() 
        if cmd in ['n', 'new']: 
            if game.started: 
                sys.stdout.write('Comfirm to give up and start a new game. [Y/N] ') 
                ans = sys.stdin.readline().strip() 
                if ans in ['', 'y', 'Y']: 
                    player.dec_chips(game.get_bet()) 
                    player.clear_cards() 
                    dealer.clear_cards() 
                    game.stop() 
                    print_status(game) 
                continue
            
            if game.get_bet() > player.get_chips(): 
                print "Insufficient Chips. Press 'q' to exit." 
                continue 

            game.start() 
            check(game) 

        elif cmd in ['p', 'print']: 
            print_status(game)

        elif cmd == 'help': 
            print_usage() 

        elif cmd in ['h', 'hit']: 
            if not player.dealer and player.stood: 
                print "You have already stood." 
                continue 

            hit(game, player) 

        elif cmd in ['s', 'stand']: 
            stand(game) 

        elif 'b'in cmd or 'bet' in cmd: 
            if game.started: 
                print "The game is already started"
                continue 

            if len(cmd.split()) != 2: 
                print "You need to set a value to bet. e.g. b 2" 
                continue 

            val = int(cmd.split()[1]) 
            
            game.set_bet(val)

            print "Bet is set to %d" %game.get_bet()

        elif cmd in ['d', 'double']: 
            if not game.started: 
                print "Round has not started yet." 
                continue 
            if len(player.cards) != 2: 
                print "You've already hit %d cards." %(len(player.cards) - 2) 

            double(game) 

        elif cmd in ['q', 'quit']: 
            sys.exit(0) 

