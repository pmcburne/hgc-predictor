from team import Team
import random
import elo

#Global fields
SIMULATIONS = 10000      #Number of simulations - 10^5 minimum recommended
INPUT_FILE = 'data/naClash.csv' #data source for match records - this may be deprecated in the future
GAMES_FILE = 'data/games.csv' #games file that records previous games
STARTING_ELO_FILE = 'data/elo.csv'
PRINT_OUTCOMES = False; #Debugging - trust me, leave this false.
GET_TOP_N = 3;
REVERSE_PERCENTAGES = False; #Used for Crucible in phase 2
CALCULATE_ELO = True;
JUST_GET_ELO = False;
PRINT_SUDDEN_DEATHS = True;

ALL_TEAMS = ['R2','GF','TS','NV','ED','SS','NT','TF',
             'TL','FN','DG','PD','TR','TX','ZE','GG',
             'MB','L5','TP','MI','MM','RR','TB','RV',
             'ES','SP','WK','CE','SO','HL','RP','KT',
             'OC','TW','LA','SE'];


ALL_TEAMS_DICT = {'R2':'Roll20 Esports','GF':'Gale Force Esports','TS':'Tempo Storm','NV':'Team Naventic',
                  'ED':'Even in Death-NEW','SS':'Superstars','NT':'No Tomorrow','TF':'Team Freedom',

                  'TL':'Team Liquid','FN':'Fnatic','DG':'Team Dignitas','PD':'Playing Ducks',
                  'TR':'Tricked Esports','TX':'Team Expert','GG':'Team Good Guys-NEW','ZE':'Zealots-NEW',
                  'MB':'MVP Black','L5':'L-5','TP':'Tempest','MI':'Mighty',
                  'MM':'MVP Miracle','RR':'Rrr-NEW','TB':'Team Blossom','RV':'Raven',
                  'ES':'E-star','SP':'SuperPerfectTeam', 'KT':'Kudos Top-NEW',
                  'CE':'ce', 'SO': 'Start Over Again','HL':'Hots Lady','RP':'RPG','WK':"W.K. Gaming-NEW",
                  'OC':'Oceania','TW':'Taiwan','LA':'Latin America','SE':'Southeast Asia'};

sudden_deaths = {};

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
            teams[i['team2']].add_loss(teams[i['team1']],i['team2wins'])
        elif i['win%'] == 0:
            teams[i['team2']].add_win(teams[i['team1']],i['team1wins'])
            teams[i['team1']].add_loss(teams[i['team2']],i['team1wins'])
            
    return teams;

def get_elo_team_dictionary():
    d = {}
    for i in ALL_TEAMS:
        d[i] = Team(i)
    return d

def get_team_elo(starting_elo_file, games_filename):
    team_dictionary = get_elo_team_dictionary()
    if starting_elo_file != None:
        elo_file = open(starting_elo_file, 'r')
        for line in elo_file:
            ls = line.split(',');
            team_dictionary[ls[0]].elo = int(ls[1]);
        elo_file.close();
    if games_filename != None:
        games_file = open(games_filename, 'r')
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
            teams[i['team2']].add_loss(teams[i['team1']],i['team2wins'])
        elif i['win%'] == 0:
            teams[i['team2']].add_win(teams[i['team1']],i['team1wins'])
            teams[i['team1']].add_loss(teams[i['team2']],i['team1wins'])
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
                teams[i['team2']].add_loss(teams[i['team1']],team2_wins)
            else:
                teams[i['team2']].add_win(teams[i['team1']],team1_wins) #not ideal. Look for long term better solution
                teams[i['team1']].add_loss(teams[i['team2']],team1_wins)
            
    return teams;

def get_top_1(teams_by_wins):
    teams_by_wins = sorted(teams_by_wins, key=lambda x: x.wins, reverse=True);
    if (len(teams_by_wins) == 1):
        return teams_by_wins[0];
    elif (teams_by_wins[0].wins > teams_by_wins[1].wins):
        return teams_by_wins[0];
    else: #get tied teams
        tied_teams = [];
        target_wins = teams_by_wins[0].wins
        for i in teams_by_wins:
            if i.wins == target_wins:
                tied_teams.append(i);
        ans = head_to_head_tiebreaker(tied_teams);
        if (len(ans) == 1):
            return ans[0];
        elif (len(ans) == 0):
            return None;

def get_top_n(prediction,n): #this function will be renamed to get_top_n and will take in an n arugment.
    #this is so I can focus on crucible in stage 6.
    #n = 0 crashes this. Not going to fix that.
    teams_by_wins = [];
    out = [];
    for i in prediction:
        teams_by_wins.append(prediction[i])

    while (n > 0) :
        next_team_up = get_top_1(teams_by_wins);
        if (next_team_up == None):
            return out;
        out.append(next_team_up);
        n = n - 1;
        found = False;
        toRemove = None;
        for i in teams_by_wins:
            if i.name == next_team_up.name:
                toRemove = i;
                found = True;
        if not found:
            print(next_team_up.name + " not found")
        else:
            teams_by_wins.remove(toRemove);

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

def head_to_head_tiebreaker(tied_teams):
    #print(tied_teams, max_teams_allowed)
    #Take in a list of teams, find how they did against each other, striate them based
    #on this internal head-to-head, and advance those with the best record.

    #tied_teams - set of teams in the tie
    max_teams_allowed = 1;
    tied_losses = {}

    #get head-to-head results
    for i in tied_teams:
        tied_losses[i] = 0
        for j in tied_teams:
            tied_losses[i] += i.lost.count(j)
    teams_by_losses = []

    #create list for each # of wins possible that is empty
    for i in range(0,15):#max 14 wins per phase
        teams_by_losses.append([]);

    #append each team to the number of losses they have
    for i in tied_losses:
        teams_by_losses[tied_losses[i]].append(i)

    if len(tied_teams) == 2:
        if len(teams_by_losses[0]) == 1:
            return [teams_by_losses[0][0]];
        else:
            return get_further_tiebreaker(tied_teams);

    elif len(tied_teams) == 3:
        if len(teams_by_losses[0]) == 1:
            return [teams_by_losses[0][0]];
        else :
            return get_further_tiebreaker(tied_teams);
    else:
        if len(teams_by_losses[0]) == 1:
            return [teams_by_losses[0][0]];
        else :
            for i in teams_by_losses:
                if len(i) == 0:
                    continue;
                elif len(i) == 1:
                    return [i[0]];
                else: #cannot resolve head-to-head
                    break;
            return get_further_tiebreaker(tied_teams);
    
def get_further_tiebreaker(teams_list):
    max_teams_allowed = 1;
    #sort by win_margin_count in reverse order
    #This is, in effect, a radix sort
    teams_list = sorted(teams_list, key=lambda x: x.win_margin_count[2], reverse=True)
    teams_list = sorted(teams_list, key=lambda x: x.win_margin_count[1], reverse=True)
    teams_list = sorted(teams_list, key=lambda x: x.win_margin_count[0], reverse=True)
    teams_list = sorted(teams_list, key=lambda x: x.win_margin_count[0], reverse=True)
    teams_list = sorted(teams_list, key=lambda x: x.map_wins - x.map_losses, reverse=True)
    ##Sudden Death check
    ##Returns 1 less team as a kludgy as fuck way of signalling this will result in sudden death
    ##Since the two teams are not distinguishable by any tiebreaker metric
    team1_win_diff = teams_list[max_teams_allowed-1].map_wins - teams_list[max_teams_allowed-1].map_losses;
    team2_win_diff = teams_list[max_teams_allowed].map_wins - teams_list[max_teams_allowed].map_losses;
    if team1_win_diff == team2_win_diff and teams_list[max_teams_allowed-1].win_margin_count == teams_list[max_teams_allowed].win_margin_count:
        if PRINT_SUDDEN_DEATHS:
            abbr_set = [];
            for i in teams_list :
                if team1_win_diff == i.map_wins - i.map_losses and teams_list[max_teams_allowed-1].win_margin_count == i.win_margin_count:
                    abbr_set.append(i.name);
            abbr_set = sorted(abbr_set);
            abbrString = "";
            for i in abbr_set:
                abbrString += i+ ",";
            if abbrString not in sudden_deaths:
                print(teams_list);
                sudden_deaths[abbrString] = 1;
            else:
                sudden_deaths[abbrString] += 1;
                
        return teams_list[:max_teams_allowed-1];
    else: #Tie is broken
        return teams_list[:max_teams_allowed];
                          
def get_team_dictionary(team_file_list, elo_scores):
    team_names = set()
    teams={}
    #Set up Team set
    for i in team_file_list[:12]:#assumes all 8 teams appear in first 12 games. This number can be increased
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
    elo_scores = get_team_elo(STARTING_ELO_FILE,GAMES_FILE)
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
    elo_scores = get_team_elo(STARTING_ELO_FILE,GAMES_FILE)
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
    get_week("NT","NV","R2","TF","TS","R2","ED","GF","ED","NT","SS","NV");
    get_week("TR","GG","DG","PD","FN","DG","ZE","TL","ZE","TR","TX","GG");
    get_week("MB","TP","MM","L5","RV","L5","MI","TB","RR","RV","MB","MM");

def main():
    team_file_list = read_team_file(INPUT_FILE)
    elo_scores = {}
    if CALCULATE_ELO:
        elo_scores = get_team_elo(STARTING_ELO_FILE, GAMES_FILE)
    else:
        elo_scores = get_elo_team_dictionary()
    if JUST_GET_ELO:
        teams_and_elos = []
        for i in elo_scores:
            teams_and_elos.append([i,round(elo_scores[i].elo)])
        teams_and_elos = sorted(teams_and_elos, key=lambda x: x[1], reverse=True);
        rank = 1
        for i in teams_and_elos:
            if "RETIRED" in ALL_TEAMS_DICT[i[0]]:
                pass
            else:
                print(rank, '\t', ALL_TEAMS_DICT[i[0]],'\t',i[1])
                rank += 1;
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
            d[j.name] += 1;
    print("Sudden Death chance", round(100*(sudden_death_count/SIMULATIONS),5),"%")
    for i in d: #turn them into percentages rather than raw counts
        #with 1 decimal place '.2%f' is fo suckas
        d[i] = round((100*d[i]/SIMULATIONS),5);
        if REVERSE_PERCENTAGES:
            d[i] = round(100-d[i],5)
    #convert dictionary to list for sexy printing power
    dlist=[]
    for i in d: #add to list the team name and the percentage appearance int
        dlist.append([i, d[i]]);
    dlist = sorted(dlist, key=lambda x: x[1], reverse=True);#sort descending by percentage
    rank = 1;
    for i in dlist:
        print(rank, '\t', ALL_TEAMS_DICT[i[0]], '\t', i[1],'%')
        rank += 1
    for i in sudden_deaths:
        print(i + " - " + str(round((sudden_deaths[i])/SIMULATIONS,5)*100) + "%");
    

if __name__=="__main__":
    main();
