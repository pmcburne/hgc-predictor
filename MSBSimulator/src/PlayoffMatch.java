
public class PlayoffMatch {
	int id;
	Team home;
	Team away;
	Team winner,loser;
	
	int winnerGoesTo, loserGoesTo;
	int winsRequired;
	
	boolean bo5;
	int homeWins, awayWins;
	
	public PlayoffMatch(int id, Team home, Team away, 
			int winnerGoesTo, int loserGoesTo, 
			boolean bo5){
		this.winner = null;
		this.loser = null;
		this.id = id;
		this.home = home;
		this.away = away;
		this.winnerGoesTo = winnerGoesTo;
		this.loserGoesTo = loserGoesTo;
		this.bo5 = bo5;
		this.awayWins = 0;
		if (bo5){
			this.homeWins = 0;
			this.winsRequired = 3;
		} else {
			this.homeWins = 1;
			this.winsRequired = 4;
		}
	}
	
	private void simulateMatch() {
		double we = homeWinExpected();
		while (homeWins < winsRequired && awayWins < winsRequired) {
			if (Math.random() < we) {
				homeWins++;
			} else {
				awayWins++;
			}
		}
		if (homeWins > awayWins) {
			winner = home;
			loser = away;
		} else {
			winner = away;
			loser = home;
		}
	}
	
	public void addTeam(Team toAdd) {
		if (home == null) {
			home = toAdd;
		} else if (away == null) {
			away = toAdd;
		} else {
			throw new IllegalStateException("ERROR: added team to full game");
		}
	}

	public Team getWinner() {
		if (winner == null) {
			simulateMatch();
		}
		return winner;
	}
	
	public Team getLoser() {
		if (winner == null) {
			simulateMatch();
		}
		return loser;
	}
	
	private double homeWinExpected() {
		int homeElo = home.elo;
		int awayElo = away.elo;
		
		int dr = awayElo - homeElo;
		
		double denominator = Math.pow(10, (dr/400.0)) + 1;
		
		return 1 / denominator;
	}
}
