import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class TeamFileParser {
	public String fileName;
	
	public TeamFileParser(String fileName) {
		this.fileName = fileName;
	}
	
	public Map<String,Team> getTeams() {
		//output hashmap
		HashMap<String,Team> teams = new HashMap<String,Team>();
		
		//read file
		try {
			BufferedReader reader = new BufferedReader( new FileReader(fileName));
			String line = reader.readLine();
			while (line != null) {
				String[] ls = line.split(",");
				Team t = new Team(ls[0], Integer.parseInt(ls[1]));
				teams.put(ls[0], t);
				line = reader.readLine();
			}
			
		} catch (FileNotFoundException e) {
			System.err.println("TeamFileParser ERROR: File Not Found: Returning Null");
			return null;
		} catch (IOException e) {
			System.err.println("TeamFileParser ERROR: IO Error: Returning Null");
			return null;
		}
		
		return teams;
	}
	
	public static void main(String[] args) {
		System.out.println("Testing Team File Parser");
		TeamFileParser tfp = new TeamFileParser("data/teams.csv");
		Map<String,Team> teams = tfp.getTeams();
		
		for (String abbrv : teams.keySet()) {
			System.out.println(abbrv + teams.get(abbrv));
		}
	}
}
