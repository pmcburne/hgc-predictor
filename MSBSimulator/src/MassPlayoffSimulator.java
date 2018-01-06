import java.util.Map;

public class MassPlayoffSimulator {
	final int SIM_COUNT = 10000;
	final int NUM_MATCHES = 10;
	
	String teamFileName, playoffFileName;
	
	public MassPlayoffSimulator(String teamFileName, String playoffFileName) {
		this.teamFileName = teamFileName;
		this.playoffFileName = playoffFileName;
	}
	
	public PlayoffMatchSummary[] simulate() {
		PlayoffMatchSummary[] pms = new PlayoffMatchSummary[NUM_MATCHES];
		for (int i = 0; i < NUM_MATCHES; i++) {
			pms[i] = new PlayoffMatchSummary(SIM_COUNT);
		}
		
		TeamFileParser tfp = new TeamFileParser(teamFileName);
		PlayoffFileParser pfp = new PlayoffFileParser(playoffFileName, teamFileName);
		
		for (int i = 0; i < SIM_COUNT; i++) {
			Map<String,Team> teams = tfp.getTeams();
			Playoff po = pfp.getPlayoffMatches();
			po.simulateMatches();
			for (int matchNumber = 1; matchNumber <= NUM_MATCHES; matchNumber++){
				pms[matchNumber-1].addMatch(po.matches.get(matchNumber));
			}
		}
		
		return pms;
	}
	
	public static void main(String[] args) {
		MassPlayoffSimulator mps = new MassPlayoffSimulator("data/teams.csv", "data/playoff.csv");
		PlayoffMatchSummary[] pms = mps.simulate();
		for(int i = 0; i < pms.length; i++) {
			System.out.println("=============MATCH " + (i + 1) + "===============");
			System.out.println(pms[i]);
		}
	}
}
