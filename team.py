class Team:
    def __init__(self, name):
        self.name = name;
        self.wins = 0
        self.losses = 0
        self.beat=[]
        self.lost=[]
        self.win_margin_count = [0,0,0]

    def add_win(self, team_they_beat,opp_wins):
        self.wins += 1
        self.win_margin_count[opp_wins] += 1
        self.beat.append(team_they_beat)

    def add_loss(self, team_they_lost_to):
        self.losses += 1
        self.lost.append(team_they_lost_to)

    def get_win_percentage(self):
        return wins / (wins + losses)

    def get_beat_name_list(self):
        out = ""
        for i in self.beat:
            out += i.name + ' '
        return out;

    def get_lost_name_list(self):
        out = ""
        for i in self.lost:
            out += i.name + ' '
        return out;

    def __repr__(self):
        out = self.name + " " + str(self.wins) + "-" + str(self.losses) + '\n'
        out += '\tWins against: ' + self.get_beat_name_list() + '\n'
        out += '\tLost against: ' + self.get_lost_name_list() + '\n'
        out += '\tWin Margins: ' + str(self.win_margin_count) + '\n'
        return out;

    def __str__(self):
        return self.name

def main():
    TempoStorm = Team("TS")
    TempoStorm.add_win("NV",2)
    TempoStorm.add_win("T8",1)
    TempoStorm.add_loss("GF")
    TempoStorm.add_loss("TF")
    print(TempoStorm)

if __name__=="__main__":
    main();
