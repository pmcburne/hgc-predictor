import java.util.HashMap;
import java.util.Map;

public class PlayoffMatchSummary {
	Map<String,Integer> participantCount;
	Map<String,Integer> winCount;
	int simCount;
	
	public PlayoffMatchSummary(int simCount) {
		participantCount = new HashMap<String,Integer>();
		winCount = new HashMap<String,Integer>();
		this.simCount = simCount;
	}
	
	public void addMatch(PlayoffMatch pm) {
		addParticipants(pm);
		addWinner(pm);
	}

	private void addWinner(PlayoffMatch pm) {
		Team t = pm.getWinner();
		if (winCount.keySet().contains(t.abbrv)) {
			winCount.put(t.abbrv, winCount.get(t.abbrv) + 1);
		} else {
			winCount.put(t.abbrv, 1);
		}
	}

	private void addParticipants(PlayoffMatch pm) {
		Team t1 = pm.home;
		if (participantCount.keySet().contains(t1.abbrv)) {
			participantCount.put(t1.abbrv, participantCount.get(t1.abbrv) + 1);
		} else {
			participantCount.put(t1.abbrv, 1);
		}
		Team t2 = pm.away;
		if (participantCount.keySet().contains(t2.abbrv)) {
			participantCount.put(t2.abbrv, participantCount.get(t2.abbrv) + 1);
		} else {
			participantCount.put(t2.abbrv, 1);
		}
		
	}
	
	public String toString() {
		String out = "----win counts----";
		for (String teamName : winCount.keySet()) {
			out += "\n"+ teamName + " - " + (((10000 * winCount.get(teamName))/(100.0 *simCount)));
		}
		out += "\n----participant counts----";
		for (String teamName : participantCount.keySet()) {
			out += "\n" + teamName + " - " + (((10000 * participantCount.get(teamName))/(100.0 * simCount)));
		}
		
		return out;
	}
}
