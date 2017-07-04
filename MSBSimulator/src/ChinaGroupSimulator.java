import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class ChinaGroupSimulator {
	Map<String,Team> teams;
	List<Match> matches;
	String gameFileName;
	
	public ChinaGroupSimulator(String teamFileName, String gameFileName) {
		this.gameFileName = gameFileName;
		TeamFileParser tfp = new TeamFileParser(teamFileName);
		teams = tfp.getTeams();
		GameFileParser gfp = new GameFileParser(gameFileName, teams);
		matches = gfp.getMatches();
	}
	
	public void simulate() {
		MatchSimulator simulator = new BestOfTwoSimulator();
		for (Match m : matches) {
			simulator.simulateMatch(m.home, m.away);
		}
	}
	
	public List<Team> getTeamsSortedByPoints() {
		List<Team> teamList = new ArrayList<Team>();
		for (String teamName : teams.keySet()) {
			teamList.add(teams.get(teamName));
		}
		
		teamList.sort(new TeamComparator());
		Collections.reverse(teamList);
		
		return teamList;
	}
	
	public List<Team> getTopThree() {
		List<Team> sortedTeams = getTeamsSortedByPoints();
		return sortedTeams.subList(0, 3);
	}
	
	public List<Team> getLastTwo() {
		List<Team> sortedTeams = getTeamsSortedByPoints();
		return sortedTeams.subList(6, 8);
	}
	
	public static void main(String[] args) {
		GroupSimulator gs = new GroupSimulator("data/cnTeams.csv", "data/cn.csv");
		gs.simulate();
		List<Team> teams = gs.getTeamsSortedByPoints();
		for (Team t : teams) {
			System.out.println(t);
		}
	}
}
