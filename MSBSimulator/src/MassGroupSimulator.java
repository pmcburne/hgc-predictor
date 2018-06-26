import java.util.HashMap;
import java.util.Map;

public class MassGroupSimulator {
	private final int NUMBER_OF_SIMULATIONS = 100000;

	Map<String, Integer> winnersBracketCounts, losersBracketCounts, eliminatedCounts, teamPointTotals;

	String teamsFileName, gamesFileName;

	public MassGroupSimulator(String teamsFileName, String gamesFileName) {
		this.teamsFileName = teamsFileName;
		this.gamesFileName = gamesFileName;
		winnersBracketCounts = new HashMap<String, Integer>();
		losersBracketCounts = new HashMap<String, Integer>();
		teamPointTotals = new HashMap<String,Integer>();
		eliminatedCounts = new HashMap<String, Integer>();
	}

	public void simulate() {
		// one simulation to setup conditions
		for (int i = 0; i < NUMBER_OF_SIMULATIONS; i++) {
			GroupSimulator gs = new GroupSimulator(teamsFileName, gamesFileName);
			gs.simulate();
			
			for (String teamName : gs.teams.keySet()) {
				try {
					int prevPoints = teamPointTotals.get(teamName);
					teamPointTotals.put(teamName, gs.teams.get(teamName).points + prevPoints);
				} catch (NullPointerException e) {
					teamPointTotals.put(teamName, gs.teams.get(teamName).points);
				}
			}

			for (Team t : gs.getTopTwo()) {
				try {
					int prevCount = winnersBracketCounts.get(t.abbrv);
					winnersBracketCounts.put(t.abbrv, prevCount + 1);
				} catch (NullPointerException e) {
					winnersBracketCounts.put(t.abbrv, 1);
				}
			}

			for (Team t : gs.getNextTwo()) {
				try {
					int prevCount = losersBracketCounts.get(t.abbrv);
					losersBracketCounts.put(t.abbrv, prevCount + 1);
				} catch (NullPointerException e) {
					losersBracketCounts.put(t.abbrv, 1);
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
		System.out.println("===== Average Points =====");
		for (String s : teamPointTotals.keySet()) {
			System.out.printf((s + " - %.1f\n"), teamPointTotals.get(s)/100000.0);
		}
		System.out.println("===== Winners Bracket =====");
		for (String s : winnersBracketCounts.keySet()) {
			System.out.printf((s + " - %.1f\n"), winnersBracketCounts.get(s)/1000.0);
		}
		System.out.println("\n===== Losers Bracket ======");
		for (String s : losersBracketCounts.keySet()) {
			System.out.printf((s + " - %.1f\n"), losersBracketCounts.get(s)/1000.0);
		}
		System.out.println("\n===== Eliminated ==========");
		for (String s : eliminatedCounts.keySet()) {
			System.out.printf((s + " - %.1f\n"), eliminatedCounts.get(s)/1000.0);
		}
	}

	public static void main(String[] args) {
		MassGroupSimulator mgs = new MassGroupSimulator("data/teams.csv", "data/group1.csv");
		mgs.simulate();

		mgs.printResults();
		
		mgs = new MassGroupSimulator("data/teams.csv", "data/group2.csv");
		mgs.simulate();

		mgs.printResults();
	}
}
