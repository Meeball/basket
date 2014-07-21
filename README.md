# Basket 

A blackjack implementation in python. 

## Get Started

### Install 

```plain 
$ python setup.py install 
``` 
### Start a Game 

```plain 
$ blackjack 
``` 

### Or quick start from project

Go to the project directory and 
```
$ bin/blackjack
```

## Instructions

###Description

You are dealt an initial two-card hand and add together the value of their cards. Face cards (kings, queens, and jacks) are counted as ten points. You and the dealer can count his or her own ace as 1 point or 11 points. All other cards are counted as the numeric value shown on the card. After the initial two cards, you have the option of getting a "hit". In a given round, either you or the dealer wins by having a score of 21 or by having the highest score that is less than 21. Scoring higher than 21 (called "going bust") results in a loss. Same score with the dealer will result in a draw ("Push") with full wager back.

In summary, you can win over the dealer by any of the following situation:

* Get 21 points on your first two cards (called a blackjack), without a dealer blackjack;

* Reach a final score higher than the dealer without exceeding 21; or

* Let the dealer draw additional cards until his or her hand exceeds 21.


###New Game [n]

Type [n] whenever you want to start a new hand or give up the current hand. When you give up the current hand, your bet won't come back.

###Set Bet [b]

You have 100 chips with you when entering the game, and the default bet is one chip. Type [b] and you can change your bet before any round begins (minimum is 1 chip, maximum is your current chips).  
 
The game is over if all the chips are gambled. Your bet will win double, get back or lose your current bet if you accordingly win,tie or lose the hand.

###Hit [h]

Type [h] to take another card each time. It would stop hitting if you went bust.

###Stand [s]

Type [s] to end your round and go to dealer's turn. 

###Double [d]

When you got your initial cards, type [d] before any hitting if you want to double your bet and hit only once. After the double, it would go to dealer's turn automatically.

###Print [p]

Print instant status including game ongoing status and current chips and bet.

###Quit [q]

Quit the game whenever you want.

 

## Features

* The dealer has to take hits until his cards total 17 or more points.

* If the initial hand is *Blackjack*, the game will go to settlement automatically.

* Count current hand total value for the player.

* The player can change his bet before the next hand begins.


## Contact Me  

You can send email to Zhi Yang [cathybhn@gmail.com](mailto:cathybhn@gmail.com)

