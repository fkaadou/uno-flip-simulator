# uno-flip-simulator

## Introduction

After playing (and giving up on) what seemed to be a never-ending game of UNO
flip with family and friends, I decided to write an UNO flip simulator to study how
our house rules were influencing the length of the games. After completing the UNO
flip simulator, I went ahead and repurposed the code to run regular UNO and tried our
house rules as well.

The simulators run a number of games and record how long the each game took (in rounds). The final results are aggregated to produce a probability distrubtion. The purpose of this project was to investigate how the rules and number of players influences the length of the game by studying the change in the probability distribution.

Please see the report for a full breakdown of the results.

## Notes on uno_flip

Games using the official rules are simulated in `main_official.py` for single-core processing and in `main_official_parallel.py` for faster multi-core processing.

Games using the house rules are simulated in `main_house.py` for single-core processing and in `main_house_parallel.py` for faster multi-core processing.

Please see the report for an explanation of the house rules.

## Notes on uno_original

Games using both the house and official rules are simulating the same two pieces of code, `main.py` (single-core processing) and `main_parallel.py` (multi-core processing). In order to choose which rule set to use, choose between `Player_official` and `Player_house` when creatig the `player` object. 
