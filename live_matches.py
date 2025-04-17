import streamlit as st
import http.client
import json
import time
import sys

def get_live_cricket_matches():
    """Fetches live cricket matches using the free cricket API"""
    try:
        conn = http.client.HTTPSConnection("free-cricbuzz-cricket-api.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': "7da27a715amsh3eb2d9745051b01p14b8bbjsn50e955d8c9b9",
            'x-rapidapi-host': "free-cricbuzz-cricket-api.p.rapidapi.com"
        }
        
        conn.request("GET", "/cricket-matches-live", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        
        #return json.loads(data.decode("utf-8"))
        return {"status":"success","response":[{"seriesName":"TRI-NATION SERIES IN UAE, 2025","matchList":[{"seriesId":"9498","matchId":"116083","matchTitle":"Ireland A vs Afghanistan A","matchFormat":" 3rd Match","matchVenue":"Abu Dhabi, Sheikh Zayed Stadium","matchDate":"Apr 17","matchTime":" 10:00 AM LOCAL ","teamOne":{"name":"AFGA","score":"","status":"bowl"},"teamTwo":{"name":"IREA","score":"64-2 (12 Ovs)","status":"bat"},"matchStatus":"Afghanistan A opt to bowl","currentStatus":"live"}]},{"seriesName":"ICC WOMENS WORLD CUP QUALIFIER, 2025","matchList":[{"seriesId":"9532","matchId":"116364","matchTitle":"Bangladesh Women vs West Indies Women","matchFormat":" 11th Match","matchVenue":"Lahore, Lahore City Cricket Associ","matchDate":"Apr 17","matchTime":" 09:30 AM LOCAL ","teamOne":{"name":"WIW","score":"","status":"bowl"},"teamTwo":{"name":"BANW","score":"163-5 (35.3 Ovs)","status":"bat"},"matchStatus":"Bangladesh Women opt to bat","currentStatus":"live"}]}]}
    except Exception as e:
        print(f"Error fetching live cricket matches: {e}", file=sys.stderr)
        return {"status": "error", "response": []}

def get_match_details(match_id):
    """Fetches detailed information for a specific match"""
    try:
        conn = http.client.HTTPSConnection("free-cricbuzz-cricket-api.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': "7da27a715amsh3eb2d9745051b01p14b8bbjsn50e955d8c9b9",
            'x-rapidapi-host': "free-cricbuzz-cricket-api.p.rapidapi.com"
        }
        
        conn.request("GET", f"/cricket-match-scoreboard?matchid={match_id}", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        
        return json.loads(data.decode("utf-8"))
        return {"status":"success","response":{"firstInnings":{"batters":[{"name":"Stephen Doheny","dismissal":"c Zubaid Akbari b Farmanullah Safi","runs":"32","balls":"25","fours":"2","sixes":"2","strikeRate":"128.00"},{"name":"Cade Carmichael","dismissal":"c and b Sharafuddin Ashraf","runs":"18","balls":"25","fours":"2","sixes":"0","strikeRate":"72.00"},{"name":"Christopher De Freitas","dismissal":"batting","runs":"10","balls":"19","fours":"2","sixes":"0","strikeRate":"52.63"},{"name":"Morgan Topping","dismissal":"batting","runs":"7","balls":"9","fours":"1","sixes":"0","strikeRate":"77.78"}],"didNotBat":{},"fallOfWickets":{"label":"Fall Of Wickets","detail":[{"name":"Cade Carmichael","score":"52-1","overs":"7.6"},{"name":"Stephen Doheny","score":"54-2","overs":"8.5"}]},"bowlers":[{"name":"Naveed Zadran","overs":"4","maidens":"0","runs":"25","wickets":"0","noBalls":"0","wides":"0","eco":"6.20"},{"name":"Khalil Ahmed","overs":"3","maidens":"0","runs":"12","wickets":"0","noBalls":"0","wides":"2","eco":"4.00"},{"name":"Sharafuddin Ashraf","overs":"3","maidens":"0","runs":"19","wickets":"1","noBalls":"0","wides":"0","eco":"6.30"},{"name":"Farmanullah Safi","overs":"3","maidens":"0","runs":"13","wickets":"1","noBalls":"0","wides":"0","eco":"4.30"}],"extras":{"details":"(b 0, lb 1, w 2, nb 0, p 0)","runs":"3"},"total":{"details":"(2 wkts, 13 Ov)","runs":"70"},"powerplays":{"label":"Mandatory","overs":"0.1-10","runs":"58"}},"secondInnings":{"batters":[],"didNotBat":{},"fallOfWickets":{"label":"Fall Of Wickets","detail":[]},"bowlers":[],"extras":{},"total":{},"powerplays":{"label":"","overs":"","runs":""}}}}
    except Exception as e:
        print(f"Error fetching match details: {e}", file=sys.stderr)
        return {"status": "error", "response": {}}

def display_live_matches():
    """Display live cricket matches in a Streamlit component"""
    # Add auto-refresh option
    auto_refresh = True
    
    # Container for match data that will be refreshed
    match_container = st.container()
    
    # Function to load and display matches
    def load_matches():
        with match_container:
            st.empty()  # Clear previous content
            
            with st.spinner("Fetching live matches..."):
                live_matches = get_live_cricket_matches()
            
            if live_matches.get("status") == "success" and live_matches.get("response"):
                for series in live_matches["response"]:
                    st.subheader(series.get("seriesName", "Unknown Series"))
                    
                    for match in series.get("matchList", []):
                        with st.expander(f"{match.get('matchTitle', 'Unknown Match')}", expanded=True):
                            # Live indicator
                            if match.get('currentStatus') == 'live':
                                st.markdown("🔴 **LIVE**")
                            
                            # Match status
                            status = match.get('matchStatus', 'N/A')
                            st.write(f"**Status:** {status}")
                            
                            # Team information with proper formatting
                            team1 = match.get('teamOne', {})
                            team2 = match.get('teamTwo', {})
                            
                            # Get team codes and format them properly
                            team1_code = team1.get('teamShortName', team1.get('name', 'Team 1'))
                            team2_code = team2.get('teamShortName', team2.get('name', 'Team 2'))
                            
                            # Format scores
                            team1_score = team1.get('score', '')
                            team2_score = team2.get('score', '')
                            
                            # Add overs information if available
                            team1_overs = team1.get('overs', '')
                            if team1_score and team1_overs:
                                team1_display = f"{team1_score} ({team1_overs} Ovs)"
                            elif team1_score:
                                team1_display = team1_score
                            else:
                                team1_display = "Yet to bat"
                                
                            team2_overs = team2.get('overs', '')
                            if team2_score and team2_overs:
                                team2_display = f"{team2_score} ({team2_overs} Ovs)"
                            elif team2_score:
                                team2_display = team2_score
                            else:
                                team2_display = "Yet to bat"
                            
                            # Display team scores in a format similar to the image
                            st.write(f"**{team1_code}:** {team1_display}")
                            st.write(f"**{team2_code}:** {team2_display}")
            else:
                st.info("No live matches available at the moment.")
            
            # Show last updated time
            st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initial load
    load_matches()
    
    # Auto-refresh logic with non-blocking approach
    if auto_refresh:
        placeholder = st.empty()
        
        # Use a session state counter instead of a blocking loop
        if "refresh_counter" not in st.session_state:
            st.session_state.refresh_counter = 30
        
        # Display current countdown
        placeholder.text(f"Next refresh in {st.session_state.refresh_counter} seconds")
        
        # Schedule the next refresh
        if st.session_state.refresh_counter <= 0:
            st.session_state.refresh_counter = 30
            load_matches()
            st.rerun()
        else:
            # Decrement counter for next run
            st.session_state.refresh_counter -= 1

if __name__ == "__main__":
    st.set_page_config(
        page_title="Live Cricket Matches",
        page_icon="🏏",
        layout="wide"
    )
    st.title("🏏 Live Cricket Matches")
    display_live_matches()
