import java.util.Map;

public class Playoff {
	
	public Map<Integer,PlayoffMatch> matches;

	public Playoff(Map<Integer, PlayoffMatch> playoffMatches) {
		this.matches = playoffMatches;
	}
	
	public void printMatches() {
		for (int i : matches.keySet()) {
			PlayoffMatch p = matches.get(i);
			if (p.home == null) {
				System.out.println(null + " - " + null);
			} else if (p.winner == null) {
				System.out.println(p.home.abbrv + " - " + p.away.abbrv);
			} else {
				System.out.println(p.home.abbrv + " - " + p.away.abbrv + " Winner: " + p.winner.abbrv);
			}
		}
	}
	
	public void simulateMatches() {
		int max = -1;
		for (int i : matches.keySet()) {
			if (i > max) {
				max = i;
			}
		}
		
		for (int i = 1; i <= max; i++) {
			PlayoffMatch pm = matches.get(i);
			Team winner = pm.getWinner();
			Team loser = pm.getLoser();
			if (pm.winnerGoesTo != -1) {
				matches.get(pm.winnerGoesTo).addTeam(winner);
			}
			if (pm.loserGoesTo != -1) {
				matches.get(pm.loserGoesTo).addTeam(loser);
			}
		}
	}

}
