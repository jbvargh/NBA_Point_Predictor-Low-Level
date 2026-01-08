import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

def check_player_trend(player_name, is_home):
    p = players.find_players_by_full_name(player_name)[0]
    id = p['id']
    log = playergamelog.PlayerGameLog(player_id = id, season='2025-26')
    df = log.get_data_frames()[0]
    print(df.head())
    if df.empty:
        return f"Error: {player_name} has not played any games in 2025-26."
    last_avg = df.head(10)['PTS'].mean()
    if is_home:
        season_avg = df[df['MATCHUP'].str.contains('vs.')]['PTS'].mean()
    else:
        season_avg = df[df['MATCHUP'].str.contains('@')]['PTS'].mean()
    if pd.isna(season_avg):
        season_avg = df['PTS'].mean()
    trend = "Neutral"
    if last_avg - season_avg >= 3.0:
        trend = "Heating Up"
    elif last_avg - season_avg <= -3.0:
        trend = "Slumping"
    return {"player": player_name, "all_point_totals": df['PTS'].tolist(), "season_ppg": round(float(season_avg), 1), "recent_ppg": round(float(last_avg), 1), "diff": round(float(last_avg - season_avg), 1), "status": trend}


