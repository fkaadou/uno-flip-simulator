#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 19:34:17 2022

@author: fouad
"""

from classes import Card, Holder, Player_official, Player_house
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import multiprocessing
from funx import percentile

# PARAMETERS

original_stdout = sys.stdout
# sys.stdout = original_stdout

# log = open('log', 'w')
# sys.stdout = log

N = 10000      # number of games
turn_count = np.zeros(N)
num_players = 6
verbose = False

player_setup = '''
player%s = Player_official('player%s', [], verbose=verbose)
player%s.draw(deck, 7, reserve=discard, setup = True)
all_players.append(player%s)
if verbose:
    print(player%s.name)
    print('----------------')
    print(player%s.hand)
'''

# read cards from file
file = open('list_of_cards', 'r')
lines = file.readlines()
file.close()

all_cards = [line.rstrip('\n').split('\t') for line in lines]

all_cards = [Card(all_cards[i][0],all_cards[i][1]) for i,c in enumerate(all_cards)]

start = time.time()

def game():
    
    Player_official('name', [], verbose)
    Player_house('name', [], verbose)
    
    # GAME SETUP
    if verbose:
        print('****************************************')
        print('***               SETUP              ***')
        print('****************************************')
        print('\n')
    
    
    # construct deck
    deck = Holder('Deck', all_cards.copy(), verbose=verbose)
    deck.shuffle()
    
    # initialize discard pile
    discard = Holder('Discard', [], verbose=verbose)
    
    while not deck.top_card().val.isnumeric():    # make sure starting card is a number card
        deck.shuffle()
    
    
    discard.add(deck.draw(reserve=deck))
    
    # setup players
    turn = 0
    
    all_players = []
    winner = False
    action, color_change = '', ''
    
    for i in range(num_players):
        exec (player_setup % (i,i,i,i,i,i))
        if verbose: print('\n')
    
    if verbose:
        # show first card
        print(f'Top Card: {discard.top_card()}\n')
        
        
        #PLAY
        print('****************************************')
        print('***               PLAY               ***')
        print('****************************************')


    while not winner:
        
        turn+=1
        if verbose:
            print(f'\nTurn #{turn}')
            
        for player in all_players:
                    
            action, color_change = player.play(deck, discard, action=action, new_color=color_change)
            # print(f'action: {action},  color_change: {color_change}')
            
            # check if playe won
            if player.hand.num_cards()==0:
                if verbose:
                    print(f'{player.name} WINS!!!')
                winner = True
                break
            
            
            if action == 'switch':
                n = all_players.index(player)
                all_players = all_players[:n][::-1] + all_players[n+1:][::-1] + [all_players[n]]    
                if verbose:
                    print('Turn has reversed.')
                break
            
            if verbose:
                print('\n')
                print(player.hand)
                print('\n')
            
    return turn
    


start = time.time()

num_cpu = multiprocessing.cpu_count()
turn_count = Parallel(n_jobs=num_cpu)(delayed(game)() for j in tqdm(range(N)))

end = time.time()
original_stdout.write(f'Elapsed time: {end-start:.2f}s \n')

# log.close()    

# save turn_counnt variable
if 'Player_official' in player_setup:
    np.savetxt(f'uno_{num_players}_players', turn_count, fmt='%i')
elif 'Player_house' in player_setup:
    np.savetxt(f'uno_house_{num_players}_players', turn_count, fmt='%i')
    
fig, ax1 = plt.subplots(figsize=(16,10))
    
y, bins, patches = plt.hist(x=turn_count, bins=int(max(turn_count)-min(turn_count)), density=True, stacked=True)
plt.title(f'Num. Players: {num_players} - Num. of Games: {N}', fontsize=30)
plt.xlabel('# of Turns', fontsize=28)
plt.ylabel('Probability', fontsize=28)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.xlim(0,200)

cum_sum = np.array([sum(y[:i+1]) for i in range(len(y))])
x = np.concatenate(([0,1,2,3], bins[:-1]))
cum_sum = np.concatenate(([0,0,0,0], cum_sum))

ax2 = ax1.twinx()
ax2.plot(x, cum_sum, lw=3, color='tab:orange')
ax2.set_ylabel('Cumulative Probability', fontsize=  22,  rotation=270)
ax2.yaxis.set_label_coords(1.1, 0.5)
ax2.tick_params(labelsize=22)
ax2.set_ylim(0,1.1)

cum_sum = np.around(cum_sum, 2)
perc = percentile(x, cum_sum)

s = f'''Min # of turns: {int(min(bins))}
Max # of turns: {int(max(bins))}
Max prob = {100*max(y):.2f}% @ {int(bins[:-1][y==max(y)])} turns

Cum. Prob:
{int(100*perc[0])}th percentile: {int(x[cum_sum==perc[0]][0])} turns
{int(100*perc[1])}th percentile: {int(x[cum_sum==perc[1]][0])} turns
{int(100*perc[2])}th percentile: {int(x[cum_sum==perc[2]][0])} turns
{int(100*perc[3])}th percentile: {int(x[cum_sum==perc[3]][0])} turns
{int(100*perc[4])}th percentile: {int(x[cum_sum==perc[4]][0])} turns
{int(100*perc[5])}th percentile: {int(x[cum_sum==perc[5]][0])} turns
'''

ax1.text(100, 0.02, s, fontsize=24)

plt.show()

# plt.savefig(f'{num_players}_{N}_mod')
