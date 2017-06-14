import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class GroupSimulator {
	Map<String,Team> teams;
	List<Match> matches;
	String gameFileName;
	
	public GroupSimulator(String teamFileName, String gameFileName) {
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
		
		//prune out non-participants
		List<String> toRemove = new LinkedList<String>();
		
		//for (String teamName : teams.keySet()) {
			
			//horrible coupled bullshit
			if (gameFileName.contains("group2")){
				teams.remove("TS");
				teams.remove("DG");
				teams.remove("ES");
				teams.remove("L5");
				teams.remove("LA");
				teams.remove("TW");
			}
			
			else {
				teams.remove("R2");
				teams.remove("OC");
				teams.remove("MB");
				teams.remove("FN");
				teams.remove("SE");
				teams.remove("SP");
			}
			
			
			//Team t = teams.get(teamName);
			/**if (t.teamsBeat.isEmpty() && t.teamsDrawn.isEmpty() && t.teamsLostTo.isEmpty()) {
				toRemove.add(teamName);
			}*/
		//}
		
		//for (String s : toRemove) {
		//	teams.remove(s);
		//}
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
	
	public List<Team> getTopTwo() {
		List<Team> sortedTeams = getTeamsSortedByPoints();
		return sortedTeams.subList(0, 2);
	}
	
	public List<Team> getNextTwo() {
		List<Team> sortedTeams = getTeamsSortedByPoints();
		return sortedTeams.subList(2, 4);
	}
	
	public static void main(String[] args) {
		GroupSimulator gs = new GroupSimulator("data/teams.csv", "data/group1.csv");
		gs.simulate();
		List<Team> teams = gs.getTeamsSortedByPoints();
		for (Team t : teams) {
			System.out.println(t);
		}
	}

	public List<Team> getLastTwo() {
		List<Team> sortedTeams = getTeamsSortedByPoints();
		return sortedTeams.subList(4, 6);
	}

}
