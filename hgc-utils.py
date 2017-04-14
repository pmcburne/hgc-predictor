from team import Team
import random
import elo

#Global fields
SIMULATIONS = 100000      #Number of simulations - 10^5 minimum recommended
INPUT_FILE = 'data/na.csv' #data source for match records - this may be deprecated in the future
GAMES_FILE = 'data/games.csv' #games file that records previous games
PRINT_OUTCOMES = False; #Debugging - trust me, leave this false.
GET_TOP_N = 1;
REVERSE_PERCENTAGES = False; #Used for Crucible in phase 2
CALCULATE_ELO = True;
JUST_GET_ELO = False;

ALL_TEAMS = ['T8','GF','TS','NV','BS','SS','NT','TF',
             'TL','FN','DG','PD','TR','TX','SN','BG',
             'MB','L5','TP','MI','MM','GG','TB','RV',
             'ES','SP','ZP','XT','CE','SO','HL','RP','KS',
             'OC','TW','LA','SE'];

ALL_TEAMS_DICT = {'T8':'Team 8','GF':'Gale Force eSports','TS':'Tempo Storm','NV':'Team Naventic',
                  'BS':'B-Step','SS':'Superstars','NT':'No Tomorrow','TF':'Team Freedom',
                  'TL':'Team Liquid','FN':'Fnatic','DG':'Team Dignitas','PD':'Playing Ducks',
                  'TR':'Tricked eSports','TX':'Team Expert','SN':'Synergy','BG':'beGenius',
                  'MB':'MVP Black','L5':'L-5','TP':'Tempest','MI':'Mighty',
                  'MM':'MVP Miracle','GG':'GG','TB':'Team Blossom','RV':'Raven',
                  'ES':'E-star','SP':'SuperPerfectTeam','ZP':'Zero Panda--RETIRED', 'XT':'X-Team',
                  'CE':'ce', 'SO': 'Start Over Again','HL':'Hots Lady--NEW','RP':'RPG--NEW','KS':"Keep It Simple--NEW",
                  'OC':'Ocenia','TW':'Taiwan','LA':'Latin America','SE':'Southeast Asia'};

def read_team_file(filename):
    """reads in team file with win probability"""
    out=[]
    try:
        infile = open(filename, 'r')
    except FileNotFoundError:
        print("File not found. Empty list returned");
        return [];  
    for line in infile:
        split = line.strip().split(',')
        if len(split) != 5:
            print("Bad line found. Skipping:", line)
            continue
        toAdd = {}
        toAdd['team1'] = split[0]
        toAdd['team2'] = split[1]
        toAdd['win%'] = float(split[2])
        if split[3].isnumeric() and split[4].isnumeric():
            toAdd['team1wins'] = int(split[3])
            toAdd['team2wins'] = int(split[4])        
        out.append(toAdd)
    return out;

def get_current_state(team_filename): #pretty sure this is depricated
    team_names = set()
    teams={}
    #This for loop assumes every team will appear once in the first
    #four games. If that changes, this must be changed
    team_file = read_team_file(team_filename)
    for i in team_file[:10]:
        team_names.add(i['team1'])
        team_names.add(i['team2'])
    for i in team_names:
        teams[i] = Team(i)
    for i in team_file:
        if i['win%'] == 1:
            teams[i['team1']].add_win(teams[i['team2']],i['team2wins'])
            teams[i['team2']].add_loss(teams[i['team1']])
        elif i['win%'] == 0:
            teams[i['team2']].add_win(teams[i['team1']],i['team1wins'])
            teams[i['team1']].add_loss(teams[i['team2']])
            
    return teams;

def get_elo_team_dictionary():
    d = {}
    for i in ALL_TEAMS:
        d[i] = Team(i)
    return d

def get_team_elo(games_filename):
    games_file = open(games_filename, 'r')
    team_dictionary = get_elo_team_dictionary()
    for line in games_file:
        if len(line) == 0 or line.startswith('#'):#skip commented lines
            continue
        ls = line.split(',');
        #parse line
        this_team = ls[0]
        that_team = ls[1]
        winner = ls[2]
        match_type = ls[3]
        if winner == this_team:
            this_win = True;
        elif winner == that_team:
            this_win = False;
        else:
            raise ValueError("winner doesn't match either input team: " + str(ls))
        try:
            this_team = team_dictionary[this_team]
            that_team = team_dictionary[that_team]
            elo.process_game(this_team, that_team, this_win, match_type);
        except KeyError:
            print(this_team, 'not found');
            pass;
    games_file.close()
    #for i in team_dictionary:
     #   print(i, team_dictionary[i].elo);
    return team_dictionary

def elo_odds(team1, team2):
    return elo.get_expected(team1.elo, team2.elo);

def get_prediction(team_file, elo_scores):
    teams = get_team_dictionary(team_file, elo_scores)
    '''generates a random simulation from a team file, while not changing decided games'''
    for i in team_file:
        #generate random number. If less then player 1 win percentage, player 1 wins
        #This is why decided games have percentages 0 and 1
        if i['win%'] == 1:
            teams[i['team1']].add_win(teams[i['team2']],i['team2wins'])
            teams[i['team2']].add_loss(teams[i['team1']])
        elif i['win%'] == 0:
            teams[i['team2']].add_win(teams[i['team1']],i['team1wins'])
            teams[i['team1']].add_loss(teams[i['team2']])
        else: #Simulate
            team1_wins = 0
            team2_wins = 0
            odds = elo_odds(teams[i['team1']],teams[i['team2']])
            while team1_wins < 3 and team2_wins < 3:
                if odds > random.random():
                    team1_wins += 1
                else:
                    team2_wins += 1
            if team1_wins == 3:
                teams[i['team1']].add_win(teams[i['team2']],team2_wins) #not ideal. Look for long term better solution
                teams[i['team2']].add_loss(teams[i['team1']])
            else:
                teams[i['team2']].add_win(teams[i['team1']],team1_wins) #not ideal. Look for long term better solution
                teams[i['team1']].add_loss(teams[i['team2']])
            
    return teams;

def get_top_n(prediction,n): #this function will be renamed to get_top_n and will take in an n arugment.
    #this is so I can focus on crucible in stage 6.
    #n = 0 crashes this. Not going to fix that.
    '''Prediction is a team dictionary'''
    teams_by_wins = []
    out = []
    for i in prediction:
        teams_by_wins.append(prediction[i])
    #get sorted list of teams
    teams_by_wins = sorted(teams_by_wins, key=lambda x: x.wins, reverse=True);
    if teams_by_wins[n-1].wins > teams_by_wins[n].wins:
        lst = teams_by_wins[0:n]
        for i in lst:
            out.append(i.name);
        return out
    else:#tiebreaker
        # this approach is incredibly fucking kludgy, and likely should be rewritten
        # specifically in phase 2, when we are talking about crucible, so top 6 (to isolate bottom 2)
        # instead of top 3. I should rewrite this using a loop. No clue why I thought writing it this way was
        # a good idea
        i = n
        while (i>0):
            if teams_by_wins[i-1].wins > teams_by_wins[i].wins:
                lst = teams_by_wins[0:i]
                for j in lst:
                    out.append(j.name);
                for j in get_tie_breaker_teams(teams_by_wins,i,n):
                    out.append(j.name);
                return out;
            i -= 1
        for i in get_tie_breaker_teams(teams_by_wins,0,n):
            out.append(i.name);
        return out;
            
def get_tie_breaker_teams(teams_by_wins, num_teams_above_tie,max_allowed):
    '''assume team by wins sorted as precondition. Get list of teams in tiebreaker'''
    win_mark = teams_by_wins[num_teams_above_tie].wins;
    tied_teams = set()
    for i in teams_by_wins:
        #teams with same number of wins as third place involved in tie breaker.
        if i.wins == win_mark:
            tied_teams.add(i);
    return head_to_head_tiebreaker(tied_teams, max_allowed - num_teams_above_tie)

def head_to_head_tiebreaker(tied_teams, max_teams_allowed):
    #print(tied_teams, max_teams_allowed)
    #Take in a list of teams, find how they did against each other, striate them based
    #on this internal head-to-head, and advance those with the best record.

    #tied_teams - set of teams in the tie
    tied_wins = {}

    #get head-to-head results
    for i in tied_teams:
        tied_wins[i] = 0
        for j in tied_teams:
            tied_wins[i] += i.beat.count(j)
    teams_by_wins = []

    #create list for each # of wins possible that is empty
    for i in range(0,15):#max 14 wins per phase
        teams_by_wins.append([]);

    #append each team to the number of wins they have
    for i in tied_wins:
        teams_by_wins[tied_wins[i]].append(i)
    teams_by_wins.reverse()
    #output list
    out = []
    for i in teams_by_wins:
        if len(i) > 0 and len(i) <= max_teams_allowed:
            max_teams_allowed -= len(i)
            for j in i:
                out.append(j)
                #tied_teams.remove(j) #this apparently doesn't work for....reasons?
                for k in tied_teams:
                    if k.name == j.name:
                        tied_teams.remove(k);
                        break;
            #TODO - recall head to head with teams in out removed. **needed bug fix**
            #if no more spots left, break, this prevents side effects
            if max_teams_allowed == 0:
                return out;
            return out + head_to_head_tiebreaker(tied_teams, max_teams_allowed);
        #If further tiebreaking is needed
        elif len(i) > 0 and len(i) > max_teams_allowed:
            further = get_further_tiebreaker(i,max_teams_allowed)
            return out + further;
    
def get_further_tiebreaker(teams_list,max_teams_allowed):
    #sort by win_margin_count in reverse order
    #This is, in effect, a radix sort
    teams_list = sorted(teams_list, key=lambda x: x.win_margin_count[2], reverse=True)
    teams_list = sorted(teams_list, key=lambda x: x.win_margin_count[1], reverse=True)
    teams_list = sorted(teams_list, key=lambda x: x.win_margin_count[0], reverse=True)
    ##Sudden Death check
    ##Returns 1 less team as a kludgy as fuck way of signalling this will result in sudden death
    ##Since the two teams are not distinguishable by any tiebreaker metric
    if teams_list[max_teams_allowed-1].win_margin_count == teams_list[max_teams_allowed].win_margin_count:
        return teams_list[:max_teams_allowed-1];
    else: #Tie is broken
        return teams_list[:max_teams_allowed];
                          
def get_team_dictionary(team_file_list, elo_scores):
    team_names = set()
    teams={}
    #Set up Team set
    for i in team_file_list[:6]:#assumes all 8 teams appear in first 4 games. This number can be increased
                           #to accomodate more games without negative side effects
        team_names.add(i['team1'])
        team_names.add(i['team2'])
    #translate Team set to team dictionary    
    for i in team_names:#add teams to dictionary keyed by their name
        teams[i] = Team(i)
        teams[i].elo = elo_scores[i]
    return teams;

def get_binomial_win_percentage_three_wins(p,n):
    if n == 0:
        return p * p * p #3-0
    elif n == 1:
        return 3 * p * p * p * (1-p) #3-1
    #3-2 possibilities - HHTTT, HTHTT, HTTHT,
    #3-2 possibilities - THHTT, THTHT, TTHHT
    elif n == 2:
        return 6 * p * p * p * (1-p) * (1-p)
    return None

def get_binomial_win_percentage_two_wins(p,n):
    if n == 0:
        return p * p
    elif n == 1:
        return 2 * p * p * (1-p)
    return None

def get_week_bo3(*team_names):
    elo_scores = get_team_elo(GAMES_FILE)
    print('Team 1 | 2-0 | 2-1 | 1-2 | 0-2 | Team 2')
    print('----|---|---|---|---|---|---|----')
    for i in range (0, int(len(team_names)/2)):
        per_game = elo.get_expected(elo_scores[team_names[2*i]],
                                           elo_scores[team_names[2*i+1]])
        team1_win = get_binomial_win_percentage_two_wins(per_game,0) + \
                    get_binomial_win_percentage_two_wins(per_game,1)
        team2_win = get_binomial_win_percentage_two_wins(1-per_game,0) + \
                    get_binomial_win_percentage_two_wins(1-per_game,1)
        print(ALL_TEAMS_DICT[team_names[2*i]],'-',round(100*team1_win,2),'% |' ,
              round(100*get_binomial_win_percentage_two_wins(per_game,0),2),' | ',
              round(100*get_binomial_win_percentage_two_wins(per_game,1),2),' | ',
              round(100*get_binomial_win_percentage_two_wins(1-per_game,1),2),' | ',
              round(100*get_binomial_win_percentage_two_wins(1-per_game,0),2),' | ',
              round(100*team2_win,2),'% -',ALL_TEAMS_DICT[team_names[2*i+1]])

def get_week(*team_names):
    elo_scores = get_team_elo(GAMES_FILE)
    print('Team 1 | 3-0 | 3-1 | 3-2 | 2-3 | 1-3 | 0-3 | Team 2')
    print('----|---|---|---|---|---|---|----')
    for i in range (0, int(len(team_names)/2)):
        per_game = elo.get_expected(elo_scores[team_names[2*i]],
                                           elo_scores[team_names[2*i+1]])
        team1_win = get_binomial_win_percentage_three_wins(per_game,0) + \
                    get_binomial_win_percentage_three_wins(per_game,1) + \
                    get_binomial_win_percentage_three_wins(per_game,2)
        team2_win = get_binomial_win_percentage_three_wins(1-per_game,0) + \
                    get_binomial_win_percentage_three_wins(1-per_game,1) + \
                    get_binomial_win_percentage_three_wins(1-per_game,2)
        print(ALL_TEAMS_DICT[team_names[2*i]],'-',round(100*team1_win,2),'% |' ,
              round(100*get_binomial_win_percentage_three_wins(per_game,0),2),' | ',
              round(100*get_binomial_win_percentage_three_wins(per_game,1),2),' | ',
              round(100*get_binomial_win_percentage_three_wins(per_game,2),2),' | ',
              round(100*get_binomial_win_percentage_three_wins(1-per_game,2),2),' | ',
              round(100*get_binomial_win_percentage_three_wins(1-per_game,1),2),' | ',
              round(100*get_binomial_win_percentage_three_wins(1-per_game,0),2),' | ',
              round(100*team2_win,2),'% -',ALL_TEAMS_DICT[team_names[2*i+1]])


def this_week():
    #get_week('GF','T8','NV','BS','TF','SS','NT','TS','NT','NV','T8','TS')
    #get_week('FN','TX','TL','TR','SN','BG','PD','DG','PD','TL','TX','DG')
    #get_week('TP','MB','TB','MM','RV','GG','MI','L5','GG','L5','TB','TP');
    get_week('XT','HL','ES','RP','SP','CE','KS','SO')

def main():
    team_file_list = read_team_file(INPUT_FILE)
    elo_scores = {}
    if CALCULATE_ELO:
        elo_scores = get_team_elo(GAMES_FILE)
    else:
        elo_scores = get_elo_team_dictionary()
    if JUST_GET_ELO:
        teams_and_elos = []
        for i in elo_scores:
            teams_and_elos.append([i,round(elo_scores[i].elo)])
        teams_and_elos = sorted(teams_and_elos, key=lambda x: x[1], reverse=True);
        for i in teams_and_elos:
            print(ALL_TEAMS_DICT[i[0]],'|',i[1])
        return
    results = []
    for i in range(0,SIMULATIONS):
        #run simulation
        prediction = get_prediction(team_file_list, elo_scores)
        ##Top 3 - need to make general
        results.append(get_top_n(prediction,GET_TOP_N))
        #if len(results[i]) == 2:
            #print(results[i]);
    sudden_death_count = 0;
    d = {}
    #Add teams to dictionary
    for i in prediction:#add teams to dictionary
        d[i] = 0        
    for i in results:
        if PRINT_OUTCOMES:
            print(i)
        if len(i) < GET_TOP_N: #assumes top 3. Need to make general
            sudden_death_count += 1
        for j in i: #count number of times each team in D appears in top results
            d[j] += 1;
    print("Sudden Death chance", round(100*(sudden_death_count/SIMULATIONS),2),"%")
    for i in d: #turn them into percentages rather than raw counts
        #with 1 decimal place '.2%f' is fo suckas
        d[i] = round((100*d[i]/SIMULATIONS),1);
        if REVERSE_PERCENTAGES:
            d[i] = round(100-d[i],1)
    #convert dictionary to list for sexy printing power
    dlist=[]
    for i in d: #add to list the team name and the percentage appearance int
        dlist.append([i, d[i]]);
    dlist = sorted(dlist, key=lambda x: x[1], reverse=True);#sort descending by percentage
    rank = 1;
    for i in dlist:
        print(rank, '|', ALL_TEAMS_DICT[i[0]], '|', i[1],'%')
        rank += 1
    

if __name__=="__main__":
    main();
