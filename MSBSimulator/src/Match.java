
public class Match {
	public Team home;
	public Team away;
	
	public Match(Team home, Team away) {
		this.home = home;
		this.away = away;
	}
	
	@Override
	public String toString() {
		return home.abbrv + " vs. " + away.abbrv;
	}
}
