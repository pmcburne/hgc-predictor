
public abstract class MatchSimulator {
	public abstract void simulateMatch(Team home, Team away);
	
	public static double getHomeWinExpected(Team home, Team away) {
		int homeElo = home.elo;
		int awayElo = away.elo;
		
		int dr = awayElo - homeElo;
		
		double denominator = Math.pow(10, (dr/400.0)) + 1;
		
		return 1 / denominator;
	}
}
