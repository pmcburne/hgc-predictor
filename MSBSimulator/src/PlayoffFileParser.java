import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PlayoffFileParser {
	String playoffFileName, teamFileName;
	
	public PlayoffFileParser(String playoffFileName, String teamFileName) {
		this.playoffFileName = playoffFileName;
		this.teamFileName = teamFileName;
	}
	
	public Playoff getPlayoffMatches() {
		Map<Integer,PlayoffMatch> playoffMatches = new HashMap<Integer,PlayoffMatch>();
		TeamFileParser tfp = new TeamFileParser(teamFileName);
		Map<String,Team> teams = tfp.getTeams();
		
		try {
			BufferedReader br = new BufferedReader(new FileReader(playoffFileName));
			String line = br.readLine();
			while(line != null) {
				Team home, away;
				boolean bo5 = false;
				String[] ls = line.split(",");
				int gameNum = Integer.parseInt(ls[0]);//0 game number
				if (ls[1].length() < 2) {
					home = null;
					away = null;
				} else {
					home = teams.get(ls[1]);
					away = teams.get(ls[2]);
				}
				/**
				int homeWins = Integer.parseInt(ls[3]);
				int awayWins = Integer.parseInt(ls[4]);
				*/
				if (1 == Integer.parseInt(ls[3])) {
					bo5 = true;
				}
				
				int winnerGoesTo = Integer.parseInt(ls[5]);
				int loserGoesTo = Integer.parseInt(ls[6]);
				
				PlayoffMatch newMatch = new PlayoffMatch(gameNum, home, away, winnerGoesTo, loserGoesTo, bo5);
				playoffMatches.put(gameNum, newMatch);
				
				line = br.readLine();				
			}			
			br.close();
		} catch (FileNotFoundException e) {
			System.err.println("ERROR: Playoff File Not Found");
			return null;
		} catch (IOException e) {
			System.err.println("ERROR: Playoff File IO Exception");
			return null;
		}
		
		return new Playoff(playoffMatches);
	}
	
	public static void main(String[] args) {
		PlayoffFileParser pfp = new PlayoffFileParser("data/playoff.csv", "data/teams.csv");
		Playoff po = pfp.getPlayoffMatches();
		po.printMatches();
		po.simulateMatches();
		po.printMatches();
	}
}
