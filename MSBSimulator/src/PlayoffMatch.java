
public class PlayoffMatch {
	int id;
	Team home;
	Team away;
	
	PlayoffMatch winnerGoesTo, loserGoesTo;
	
	boolean bo5;
	
	public PlayoffMatch(int id, Team home, Team away, PlayoffMatch winnerGoesTo, PlayoffMatch loserGoesTo, boolean bo5){
		this.id = id;
		this.home = home;
		this.away = away;
		this.winnerGoesTo = winnerGoesTo;
		this.loserGoesTo = loserGoesTo;
		this.bo5 = bo5;
	}
}
