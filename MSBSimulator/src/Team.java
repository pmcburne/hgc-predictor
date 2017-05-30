import java.util.HashSet;
import java.util.Set;

public class Team {
	public String abbrv;
	public int elo;
	public int points;
	public Set<Team> teamsBeat;
	public Set<Team> teamsDrawn;
	public Set<Team> teamsLostTo;
	
	public boolean suddenDeathWin = false;

	public Team(String abbrv, int elo) {
		this.abbrv = abbrv;
		this.elo = elo;
		points = 0;
		teamsBeat = new HashSet<Team>();
		teamsDrawn = new HashSet<Team>();
		teamsLostTo = new HashSet<Team>();
	}
	
	@Override
	public int hashCode() {
		return abbrv.hashCode();
	}
	
	@Override
	public boolean equals(Object o) {
		try {
			Team other = (Team) o;
			return this.abbrv == other.abbrv;
		} catch(ClassCastException e) {
			return false;
		}
	}
	
	@Override
	public String toString() {
		String out = abbrv + " - " + elo + " - " + points + "\n";
		out += "\tBeat - " + teamSetToString(teamsBeat) + "\n";
		out += "\tDrawn - " + teamSetToString(teamsDrawn) + "\n";
		out += "\tLost to - " + teamSetToString(teamsLostTo) + "\n";
		return out;
	}
	
	private String teamSetToString(Set<Team> teams) {
		if (teams.isEmpty()) {
			return "None";
		}
		String out = "";
		boolean first = true;
		for (Team t : teams) {
			if(first) {
				first = false;
			} else {
				out +=",";
			}
			out += t.abbrv;
		}
		return out;
	}
}
