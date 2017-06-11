import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class PlayoffFileParser {
	String playoffFileName, teamFileName;
	
	public PlayoffFileParser(String playoffFileName, String teamFileName) {
		this.playoffFileName = playoffFileName;
		this.teamFileName = teamFileName;
	}
	
	public List<PlayoffMatch> getPlayoffMatches() {
		List<PlayoffMatch> out = new ArrayList<PlayoffMatch>();
		TeamFileParser tfp = new TeamFileParser(teamFileName);
		Map<String,Team> teams = tfp.getTeams();
		
		try {
			BufferedReader br = new BufferedReader(new FileReader(playoffFileName));
			String line = br.readLine();
			while(line != null) {
				String[] ls = line.split(",");
				Team home = null ; //todo replace
			}			
			br.close();
		} catch (FileNotFoundException e) {
			System.err.println("ERROR: Playoff File Not Found");
			return null;
		} catch (IOException e) {
			System.err.println("ERROR: Playoff File IO Exception");
			return null;
		}
		
		return out;
	}
}
