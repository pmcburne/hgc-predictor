import java.util.HashMap;
import java.util.Map;

public class ChinaMassSimulator {
	private final int NUMBER_OF_SIMULATIONS = 100000;

	Map<String, Integer> winnersBracketCounts, losersBracketCounts, eliminatedCounts;

	String teamsFileName, gamesFileName;

	public ChinaMassSimulator(String teamsFileName, String gamesFileName) {
		this.teamsFileName = teamsFileName;
		this.gamesFileName = gamesFileName;
		winnersBracketCounts = new HashMap<String, Integer>();
		eliminatedCounts = new HashMap<String, Integer>();
	}

	public void simulate() {
		// one simulation to setup conditions
		for (int i = 0; i < NUMBER_OF_SIMULATIONS; i++) {
			ChinaGroupSimulator gs = new ChinaGroupSimulator(teamsFileName, gamesFileName);
			gs.simulate();

			for (Team t : gs.getTopThree()) {
				try {
					int prevCount = winnersBracketCounts.get(t.abbrv);
					winnersBracketCounts.put(t.abbrv, prevCount + 1);
				} catch (NullPointerException e) {
					winnersBracketCounts.put(t.abbrv, 1);
				}
			}


			for (Team t : gs.getLastTwo()) {
				try {
					int prevCount = eliminatedCounts.get(t.abbrv);
					eliminatedCounts.put(t.abbrv, prevCount + 1);
				} catch (NullPointerException e) {
					eliminatedCounts.put(t.abbrv, 1);
				}
			}
		}
	}
	
	public void printResults() {
		System.out.println("===== Eastern Clash =====");
		for (String s : winnersBracketCounts.keySet()) {
			System.out.printf((s + " - %.3f\n"), winnersBracketCounts.get(s)/1000.0);
		}
		System.out.println("\n===== Relegated ==========");
		for (String s : eliminatedCounts.keySet()) {
			System.out.printf((s + " - %.3f\n"), eliminatedCounts.get(s)/1000.0);
		}
	}

	public static void main(String[] args) {
		ChinaMassSimulator mgs = new ChinaMassSimulator("data/cnTeams.csv", "data/cn.csv");
		mgs.simulate();

		mgs.printResults();
	}
}
