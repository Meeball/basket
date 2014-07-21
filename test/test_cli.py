
import pytest 

from basket.core import Game 
from basket.core import Card 

from basket.cli import stand
from basket.cli import check 

CHIPS_NUM = 100 

@pytest.fixture() 
def game(): 
    return Game() 

@pytest.fixture() 
def winning_game(): 
    g = Game() 
    g.start() 
    player = g.get_player() 
    dealer = g.get_dealer() 
    
    player.chips = 100 
    player.cards = [Card('C', 'A'), Card('S', 'A'), Card('H', '3')] 
    dealer.cards = [Card('D', '6'), Card('S', '8')] 

    return g 

@pytest.fixture() 
def losing_game(): 
    g = Game()  
    g.start() 
    player = g.get_player() 
    dealer = g.get_dealer() 
    
    g.deck.deck = [Card('C', '6')] 
    player.chips = CHIPS_NUM
    player.cards = [Card('C', 'A'), Card('S', 'A'), Card('H', '3')] 
    dealer.cards = [Card('D', '6'), Card('S', '8')] 

    return g 

def test_start(): 
    game = Game() 
    game.start() 
    player = game.get_player() 
    dealer = game.get_dealer() 

    assert 2 == len(player.cards) 
    assert 2 == len(player.cards) 

def test_check(winning_game): 
    player = winning_game.get_player() 
    check(winning_game, finished=True) 
    assert not winning_game.started
    assert player.chips == CHIPS_NUM + winning_game.get_bet() 

def test_stand(losing_game): 
    player = losing_game.get_player() 
    stand(losing_game) 
    assert not losing_game.started 
    assert player.chips == CHIPS_NUM - losing_game.get_bet() 

