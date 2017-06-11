import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class GameFileParser {
	String fileName;
	Map<String,Team> teams;

	public GameFileParser(String fileName, Map<String, Team> teams) {
		this.fileName = fileName;
		this.teams = teams;
	}

	@SuppressWarnings("resource")
	public List<Match> getMatches() {
		List<Match> matches = new LinkedList<Match>();
		BufferedReader reader;
		// read file
		try {
			reader = new BufferedReader(new FileReader(fileName));
			String line = reader.readLine();
			while (line != null) {
				String[] ls = line.split(",");
				
				if (!teams.containsKey(ls[0])) {
					throw new IllegalStateException("ERROR: Team abbrv " + ls[0] + " not found in teams.");
				}
				if (!teams.containsKey(ls[1])) {
					throw new IllegalStateException("ERROR: Team abbrv " + ls[0] + " not found in teams.");
				}
				
				Match t = new Match(teams.get(ls[0]), teams.get(ls[1]));
				matches.add(t);
				
				line = reader.readLine();
			}
			reader.close();

		} catch (FileNotFoundException e) {
			System.err.println("GameFileParser ERROR: File Not Found: Returning Null");
			return null;
		} catch (IOException e) {
			System.err.println("GameFileParser ERROR: IO Error: Returning Null");
			return null;
		}
		return matches;
	}
	
	public static void main(String[] args) {
		//System.out.println("Testing Game File Parser");
		TeamFileParser tfp = new TeamFileParser("data/teams.csv");
		Map<String,Team> teams = tfp.getTeams();
		GameFileParser gfp = new GameFileParser("data/group2.csv", teams);
		List<Match> matches = gfp.getMatches();
		for (Match i : matches) {
			System.out.println(i);
		}
	}
}
