import java.util.Comparator;

public class TeamComparator implements Comparator<Team>{

	@Override
	public int compare(Team t1, Team t2) {
		if (t1.points != t2.points) {
			return t1.points - t2.points;
		} else { //sudden death
			if(Math.random() < MatchSimulator.getHomeWinExpected(t1, t2)) {
				return 1;
			} else {
				return -1;
			}
		}
		
		/** Head to head 
		 * else if(t1.teamsBeat.contains(t2.abbrv)) {
		
			return 1;
		} else if (t2.teamsBeat.contains(t2.abbrv)) {
			return -1;
		} else {
			return 0;
		}
		*/
		
		
	}

}
