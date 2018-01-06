
public class BestOfTwoSimulator extends MatchSimulator {
	@Override
	public void simulateMatch(Team home, Team away) {
		double winExpected = getHomeWinExpected(home, away);
		int homeWins = 0;
		int awayWins = 0;
		for (int i = 0; i < 2; i++) {
			if (Math.random() < winExpected) {
				homeWins++;
			} else {
				awayWins++;
			}
		}
		
		if (homeWins == 2&& awayWins == 0) {
			home.teamsBeat.add(away);
			home.points += 2;
			away.teamsLostTo.add(home);
		} else if (homeWins == 1 && awayWins == 1) {
			home.teamsDrawn.add(away);
			home.points++;
			away.teamsDrawn.add(home);
			away.points++;
		} else if (homeWins == 0 && awayWins == 2) {
			home.teamsLostTo.add(away);
			away.teamsBeat.add(home);
			away.points += 2;
		}
	}
}
