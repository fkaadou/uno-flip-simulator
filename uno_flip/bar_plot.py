#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 18:56:22 2022

@author: fouad
"""

import matplotlib.pyplot as plt
import numpy as np
from funx import percentile

prog = '''count%s = np.loadtxt('uno_flip_house_%s_players')'''

for i in range(2, 7):
    exec(prog % (i,i))
    

all_counts = np.array([count2, count3, count4, count5, count6])

#######################################################################

# all_counts = all_counts[::-1]

fig, axs = plt.subplots(figsize=(10,8))

for i, count in enumerate(all_counts):
           
    y, bins, patches = plt.hist(x=count, bins=int(max(count)-min(count)), density=True, 
                                stacked=True, label=f'{i+2} players', alpha=1)

plt.xlabel('Number of Rounds', fontsize=28)
plt.ylabel('Probability', fontsize=28)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.xlim(0,150)
plt.ylim(0, 0.12)
plt.legend(fontsize=22)
plt.show()
    
# plt.savefig('tex/figs/uno_flip_house_overlay')

############################################################################

for i, count in enumerate(all_counts):
    
    fig, ax1 = plt.subplots(figsize=(12,8))
        
    y, bins, patches = plt.hist(x=count, bins=int(max(count)-min(count)), density=True, stacked=True)
    plt.xlabel('Number of Rounds', fontsize=28)
    plt.ylabel('Probability', fontsize=28)
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    plt.xlim(0,150)
    plt.ylim(0,0.12)
    
    cum_sum = np.array([sum(y[:i+1]) for i in range(len(y))])
    
    if 'flip' not in prog:
        x = np.concatenate(([0,1,2,3,4,5,6,7], bins[:-1]))
        cum_sum = np.concatenate(([0,0,0,0,0,0,0,0], cum_sum))
    else:
        x = np.concatenate(([0,1,2,3], bins[:-1]))
        cum_sum = np.concatenate(([0,0,0,0], cum_sum))
    
    ax2 = ax1.twinx()
    ax2.plot(x, cum_sum, lw=3, color='tab:orange')
    ax2.set_ylabel('Cumulative Probability', fontsize=22,  rotation=270)
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
    
    print('***********************************************')
    print(f'Number of players {i+2}')
    print(s)

    plt.show()

    # plt.savefig(f'tex/figs/uno_flip_house_{i+2}')
