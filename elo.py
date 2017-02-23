#Elo rankings
from team import Team
import math

#K values
QUALIFIER = 20
REGIONAL = 35   #Region Season game - k = 30
CLASH = 40      #Western/Eastern Clash = 50
BRAWL = 50      #International Brawl = 60

#Initial Team Ranking
NEW_TEAM_RATING = 1500

# create k dictionary():
K = {}
K['q'] = QUALIFIER
K['r'] = REGIONAL;
K['c'] = CLASH
K['b'] = BRAWL

def get_expected(this_team, that_team):
    """gets the W_e value, which should be a number between 0 and .5
    this_team - return value is this_team's chance to win against that_team"""
    dr = this_team.elo - that_team.elo
    w_e = 1 / (math.pow(10, (-dr / 400)) + 1)
    return w_e;

def update_rating(this_team, that_team, expected, actual, k):
    this_team.elo = this_team.elo + k * (actual - expected);

def process_game(this_team, that_team, this_win, class_of_game):
    """Updates the elo ranking of a team based on the result of a GAME (not a match)

    this updates BOTH this_team's and that_team's elo to reflect the outcome
    of a game.

    this_team should be a team object, NOT a team name.
    same with that_team
    this_win is true if this_team won, and false if that_team won
    class_of_game should be 'qualifier' or 'q', 'regional' or 'r', etc."""
    #get expected win %
    this_expected = get_expected(this_team, that_team)
    that_expected = get_expected(that_team, this_team)

    #extract true false into 1/0 for calculation
    if this_win:
        this_win = 1
        that_win = 0
    else:
        this_win = 0
        that_win = 1
        
    #get matching k value
    k = K[class_of_game[0].lower()]

    #update ratings for both teams
    update_rating(this_team, that_team, this_expected, this_win, k);
    update_rating(that_team, this_team, that_expected, that_win, k);
    
    

def main():#testing
    this_team = Team("This")
    that_team = Team("That")
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    process_game(this_team, that_team, True, 'regional')
    process_game(that_team, this_team, True, 'regional')
    print(this_team.name,this_team.elo)
    print(that_team.name,that_team.elo)

if __name__ == "__main__":
    main()
    
