#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 18:10:16 2022

@author: fouad
"""

def log_monitor(verbose):
    
    if not verbose:
        return
    
    max_MB = 1
    while True:
        if os.path.getsize('log')/1024**2 > max_MB:
            original_stdout.write(f'File larger than {max_MB}MB. Game likely stuck.')
            original_stdout.write(f'Error in game {j} of {N}\n')
            break
    sys.exit()
            


def percentile(bins, cum_sum):
    
    perc0 = [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
    perc  = [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
        
    delta = [0.00, -0.01, 0.01, -0.02, 0.02, -0.03, 0.03, -0.04, 0.04, -0.05, 0.05]
    
    for i, p in enumerate(perc0):
        for d in delta:
            try:
                int(bins[cum_sum==p+d][0])
                perc[i] = p + d
                break
            except:
                pass
            
    return perc