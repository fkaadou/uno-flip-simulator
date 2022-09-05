#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 18:45:09 2022

@author: fouad
"""
from random     import shuffle
from statistics import mode as Mode

class Card:

    def __init__(self, val, color):
        
        self.color = color
        self.val   = val

    def __str__(self):
        return f'''({self.val}, {self.color})'''
    
    
class Holder:
    
    verbose = True
    
    def __init__(self, name, stack, verbose):
        self.name    = name
        self.stack   = stack
        self.verbose = verbose
        
    def __str__(self):
        for card in self.stack:
            print(card)
        print('-------------------------------')
        return f'Cards in {self.name}: {len(self.stack)}'

    def shuffle(self):
        shuffle(self.stack)
    
    def num_cards(self):
        return len(self.stack)
    
    def top_card(self):
        if len(self.stack) > 0:
            return self.stack[len(self.stack)-1]
        
    def draw(self, reserve=''):
        try:
            return self.stack.pop()
        except:
            self.reshuffle(reserve)
            return self.stack.pop()
        
    def add(self, card):
        self.stack.append(card)
 
    
    def reshuffle(self, reserve=''):
        if self.verbose: 
            print(f'{self.name} is empty. reshuffling with discard pile.')
        
        while reserve.num_cards() > 0:
            self.add(reserve.draw())
        
        self.shuffle()
        
        # add card to discard after reshuffling deck
        reserve.add(self.stack.pop())
    
class Player_official:
    
    verbose = True
    
    def __init__(self, name, hand, verbose):
        self.name    = name
        self.hand    = Holder(name, hand, verbose=verbose)
        self.verbose = verbose
        
    def draw(self, deck, num_cards, reserve, setup=False):
        for i in range(num_cards):
            if not (reserve.num_cards() == 1 and deck.num_cards() == 0):
                self.hand.stack.append(deck.draw(reserve))
                if not setup and self.verbose:
                    print(f'{self.name} drew:   {self.hand.top_card()}.')
            else:
                # if self.verbose:
                print(f'{self.name} tried to draw a card but deck and discard empty.')
            
    def play(self, deck, discard, action='', new_color=''):
        
        color_change = ''        
        top = discard.top_card()
        
        if new_color and self.verbose:
            print(f'new color {new_color}')
        
        color_discard = top.color
        val_discard   = top.val
        max_draw = 3
            
        
        
        # *** RESOLVE PREVIOUS PLAYER ACTION ***
        
        # Basically action == 'change'
        # update color if previous player changed color
        # change value to -1 so no cards match and player must find card 
        # that matches new color only
        if new_color:
            color_discard = new_color
            val_discard  = '-1' 
            if self.verbose:
                print(f'{self.name} must now play {new_color} cards.')
            
        if action=='plus2' or action=='plus4':
            num_cards = int(action[-1])
            self.draw(deck, num_cards, reserve=discard)
            if self.verbose:
                print(f'{self.name} drew {num_cards} card(s) from deck.')
            
        # skip turn
        if action == 'skip':
            if self.verbose:
                print(f'{self.name} skipped their turn.')
            return '', ''
        
        # ****************************************
        
        # PLAY 
        # Check 1:
        # check if card in hand matches top card color or value
        for i, card in enumerate(self.hand.stack):
            
            color = card.color
            val   = card.val

            # extra statement change cards are played in check 2 only
            if (color == color_discard or val == val_discard) and val != 'change':
                discard.add(self.hand.stack.pop(i))
            
                if self.verbose:
                    print(f'{self.name} playes {card} @ check 1')
                
                if val.isnumeric():
                    return '', color_change
                else:
                    return val, color_change
        
        # Check 2:
        # if here then no card matching color or value found
        # check to see if hand contains non-colored cards
        for i, card in enumerate(self.hand.stack):
            
            color = card.color
            val   = card.val

            # choose to change color to most color in hand
            if color == 'null':
                discard.add(self.hand.stack.pop(i))
                
                if self.verbose:
                    print(f'{self.name} playes {card} @ check 2')
                
                hand_colors = [card.color for card in self.hand.stack if card.color != 'null']
                
                if self.verbose:
                    print(f'hand colors: {hand_colors}')
                
               
                try:
                    color_change = Mode(hand_colors)
                except:
                    if self.hand.num_cards()==0:
                        return '',''
                    else:
                        # if all cards in hand are null then pick red
                        color_change = 'red'
                            
         
                if self.verbose:
                    print(f'{self.name} changes the color to {color_change}.')
                
                return val, color_change
        
        
        # Check 3:
        # if here then player has not cards to play
        # player must draw up to three cards
        count = 0
        while count<max_draw:
            
            if (discard.num_cards() == 1 and deck.num_cards() == 0):
                print('Empty deck.')
                return '', color_change
                
                 
            if deck.num_cards() == 0:
                deck.reshuffle(reserve=discard)
            
            deck_color = deck.top_card().color
            deck_val   = deck.top_card().val

                
            if deck_color == color_discard or deck_val == val_discard or deck_color == 'null':
                card =  deck.draw(reserve=discard)
                discard.add(card)
                
                if self.verbose:
                    print(f'{self.name} playes {card} from deck')
                
                # choose to change color to most color in hand
                if deck_color == 'null':
                    
                    hand_colors = [card.color for card in self.hand.stack if card.color != 'null']
                    
                    try:
                        color_change = Mode(hand_colors)
                    except:
                        # if all cards in hand are null then pick red
                        color_change = 'red'
                    
                    if self.verbose:
                        print(f'{self.name} changes the color to {color_change}.')

                if deck_val.isnumeric():
                    return '', color_change
                else:
                    return deck_val, color_change
             
            else:
                self.draw(deck, 1, reserve=discard)
            
            count+=1
                
        if count == max_draw:
            return '', color_change

    
class Player_house:
    
    verbose = True
    
    def __init__(self, name, hand, verbose):
        self.name    = name
        self.hand    = Holder(name, hand, verbose=verbose)
        self.verbose = verbose
        
    def draw(self, deck, num_cards, reserve, setup=False):
        for i in range(num_cards):
            if not (reserve.num_cards() == 1 and deck.num_cards() == 0):
                self.hand.stack.append(deck.draw(reserve))
                if not setup and self.verbose:
                    print(f'{self.name} drew:   {self.hand.top_card()}.')
            else:
                # if self.verbose:
                print(f'{self.name} tried to draw a card but deck and discard empty.')
            
    def play(self, deck, discard, action='', new_color=''):
        
        color_change = ''        
        top = discard.top_card()
        
        if new_color and self.verbose:
            print(f'new color {new_color}')
        
        color_discard = top.color
        val_discard   = top.val
        max_draw = 3
            
        
        
        # *** RESOLVE PREVIOUS PLAYER ACTION ***
        
        # Basically action == 'change'
        # update color if previous player changed color
        # change value to -1 so no cards match and player must find card 
        # that matches new color only
        if new_color:
            color_discard = new_color
            val_discard  = '-1' 
            if self.verbose:
                print(f'{self.name} must now play {new_color} cards.')
            
        if 'plus' in action:
            # check to see if holding a plus* card
            for i, card in enumerate(self.hand.stack):

                color = card.color
                val   = card.val
                
                if 'plus' in val:
                    discard.add(self.hand.stack.pop(i))
                    
                    if self.verbose:
                        print(f'{self.name} playes {card} @ plus check')
                    
                    # if playin plus2 player must also choose new color
                    if val=='plus4':
                            

                        hand_colors = [card.color for card in self.hand.stack if card.color != 'null']
                        
                        if self.verbose:
                            print(f'hand colors: {hand_colors}')
                    
                        try:
                            color_change = Mode(hand_colors)
                        except:
                            if self.hand.num_cards()==0:
                                return '',''
                            else:
                                # if all cards in hand are null then pick red
                                color_change = 'red'
  
                        if self.verbose:
                            print(f'{self.name} changes the color to {color_change}.')
                                          
                    new_plus = f'plus{int(action[4:]) + int(val[4:])}'
                    
                    return new_plus, color_change
            
            
            # if not plus cards in hand then draw
            num_cards = int(action[-1])
            self.draw(deck, num_cards, reserve=discard)
            if self.verbose:
                print(f'{self.name} drew {num_cards} card(s) from deck.')
            
        # skip turn
        if action == 'skip':
            if self.verbose:
                print(f'{self.name} skipped their turn.')
            return '', ''
        
        # ****************************************
        
        # PLAY 
        # Check 1:
        # check if card in hand matches top card color or value
        for i, card in enumerate(self.hand.stack):
            
            color = card.color
            val   = card.val

            # extra statement change cards are played in check 2 only
            if (color == color_discard or val == val_discard) and val != 'change':
                discard.add(self.hand.stack.pop(i))
            
                if self.verbose:
                    print(f'{self.name} playes {card} @ check 1')
                
                if val.isnumeric():
                    return '', color_change
                else:
                    return val, color_change
        
        # Check 2:
        # if here then no card matching color or value found
        # check to see if hand contains non-colored cards
        for i, card in enumerate(self.hand.stack):
            
            color = card.color
            val   = card.val

            # choose to change color to most color in hand
            if color == 'null':
                discard.add(self.hand.stack.pop(i))
                
                if self.verbose:
                    print(f'{self.name} playes {card} @ check 2')
                
                hand_colors = [card.color for card in self.hand.stack if card.color != 'null']
                
                if self.verbose:
                    print(f'hand colors: {hand_colors}')
                
               
                try:
                    color_change = Mode(hand_colors)
                except:
                    if self.hand.num_cards()==0:
                        return '',''
                    else:
                        # if all cards in hand are null then pick red
                        color_change = 'red'
                            
         
                if self.verbose:
                    print(f'{self.name} changes the color to {color_change}.')
                
                return val, color_change
        
        
        # Check 3:
        # if here then player has not cards to play
        # player must draw up to three cards
        count = 0
        while count<max_draw:
            
            if (discard.num_cards() == 1 and deck.num_cards() == 0):
                print('Empty deck.')
                return '', color_change
                
                 
            if deck.num_cards() == 0:
                deck.reshuffle(reserve=discard)
            
            deck_color = deck.top_card().color
            deck_val   = deck.top_card().val

                
            if deck_color == color_discard or deck_val == val_discard or deck_color == 'null':
                card =  deck.draw(reserve=discard)
                discard.add(card)
                
                if self.verbose:
                    print(f'{self.name} playes {card} from deck')
                
                # choose to change color to most color in hand
                if deck_color == 'null':
                    
                    hand_colors = [card.color for card in self.hand.stack if card.color != 'null']
                    
                    try:
                        color_change = Mode(hand_colors)
                    except:
                        # if all cards in hand are null then pick red
                        color_change = 'red'
                    
                    if self.verbose:
                        print(f'{self.name} changes the color to {color_change}.')

                if deck_val.isnumeric():
                    return '', color_change
                else:
                    return deck_val, color_change
             
            else:
                self.draw(deck, 1, reserve=discard)
            
            count+=1
                
        if count == max_draw:
            return '', color_change