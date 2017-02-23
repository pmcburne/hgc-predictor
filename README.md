# hgc-predictor

Very quick hack

Run hgc-utils.py in Python 3 to see results.

To change source file, open hgc-utils.py and change the line:

======================GLOBAL PARAMETERS==============================

SIMULATIONS = 100000 - Number of simulations, defaults to 100K

----------------------------------------------------------------------

INPUT_FILE = 'data/na.csv' or 'data/eu.csv' or 'data/kr.csv' (cn.csv still coming) #the input file you want to use to predict games

Input File format should be 5 column CSV, seen here:

https://docs.google.com/spreadsheets/d/1i9MIr_W094s2wehf-vh3Y6of5A8gstR7C9CSkFLG3Cg/edit?usp=sharing

Go to a 50/50 page to see the relevant format

For games already completed, win chance (column 3) should be 1 or 0 (1 if Column 1 wins, 0 if column 2 wins). 0.5 if not completed 
Additionally, column 4 and 5 should have the number of map wins from each set. Leave 4 and 5 blank if you plan to
simulate randomly.

Ignore naAdjusted, euAdjusted, etc. The new elo system makes those files obsolete.

----------------------------------------------------------------------

GAMES_FILES = 'data/games.csv' - this file is used to calculate elo and conglamerates all games (not matches) from all regions. Should include all completed games for mos accurate results. See games tab in https://docs.google.com/spreadsheets/d/1i9MIr_W094s2wehf-vh3Y6of5A8gstR7C9CSkFLG3Cg/edit?usp=sharing for details.

----------------------------------------------------------------------

PRINT_OUTCOMES = False; - leave this one false. This is for debugging, as it prints the outcome of each simulation. But since there are 100000 simulations by default, it's a lot.

----------------------------------------------------------------------

GET_TOP_N = 1; - get top N teams. Set to 3 for clashes, 6 for Crucibles, 1 for top 1 for Brawls.

----------------------------------------------------------------------

REVERSE_PERCENTAGES = False; - for Crucible, it's useful to find percentage they are in the bottom 2 rather than the top 6. This "reverses" all percentages with pct = 100 - p. Basically odds of being BELOW top N rather than in top n

----------------------------------------------------------------------

CALCULATE_ELO = True; - Used for adjusted prediction. If this is true, elo is calculated and used in simulations. If False, Elo is ignored and all games are 50/50.

----------------------------------------------------------------------

JUST_GET_ELO = False; - Set to true if you just want to get current Elo ratings. Does no simulation.

===========================================================================

TO-DO  
Setup user commandline arguments  

