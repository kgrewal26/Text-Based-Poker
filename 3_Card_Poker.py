#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/

import random
import os
from operator import attrgetter

class Card:

    def __init__(self, **kwargs):
        if 'suit' in kwargs: self.suit = kwargs['suit']
        if 'number' in kwargs: self.number = kwargs['number']
    
    def __repr__(self):
        return repr(f'{self.number}{self.suit}')
    
    def __eq__(self, other):
        
        if not isinstance(other, Card):
            return notImplemented
        
        return self.suit == other.suit and self.number == other.number
    
    def suit(self, suit = None):
        if suit: self.suit = suit
        try: return self.suit
        except AttributeError: return None

    def number(self, num = None):
        if num: self.number = num
        try: return self.number
        except AttributeError: return None
    
    def __str__(self):
        return f'{self.number()}{self.suit()}'

class Deck:

    def __init__(self, cards, size):
        self._cards = cards
        self._size = size
    
    def cards(self, cards = None):
        if cards: self._cards = cards
        try: return self._cards
        except AttributeError: return None

    def size(self, size = None):
        if size: self._size = size
        try: return self._size
        except AttributeError: return None
    
    def increaseSize(self):
        size(size() + 1)
    
    def shuffle(self):
        random.shuffle(self.cards())
    
    def drawCards(self):
        
        userCards = [self.cards()[0], self.cards()[1], self.cards()[2]]
        compCards = [self.cards()[3], self.cards()[4], self.cards()[5]]
        
        userHand = Hand(userCards)
        compHand = Hand(compCards)
        
        userHand.checkStatus()
        compHand.checkStatus()
        return (userHand, compHand)
        
    def __str__(self):
        stringText = ''
        for card in self.cards():
            stringText = stringText +f'{card.number}{card.suit} '  
        return stringText + f'\nSize: {self.size()}'

class Hand():
    def __init__(self, hCards):
        self._hCards = hCards
        self._status = "Nothing"
        self._ranking = 0
        self.checkStatus()
        
    def hCards(self, hcards = None):
        if hcards: self._hCards = hcards
        try: return self._hCards
        except AttributeError: return None
    
    def status(self, status = None):
        if status: self._status = status
        try: return self._status
        except AttributeError: return None
        
    def ranking(self, ranking = None):
        if ranking: self._ranking = ranking
        try: return self._ranking
        except AttributeError: return None
    
    def sortHand(self): 
        
        return sorted(self.hCards(), key = attrgetter('number'))
            
    
    def checkStraight(self):
        
        self.hCards(self.sortHand())
        cardNums = []        
        for card in self.hCards():
            cardNums.append(card.number)
            
        firstNum = self.hCards()[0].number
        straightNums = [firstNum, firstNum + 1, firstNum + 2]
        
        return cardNums == straightNums
    
    def checkSameSuit(self):
        
        firstSuit = self.hCards()[0].suit
        
        for card in self.hCards():
            
            if (card.suit != firstSuit):
                return False
            
        return True
    
    
    def checkTriple(self):
        
        firstNum = self.hCards()[0].number
        
        for card in self.hCards():
            if card.number != firstNum:
                return False
            
        return True
    
    def checkDouble(self):
        
        if ((self.hCards()[0].number == self.hCards()[1].number) or (self.hCards()[0].number == self.hCards()[2].number) or (self.hCards()[1].number == self.hCards()[2].number)):
            return True
        else:
            return False
    
    def checkStatus(self):
        
        self.sortHand()
        
        if ((self.checkSameSuit()) and (self.checkStraight())):
            self.status('Straight Same Suit')
            self.ranking(5)
        elif self.checkTriple():
            self.status('Triple')
            self.ranking(4)
        elif self.checkStraight():
            self.status('Straight')
            self.ranking(3)
        elif self.checkDouble():
            self.status('Double')
            self.ranking(2)
        elif self.checkSameSuit():
            self.status('Same Suit')
            self.ranking(1)
    
    def __str__(self):
       
        stringText = 'Cards: '
        
        for card in self.hCards():
            stringText = stringText + f'{card.number}{card.suit} '
        
        return stringText + f'    You Have a: {self.status()}' 

class Player():

    def __init__(self, name, balance):
        self._name = name
        self._hand = None
        self._balance = balance
        
    def hand(self, hand = None):
        if hand: self._hand = hand
        try: return self._hand
        except AttributeError: return None
    
    def balance(self, balance = None):
        if balance: self._balance = balance
        try: return self._balance
        except AttributeError: return None
    
    def name(self):
        return self._name
    
    def __str__(self):
        
        return f'{self.name()} Balance: {self.balance()}        Hand: {self.hand()}'
    
    def __repr__(self):
        return f'{self.name()} Balance: {self.balance()} Hand: {self.hand()}'
    
class Game():
    
    def __init__(self):
        self._player = Player('User', 500)
        self._comp = Player('Comp', 500)
        
    def player(self, player = None):
        if player: self._player = player
        try: return self._player 
        except AttributeError: return None
    
    def comp(self, comp = None):
        if comp: self._comp = comp
        try: return self._comp 
        except AttributeError: return None
    
    
    def createDeck(self):
        
        suits = ('A','D', 'S', 'C')
        number  = 1
        cards = []
        
        while (number <= 13):
            for suit in suits:
                cards.append(Card(suit = suit, number = number))
            number += 1
       
        return Deck(cards, len(cards))
        
        
    def playGame(self):
        
        deck = self.createDeck()
        
        print ('\n\n*******************STARTING NEW ROUND*******************')
        
        deck.shuffle()
        hands = deck.drawCards()
        
        self.player().hand(hands[0])  
        self.comp().hand(hands[1])
        
        print(self.player())
        print(f'Computer Balance: {self.comp().balance()}    Computer Cards: __ __ __\n\n')
        
        bet = 0
        
        while ((bet < 50) or (bet > self.player().balance())):
            try:
                bet = input(f'What would you like to bet (min 50) (max {self.player().balance()}): ')
                bet = int(bet)
            except ValueError:
                print('Incorrect Input, try Again.')
                bet = 0
        
        print(f'You bet: {bet} and the computer matches that.')
        
        print(f'\nYour Hand: {self.player().hand().hCards()}  Computer Hand: {self.comp().hand().hCards()}')
        
        self.findWinner(bet)
        
        print ('\n\n**********************END OF ROUND**********************')
        
    
    def findWinner(self, bet):
        
        if (self.player().hand().ranking() > self.comp().hand().ranking()):
            print(f'\n{self.player().hand().status()} beats {self.comp().hand().status()}, {self.player().name()} wins the round!')
            
            if (bet >= self.comp().balance()):
                self.comp().balance(1)
                print('\nThe computer has gone bankrupt!')
            else:
                self.comp().balance(self.comp().balance() - bet)
                
            self.player().balance(self.player().balance() + bet)
            
        elif (self.player().hand().ranking() < self.comp().hand().ranking()):
            print(f'\n{self.comp().hand().status()} beats {self.player().hand().status()}, {self.comp().name()} wins the round!')
            
            if (bet == self.player().balance()):
                self.player().balance(1)
                print('\nThe User has gone bankrupt!')
            else:
                self.player().balance(self.player().balance() - bet)

            self.comp().balance(self.comp().balance() + bet)
        else:
            print(f'\n{self.player().hand().status()} is the same as {self.comp().hand().status()}, this rounds a tie!')
    
    def findGameWinner(self):
        if (self.player().balance() > self.comp().balance()):
            return f'{self.player().name()} wins the game!'
        elif (self.comp().balance() > self.player().balance()):
            return f'{self.comp().name()} wins the game!'
        
        return 'Both the user and computer have the same ending balance - this games a tie!'

game = Game()

decision = ' '

print("Welcome to 3 Card Poker!")

while ((decision != 'N') and (game.player().balance() > 50) and (game.comp().balance() > 50)):
    game.playGame()
    
    decision = input('\nWould you like to continue (Y/N): ')
    
    while ((decision != 'Y') and (decision != 'N')):
        print("\nInvalid Input, Try Again. Make sure you are entering Y or N")
        decision = input('\nWould you like to continue (Y/N): ')

print('\nThat concludes the game...\n')
print(game.findGameWinner())
print('\nPlease play again soon!')

#done so that the command prompt doesnt automatically closed - for the exe file.
input('')
