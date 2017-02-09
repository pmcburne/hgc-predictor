# hgc-predictor

Very quick hack

Run hgc-utils.py in Python 3 to see results.

To change source file, open hgc-utils.py and change the line:

INPUT_FILE = 'data/naAdjusted.csv' #insert whatever file you want

Input File format should be 5 column CSV, seen here:

https://docs.google.com/spreadsheets/d/1i9MIr_W094s2wehf-vh3Y6of5A8gstR7C9CSkFLG3Cg/edit?usp=sharing

For games already completed, win chance (column 3) should be 1 or 0 (1 if Column 1 wins, 0 if column 2 wins). 
Additionally, column 4 and 5 should have the number of map wins from each set. Leave this blank if you plan to
simulate randomly.


TO-DO  
Setup user commandline arguments  
Setup "Crucible mode" where instead of top 3, we are looking for bottom 2 (or at least top 6, anyways)  
